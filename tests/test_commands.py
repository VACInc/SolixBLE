"""Tests for the execution of on-device commands.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""

from contextlib import nullcontext
from unittest import mock

import pytest

from SolixBLE.device import SolixBLEDevice
from SolixBLE.prime_device import PrimeDevice
from tests.const import MOCK_BLE_DEVICE
from tests.devices.c300 import C300_TEST_COMMANDS, C300_TEST_COMMANDS_RESPONSES
from tests.devices.c300dc import C300DC_TEST_COMMANDS
from tests.devices.c800 import C800_TEST_COMMANDS, C800_TEST_COMMANDS_RESPONSES
from tests.devices.c1000 import C1000_TEST_COMMANDS, C1000_TEST_COMMANDS_RESPONSES
from tests.devices.c1000g2 import C1000G2_TEST_COMMANDS
from tests.devices.f2600 import F2600_TEST_COMMANDS, F2600_TEST_COMMANDS_RESPONSES
from tests.devices.f3800 import F3800_TEST_COMMANDS
from tests.devices.prime_160w_charger import PRIME_CHARGER_160W_TEST_COMMANDS
from tests.devices.prime_250w_charger import PRIME_CHARGER_250W_TEST_COMMANDS


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("device_class", "function", "arguments", "expected"),
    [
        *C300_TEST_COMMANDS,
        *C300DC_TEST_COMMANDS,
        *C800_TEST_COMMANDS,
        *C1000_TEST_COMMANDS,
        *C1000G2_TEST_COMMANDS,
        *F2600_TEST_COMMANDS,
        *F3800_TEST_COMMANDS,
        *PRIME_CHARGER_160W_TEST_COMMANDS,
        *PRIME_CHARGER_250W_TEST_COMMANDS,
    ],
)
async def test_send_command(
    device_class: type[SolixBLEDevice],
    function: str,
    arguments: list,
    expected: Exception | list[(str, str)],
) -> None:
    """
    Test that the expected command is sent to the mock device.

    :param device_class: Class of device under test.
    :param function: Function to be called.
    :param arguments: Arguments to be given to function.
    :param expected: Error or expected cmd and payload calls to _send_command.
    """

    mock_function_name = (
        "SolixBLE.PrimeDevice._send_command" if
        issubclass(device_class, PrimeDevice) else
        "SolixBLE.SolixBLEDevice._send_command"
    )

    device = device_class(MOCK_BLE_DEVICE)
    with (
        mock.patch(mock_function_name) as mocked,
        pytest.raises(expected) if isinstance(expected, type) else nullcontext(),
    ):

        fn = getattr(device, function)
        await fn(*arguments)

        for call in expected:
            mocked.assert_called_once_with(
                cmd=bytes.fromhex(call[0]),
                payload=bytes.fromhex(call[1]),
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("device_class", "function", "arguments", "expected", "listen", "returned"),
    [
        *C300_TEST_COMMANDS_RESPONSES,
        *C800_TEST_COMMANDS_RESPONSES,
        *C1000_TEST_COMMANDS_RESPONSES,
        *F2600_TEST_COMMANDS_RESPONSES,
    ],
)
async def test_send_command_response(  # noqa: PLR0913, PLR0917
    device_class: type[SolixBLEDevice],
    function: str,
    arguments: list,
    expected: list[(str, str)],
    listen: list[str, str, str | None],
    returned: dict | Exception | None,
) -> None:
    """
    Test sending of commands and handling of response.

    Test that the expected command is sent to the mock device
    and return a response and assert that the correct result
    is returned by the function, if any.

    :param device_class: Class of device under test.
    :param function: Function to be called.
    :param arguments: Arguments to be given to function.
    :param expected: Expected cmd and payload calls to _send_command.
    :param listen: Result(s) of calling _listen_for_packet(pattern, cmd).
    :param returned: Expected return value of the function.
    """

    mock_function_name = (
        "SolixBLE.PrimeDevice._send_command" if
        issubclass(device_class, PrimeDevice) else
        "SolixBLE.SolixBLEDevice._send_command"
    )

    device = device_class(MOCK_BLE_DEVICE)
    with (
        mock.patch(mock_function_name) as mock_send,
        mock.patch("SolixBLE.SolixBLEDevice._listen_for_packet") as mock_listen,
        pytest.raises(returned) if isinstance(returned, type) else nullcontext(),
    ):
        mock_listen.side_effect = [bytes.fromhex(p[2] or b"") for p in listen]

        fn = getattr(device, function)
        result = await fn(*arguments)
        assert result == returned

        for call in expected:
            mock_send.assert_called_once_with(
                cmd=bytes.fromhex(call[0]),
                payload=bytes.fromhex(call[1]),
            )

        for call in listen:
            mock_listen.assert_called_once_with(
                bytes.fromhex(call[0]),
                bytes.fromhex(call[1]),
            )
