"""C800(X) power station device tests.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""
import pytest

from SolixBLE.devices.c800 import C800
from SolixBLE.states import DisplayTimeout, LightStatus

########################
# Test device commands #
########################

# These tests are for sending commands to the device and making sure the
# correct calls are made to the command sending functions and errors are
# raised where appropriate. See test_send_command() in test_commands.py.

C800_TEST_COMMANDS = [
    pytest.param(
        C800,
        "turn_ac_on",
        [],
        [("404a", "a10121a2020101")],
        id="c800_ac_on",
    ),
    pytest.param(
        C800,
        "turn_ac_off",
        [],
        [("404a", "a10121a2020100")],
        id="c800_ac_off",
    ),
    pytest.param(
        C800,
        "turn_dc_on",
        [],
        [("404b", "a10121a2020101")],
        id="c800_dc_on",
    ),
    pytest.param(
        C800,
        "turn_dc_off",
        [],
        [("404b", "a10121a2020100")],
        id="c800_dc_off",
    ),
    pytest.param(
        C800,
        "set_light_mode",
        [LightStatus.LOW],
        [("404f", "a10121a2020101")],
        id="c800_light_low",
    ),
    pytest.param(
        C800,
        "set_light_mode",
        [LightStatus.MEDIUM],
        [("404f", "a10121a2020102")],
        id="c800_light_med",
    ),
    pytest.param(
        C800,
        "set_light_mode",
        [LightStatus.HIGH],
        [("404f", "a10121a2020103")],
        id="c800_light_high",
    ),
    pytest.param(
        C800,
        "set_light_mode",
        [LightStatus.SOS],
        [("404f", "a10121a2020104")],
        id="c800_light_sos",
    ),
    pytest.param(
        C800,
        "set_light_mode",
        [LightStatus.UNKNOWN],
        ValueError,
        id="c800_light_unknown",
    ),
    pytest.param(
        C800,
        "set_display_mode",
        [LightStatus.LOW],
        [("404c", "a10121a2020101")],
        id="c800_display_low",
    ),
    pytest.param(
        C800,
        "set_display_mode",
        [LightStatus.MEDIUM],
        [("404c", "a10121a2020102")],
        id="c800_display_med",
    ),
    pytest.param(
        C800,
        "set_display_mode",
        [LightStatus.HIGH],
        [("404c", "a10121a2020103")],
        id="c800_display_high",
    ),
    pytest.param(
        C800,
        "set_display_mode",
        [LightStatus.SOS],
        ValueError,
        id="c800_display_sos",
    ),
    pytest.param(
        C800,
        "set_display_mode",
        [LightStatus.UNKNOWN],
        ValueError,
        id="c800_display_unknown",
    ),
    pytest.param(
        C800,
        "set_display_timeout",
        [DisplayTimeout.S20],
        [("4046", "a10121a203021400")],
        id="c800_display_timeout_20s",
    ),
    pytest.param(
        C800,
        "set_display_timeout",
        [DisplayTimeout.S1800],
        [("4046", "a10121a203020807")],
        id="c800_display_timeout_30m",
    ),
    pytest.param(
        C800,
        "set_display_timeout",
        [DisplayTimeout.UNKNOWN],
        ValueError,
        id="c800_display_timeout_unknown",
    ),
    pytest.param(
        C800,
        "turn_display_on",
        [],
        [("4052", "a10121a2020101")],
        id="c800_display_on",
    ),
    pytest.param(
        C800,
        "turn_display_off",
        [],
        [("4052", "a10121a2020100")],
        id="c800_display_off",
    ),
]


####################################
# Test device commands & responses #
####################################

# These tests are for sending commands to the device and making sure the correct
# calls are made to the command sending functions, that the response is handled
# appropriately, the correct value is returned, and errors are raised where
# appropriate. See test_send_command_response() in test_commands.py.

C800_TEST_COMMANDS_RESPONSES = [
    pytest.param(
        C800,
        "get_status_update",
        [],
        [("4040", "a10121")],
        [("03010f", "c840", None)],
        TimeoutError,
        id="c800_status_update_error",
    ),
]
