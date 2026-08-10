"""C300(X) DC power station device tests.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""
import pytest

from SolixBLE.devices.c300dc import C300DC
from SolixBLE.states import DisplayTimeout, LightStatus

########################
# Test device commands #
########################

# These tests are for sending commands to the device and making sure the
# correct calls are made to the command sending functions and errors are
# raised where appropriate. See test_send_command() in test_commands.py.

C300DC_TEST_COMMANDS = [
    pytest.param(
        C300DC,
        "turn_dc_on",
        [],
        [("404b", "a10121a2020101")],
        id="c300dc_dc_on",
    ),
    pytest.param(
        C300DC,
        "turn_dc_off",
        [],
        [("404b", "a10121a2020100")],
        id="c300dc_dc_off",
    ),
    pytest.param(
        C300DC,
        "turn_display_on",
        [],
        [("4052", "a10121a2020101")],
        id="c300dc_display_on",
    ),
    pytest.param(
        C300DC,
        "turn_display_off",
        [],
        [("4052", "a10121a2020100")],
        id="c300dc_display_off",
    ),
    pytest.param(
        C300DC,
        "set_light_mode",
        [LightStatus.LOW],
        [("404f", "a10121a2020101")],
        id="c300dc_light_low",
    ),
    pytest.param(
        C300DC,
        "set_light_mode",
        [LightStatus.MEDIUM],
        [("404f", "a10121a2020102")],
        id="c300dc_light_med",
    ),
    pytest.param(
        C300DC,
        "set_light_mode",
        [LightStatus.HIGH],
        [("404f", "a10121a2020103")],
        id="c300dc_light_high",
    ),
     pytest.param(
        C300DC,
        "set_display_timeout",
        [DisplayTimeout.S20],
        [("4046", "a10121a203021400")],
        id="c300dc_display_timeout_20s",
    ),
    pytest.param(
        C300DC,
        "set_display_timeout",
        [DisplayTimeout.S1800],
        [("4046", "a10121a203020807")],
        id="c300dc_display_timeout_30m",
    ),
    pytest.param(
        C300DC,
        "set_display_mode",
        [LightStatus.LOW],
        [("404c", "a10121a2020101")],
        id="c300dc_display_low",
    ),
    pytest.param(
        C300DC,
        "set_display_mode",
        [LightStatus.MEDIUM],
        [("404c", "a10121a2020102")],
        id="c300dc_display_med",
    ),
    pytest.param(
        C300DC,
        "set_display_mode",
        [LightStatus.HIGH],
        [("404c", "a10121a2020103")],
        id="c300dc_display_high",
    ),
    pytest.param(
        C300DC,
        "set_display_mode",
        [LightStatus.SOS],
        ValueError,
        id="c300dc_display_sos",
    ),
    pytest.param(
        C300DC,
        "set_display_mode",
        [LightStatus.UNKNOWN],
        ValueError,
        id="c300dc_display_unknown",
    ),
]
