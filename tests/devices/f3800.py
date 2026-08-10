"""F3800 power station device tests.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""
import pytest

from SolixBLE.devices.f3800 import F3800

########################
# Test device commands #
########################

# These tests are for sending commands to the device and making sure the
# correct calls are made to the command sending functions and errors are
# raised where appropriate. See test_send_command() in test_commands.py.

F3800_TEST_COMMANDS = [
    pytest.param(
        F3800,
        "turn_ac_on",
        [],
        [("404a", "a10121a2020101")],
        id="f3800_ac_on",
    ),
    pytest.param(
        F3800,
        "turn_ac_off",
        [],
        [("404a", "a10121a2020100")],
        id="f3800_ac_off",
    ),
    pytest.param(
        F3800,
        "turn_dc_on",
        [],
        [("404b", "a10121a2020101")],
        id="f3800_dc_on",
    ),
    pytest.param(
        F3800,
        "turn_dc_off",
        [],
        [("404b", "a10121a2020100")],
        id="f3800_dc_off",
    ),
]
