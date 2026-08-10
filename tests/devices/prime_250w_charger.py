"""Anker Prime 250w charger tests.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""
import pytest

from SolixBLE.devices.prime_charger_250w import PrimeCharger250w

########################
# Test device commands #
########################

# These tests are for sending commands to the device and making sure the
# correct calls are made to the command sending functions and errors are
# raised where appropriate. See test_send_command() in test_commands.py.

PRIME_CHARGER_250W_TEST_COMMANDS = [
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c1_on",
        [],
        [("4207", "a10121a2020100a3020101")],
        id="prime_charger_250w_usb_c1_on",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c1_off",
        [],
        [("4207", "a10121a2020100a3020100")],
        id="prime_charger_250w_usb_c1_off",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c1",
        [300],
        [("4209", "a10121a2020100a306042c01000000")],
        id="prime_charger_250w_usb_c1_timer_5m",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c1",
        [7200],
        [("4209", "a10121a2020100a30604201c000000")],
        id="prime_charger_250w_usb_c1_timer_120m",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c2_on",
        [],
        [("4207", "a10121a2020101a3020101")],
        id="prime_charger_250w_usb_c2_on",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c2_off",
        [],
        [("4207", "a10121a2020101a3020100")],
        id="prime_charger_250w_usb_c2_off",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c2",
        [300],
        [("4209", "a10121a2020101a306042c01000000")],
        id="prime_charger_250w_usb_c2_timer_5m",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c2",
        [7200],
        [("4209", "a10121a2020101a30604201c000000")],
        id="prime_charger_250w_usb_c2_timer_120m",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c3_on",
        [],
        [("4207", "a10121a2020102a3020101")],
        id="prime_charger_250w_usb_c3_on",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c3_off",
        [],
        [("4207", "a10121a2020102a3020100")],
        id="prime_charger_250w_usb_c3_off",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c3",
        [300],
        [("4209", "a10121a2020102a306042c01000000")],
        id="prime_charger_250w_usb_c3_timer_5m",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c3",
        [7200],
        [("4209", "a10121a2020102a30604201c000000")],
        id="prime_charger_250w_usb_c3_timer_120m",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c4_on",
        [],
        [("4207", "a10121a2020103a3020101")],
        id="prime_charger_250w_usb_c4_on",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_c4_off",
        [],
        [("4207", "a10121a2020103a3020100")],
        id="prime_charger_250w_usb_c4_off",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c4",
        [300],
        [("4209", "a10121a2020103a306042c01000000")],
        id="prime_charger_250w_usb_c4_timer_5m",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_c4",
        [7200],
        [("4209", "a10121a2020103a30604201c000000")],
        id="prime_charger_250w_usb_c4_timer_120m",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_a1_a2_on",
        [],
        [("4207", "a10121a2020104a3020101")],
        id="prime_charger_250w_usb_a1_a2_on",
    ),
    pytest.param(
        PrimeCharger250w,
        "turn_usb_a1_a2_off",
        [],
        [("4207", "a10121a2020104a3020100")],
        id="prime_charger_250w_usb_a1_a2_off",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_a1_a2",
        [300],
        [("4209", "a10121a2020104a306042c01000000")],
        id="prime_charger_250w_usb_a1_a2_timer_5m",
    ),
    pytest.param(
        PrimeCharger250w,
        "set_timer_usb_a1_a2",
        [7200],
        [("4209", "a10121a2020104a30604201c000000")],
        id="prime_charger_250w_usb_a1_a2_timer_120m",
    ),
]
