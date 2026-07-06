"""Anker MagGo 3-in-1 Wireless Charger model.

.. moduleauthor:: reverse-engineered by community contribution

"""

from ..const import DEFAULT_METADATA_FLOAT
from ..prime_device import PrimeDevice
from ..states import PortStatus

#: Command sent after connecting to start the telemetry stream. Like the C1000
#: Gen 2, this charger streams nothing until it receives this subscribe command.
CMD_SUBSCRIBE = "4200"
SUBSCRIBE_PAYLOAD = "a10121"


class MagGo3in1(PrimeDevice):
    """
    Anker MagGo 3-in-1 Wireless Charger (model A25x7, serial prefix ``ASHDKXU``).

    Use this class to connect and monitor the 3-in-1 wireless charging station
    (phone MagSafe pad + Apple Watch puck + earbuds pad).

    It uses the same ECDH + AES-GCM encryption and telemetry framing as the
    Prime chargers, but streams nothing until it receives a subscribe command
    (``0200`` / ``4200`` with the encryption flag). Telemetry then arrives on
    command ``4300`` as a compact report: three wireless pads live in TLV
    parameters ``a2``/``a3``/``a4``, each with the ``04 <status> <volt LE>
    <current LE> <power LE>`` per-port shape used by the Prime chargers.

    .. note::
        Reverse-engineered from BLE captures. **Per-pad power was confirmed**
        against an Apple Watch charging at 2.8 W (``a2[6:8]`` little-endian
        ``0x011d`` = 285 -> 2.85 W). The per-pad voltage/current fields
        (``[2:4]``/``[4:6]``) are present but their scaling was not confidently
        confirmed for wireless pads, so only power + status are exposed here.
    """

    #: This charger only reports telemetry on command ``4300``.
    _TELEMETRY_COMMANDS: tuple[str, ...] = ("4300",)

    async def _post_connect(self) -> None:
        """Subscribe to telemetry once connected.

        The charger streams no telemetry until it receives this command, so we
        send it after every (re)connection.
        """
        await self._send_command(
            cmd=bytes.fromhex(CMD_SUBSCRIBE),
            payload=bytes.fromhex(SUBSCRIBE_PAYLOAD),
        )

    @property
    def pad_1(self) -> PortStatus:
        """Wireless pad 1 status (TLV ``a2``).

        :returns: Status of pad 1.
        """
        return PortStatus(self._parse_int("a2", begin=1, end=2))

    @property
    def pad_1_power(self) -> float:
        """Wireless pad 1 power (W).

        :returns: Power delivered by pad 1 or default float value.
        """
        if self._data is None:
            return DEFAULT_METADATA_FLOAT
        return self._parse_int("a2", begin=6, end=8) / 100.0

    @property
    def pad_2(self) -> PortStatus:
        """Wireless pad 2 status (TLV ``a3``).

        :returns: Status of pad 2.
        """
        return PortStatus(self._parse_int("a3", begin=1, end=2))

    @property
    def pad_2_power(self) -> float:
        """Wireless pad 2 power (W).

        :returns: Power delivered by pad 2 or default float value.
        """
        if self._data is None:
            return DEFAULT_METADATA_FLOAT
        return self._parse_int("a3", begin=6, end=8) / 100.0

    @property
    def pad_3(self) -> PortStatus:
        """Wireless pad 3 status (TLV ``a4``).

        :returns: Status of pad 3.
        """
        return PortStatus(self._parse_int("a4", begin=1, end=2))

    @property
    def pad_3_power(self) -> float:
        """Wireless pad 3 power (W).

        :returns: Power delivered by pad 3 or default float value.
        """
        if self._data is None:
            return DEFAULT_METADATA_FLOAT
        return self._parse_int("a4", begin=6, end=8) / 100.0

    @property
    def total_power(self) -> float:
        """Total power delivered across all three pads (W).

        :returns: Sum of all pad power or default float value.
        """
        if self._data is None:
            return DEFAULT_METADATA_FLOAT
        return round(self.pad_1_power + self.pad_2_power + self.pad_3_power, 2)
