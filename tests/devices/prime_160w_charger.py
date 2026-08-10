"""Anker Prime 160w charger tests.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""
import pytest

from SolixBLE.devices.prime_charger_160w import PrimeCharger160w

########################
# Test device commands #
########################

# These tests are for sending commands to the device and making sure the
# correct calls are made to the command sending functions and errors are
# raised where appropriate. See test_send_command() in test_commands.py.

PRIME_CHARGER_160W_TEST_COMMANDS = [
    pytest.param(
        PrimeCharger160w,
        "turn_usb_c1_on",
        [],
        [("4207", "a10121a2020100a3020101")],
        id="prime_charger_160w_usb_c1_on",
    ),
    pytest.param(
        PrimeCharger160w,
        "turn_usb_c1_off",
        [],
        [("4207", "a10121a2020100a3020100")],
        id="prime_charger_160w_usb_c1_off",
    ),
    pytest.param(
        PrimeCharger160w,
        "set_timer_usb_c1",
        [300],
        [("4209", "a10121a2020100a305042c010000")],
        id="prime_charger_160w_usb_c1_timer_5m",
    ),
    pytest.param(
        PrimeCharger160w,
        "set_timer_usb_c1",
        [7200],
        [("4209", "a10121a2020100a30504201c0000")],
        id="prime_charger_160w_usb_c1_timer_120m",
    ),
    pytest.param(
        PrimeCharger160w,
        "turn_usb_c2_on",
        [],
        [("4207", "a10121a2020101a3020101")],
        id="prime_charger_160w_usb_c2_on",
    ),
    pytest.param(
        PrimeCharger160w,
        "turn_usb_c2_off",
        [],
        [("4207", "a10121a2020101a3020100")],
        id="prime_charger_160w_usb_c2_off",
    ),
    pytest.param(
        PrimeCharger160w,
        "set_timer_usb_c2",
        [300],
        [("4209", "a10121a2020101a305042c010000")],
        id="prime_charger_160w_usb_c2_timer_5m",
    ),
    pytest.param(
        PrimeCharger160w,
        "set_timer_usb_c2",
        [7200],
        [("4209", "a10121a2020101a30504201c0000")],
        id="prime_charger_160w_usb_c2_timer_120m",
    ),
    pytest.param(
        PrimeCharger160w,
        "turn_usb_c3_on",
        [],
        [("4207", "a10121a2020102a3020101")],
        id="prime_charger_160w_usb_c3_on",
    ),
    pytest.param(
        PrimeCharger160w,
        "turn_usb_c3_off",
        [],
        [("4207", "a10121a2020102a3020100")],
        id="prime_charger_160w_usb_c3_off",
    ),
    pytest.param(
        PrimeCharger160w,
        "set_timer_usb_c3",
        [300],
        [("4209", "a10121a2020102a305042c010000")],
        id="prime_charger_160w_usb_c3_timer_5m",
    ),
    pytest.param(
        PrimeCharger160w,
        "set_timer_usb_c3",
        [7200],
        [("4209", "a10121a2020102a30504201c0000")],
        id="prime_charger_160w_usb_c3_timer_120m",
    ),
]
