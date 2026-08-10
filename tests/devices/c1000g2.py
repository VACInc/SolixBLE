"""C1000G2 power station device tests.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""
import pytest

from SolixBLE.devices.c1000g2 import C1000G2

########################
# Test device commands #
########################

# These tests are for sending commands to the device and making sure the
# correct calls are made to the command sending functions and errors are
# raised where appropriate. See test_send_command() in test_commands.py.

C1000G2_TEST_COMMANDS = [
    pytest.param(
        C1000G2,
        "turn_ac_on",
        [],
        [("4101", "a10121a2020101")],
        id="c1000g2_ac_on",
    ),
    pytest.param(
        C1000G2,
        "turn_ac_off",
        [],
        [("4101", "a10121a2020100")],
        id="c1000g2_ac_off",
    ),
    pytest.param(
        C1000G2,
        "turn_dc_on",
        [],
        [("4102", "a10121a2020101")],
        id="c1000g2_dc_on",
    ),
    pytest.param(
        C1000G2,
        "turn_dc_off",
        [],
        [("4102", "a10121a2020100")],
        id="c1000g2_dc_off",
    ),
]
