"""Data structures of packets.

This module contains the byte structures used for encoding and
decoding the packet format used by Anker devices.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""

import operator
from functools import reduce
from typing import Any

from construct import (
    BitStruct,
    Bytes,
    Checksum,
    Const,
    ExprAdapter,
    GreedyBytes,
    GreedyRange,
    Hex,
    HexDump,
    If,
    Int8ul,
    Int16ul,
    Nibble,
    Optional,
    RawCopy,
    Rebuild,
    Struct,
    this,
)

from SolixBLE.utilities import _to_bytes


def _get_val(obj: Any, key: str, default: Any=None) -> Any:
    """
    Return value from dictionary, container, objects, or None.

    :param obj: Object to extract value from.
    :param key: The key or property to extract from the object.
    :param default: Default to return if not found.
    :returns: Found value or default.
    """
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

Packet = ExprAdapter(

    # Structure of the packet
    Struct(

        # Bytes of packet excluding checksum
        "content" / RawCopy(
            Struct(

                # Header of the packet
                "header" / Hex(Const(bytes.fromhex("ff09"))),

                # Length of the entire packet
                "length" / Rebuild(Int16ul, lambda this: 10 + len(this.payload_bytes)),

                # Pattern of the packet (e.g negotiation type, telemetry type etc)
                "pattern" / Hex(Bytes(3)),

                # Command of the packet (e.g turn on, off, etc)
                "cmd" / Hex(Bytes(2)),

                # Payload bytes of the packet (may be encrypted or fragmented)
                "payload_bytes" / HexDump(Bytes(lambda this: this.length - 10)),
            ),
        ),

        # XOR checksum of the packet
        "checksum" / Hex(Checksum(
            Int8ul,
            lambda data: reduce(operator.xor, data, 0),
            this.content.data,
        )),
    ),

    # Encoders and decoders which allow for direct access
    # (e.g packet.cmd rather than packet.content.cmd)
    decoder=lambda p, _: p.content.value,
    encoder=lambda p, _: {
            "content": {
                "value": {
                    "header": _to_bytes(_get_val(p, "header", "ff09")),
                    "pattern": _to_bytes(_get_val(p, "pattern")),
                    "cmd": _to_bytes(_get_val(p, "cmd")),
                    "payload_bytes": _to_bytes(_get_val(p, "payload_bytes", b"")),
                },
            },
    },
)
"""
Anker device packet.

This class represents a packet of an Anker device. Packets are made up of a
header, size, pattern, cmd, payload, and a checksum.

Structure: <Header 2B> <Size 2B> <Pattern 3B> <CMD 2B> <Payload nB> <Checksum 1B>.

Usage:
    .. code-block:: python
       :linenos:

        packet = Packet.parse(packet_bytes)
        print(f"p: {packet.pattern}, c: {packet.cmd}, b: {packet.payload_bytes}")

        packet_bytes = Packet.build({
            "pattern": "030001",
            "cmd": "0000",
            "payload_bytes": "a101a20200a303010000",
        })

"""

FragmentedPayload = Struct(

    # Fragment information
    "frag" / BitStruct(
        "index" / Nibble,
        "total" / Nibble,
    ),

    # The content of the payload
    "data" / GreedyBytes,
)
"""
Payload section of an Anker packet that is fragmented.

The "frag" section represents the fragmentation information of the payload.
This information is not always present in non-fragmented packets.

The "data" section represents the content of the fragment and may be encrypted.
The fragments must be re-assembled before decryption can begin.

This structure is used for re-assembling fragmented payloads only.

Structure: <Index 4b> <Total 4b> <Data nB>.

Usage:

    .. code-block:: python
       :linenos:

        frag_payload = FragmentedPayload.parse(payload_bytes)
        print(f"{frag_p.frag.index}/{frag_p.frag.total}: {frag_p.data}")

"""

Parameter = Struct(

    # The key of the parameter (e.g a1, a2, ...)
    "key" / Hex(Bytes(1)),

    # The length of the parameter excluding the key
    "length" / Rebuild(
        Int8ul,
        lambda p: (1 if p.get("type") is not None else 0) + len(p.get("value") or b""),
    ),

    # Optional type of the parameter
    "type" / If(
        lambda p: p.get("type") is not None if p._building else p.length > 1,
        Int8ul,
    ),

    # Optional content of the parameter
    "value" / If(
        lambda p: (p.length - (1 if p.type is not None else 0)) > 0,
        HexDump(Bytes(lambda p: p.length - (1 if p.type is not None else 0))),
    ),
)
"""
Individual parameter of a payload of an Anker packet.

Paramaters contain a key (e.g a1, a2, ...), the length, optional
type information, and an optional content.

Structure: <Key 1B> <Length 1B> <Type 1B> <Content nB>.

The length value is the length of the entire parameter excluding the key.

This structure is only used as a part of the Parameters type for creating,
modifying, encoding, and decoding payloads.
"""


class ParameterDict(dict):
    """
    Subclass to allow for direct action on the paramaters type.

    This is used to allow for the new parameters type to be
    converted to the legacy type for backwards compatibility.

    Usage:

        .. code-block:: python
           :linenos:

            parameters = Parameters.parse(complete_payload)
            old_parameters = parameters.to_legacy()

    """

    def __init__(self, *args, prefix: bytes | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    def to_legacy(self) -> dict[str, bytes]:
        """Return legacy format of paramaters."""
        return {k:
            (v.type.to_bytes(1) if v is not None and v.type is not None else b"") +
            (v.value or b"")
        for k, v in self.items()}


Parameters = ExprAdapter(
    Struct(

        # 0x00 optional prefix
        "prefix" / If(
            this._parsing or (this._building and this._.prefix is not None),
            Optional(Const(bytes.fromhex("00"))),
        ),

        # List of parameters
        "parameters" / GreedyRange(Parameter),
    ),
    decoder=lambda obj, _: ParameterDict(
        {p.key.hex(): p for p in obj.parameters},
        prefix=obj.prefix,
    ),
    encoder=lambda ps, _: {
        "prefix": getattr(ps, "prefix", None),
        "parameters": list(ps.values()) if isinstance(ps, dict) else ps,
    },
)
"""
Decoded parameters of the payload of an Anker packet.

The payload of Anker packets is made up of a list of
parameters and is sometimes prefixed with 00.

Structure: <Prefix 1B> <Parameter 1 nB> ... <Parameter n nB>.

This structure is used to encode, decode, modify, and generate payloads.

Usage:

    .. code-block:: python
       :linenos:

        parameters = Parameters.parse(reassembled_payload)
        parameters["a1"] = Parameter({
            "key": "a1",
            "type": 12,
            "value": "00ff",
        })

        plaintext_payload = Parameters.build(parameters)

"""
