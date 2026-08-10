"""F2600 power station device tests.

.. moduleauthor:: Harvey Lelliott (flip-dots) <harveylelliott@duck.com>

"""
import pytest

from SolixBLE.devices.f2600 import F2600
from SolixBLE.states import DisplayTimeout, LightStatus

########################
# Test device commands #
########################

# These tests are for sending commands to the device and making sure the
# correct calls are made to the command sending functions and errors are
# raised where appropriate. See test_send_command() in test_commands.py.

F2600_TEST_COMMANDS = [
    pytest.param(
        F2600,
        "turn_ac_on",
        [],
        [("404a", "a10121a2020101")],
        id="f2600_ac_on",
    ),
    pytest.param(
        F2600,
        "turn_ac_off",
        [],
        [("404a", "a10121a2020100")],
        id="f2600_ac_off",
    ),
    pytest.param(
        F2600,
        "turn_dc_on",
        [],
        [("404b", "a10121a2020101")],
        id="f2600_dc_on",
    ),
    pytest.param(
        F2600,
        "turn_dc_off",
        [],
        [("404b", "a10121a2020100")],
        id="f2600_dc_off",
    ),
    pytest.param(
        F2600,
        "set_ac_timer",
        [300],
        [("4042", "a10121a205022c010000")],
        id="f2600_ac_timer_5m",
    ),
    pytest.param(
        F2600,
        "set_dc_timer",
        [300],
        [("4043", "a10121a205022c010000")],
        id="f2600_dc_timer_5m",
    ),
    pytest.param(
        F2600,
        "set_ac_timer",
        [10],
        [("4042", "a10121a205020a000000")],
        id="f2600_ac_timer_10s",
    ),
    pytest.param(
        F2600,
        "set_dc_timer",
        [10],
        [("4043", "a10121a205020a000000")],
        id="f2600_dc_timer_10s",
    ),
    pytest.param(
        F2600,
        "set_light_mode",
        [LightStatus.LOW],
        [("404f", "a10121a2020101")],
        id="f2600_light_low",
    ),
    pytest.param(
        F2600,
        "set_light_mode",
        [LightStatus.MEDIUM],
        [("404f", "a10121a2020102")],
        id="f2600_light_med",
    ),
    pytest.param(
        F2600,
        "set_light_mode",
        [LightStatus.HIGH],
        [("404f", "a10121a2020103")],
        id="f2600_light_high",
    ),
    pytest.param(
        F2600,
        "set_light_mode",
        [LightStatus.SOS],
        [("404f", "a10121a2020104")],
        id="f2600_light_sos",
    ),
    pytest.param(
        F2600,
        "set_light_mode",
        [LightStatus.UNKNOWN],
        ValueError,
        id="f2600_light_unknown",
    ),
    pytest.param(
        F2600,
        "set_display_mode",
        [LightStatus.LOW],
        [("404c", "a10121a2020101")],
        id="f2600_display_low",
    ),
    pytest.param(
        F2600,
        "set_display_mode",
        [LightStatus.MEDIUM],
        [("404c", "a10121a2020102")],
        id="f2600_display_med",
    ),
    pytest.param(
        F2600,
        "set_display_mode",
        [LightStatus.HIGH],
        [("404c", "a10121a2020103")],
        id="f2600_display_high",
    ),
    pytest.param(
        F2600,
        "set_display_mode",
        [LightStatus.SOS],
        ValueError,
        id="f2600_display_sos",
    ),
    pytest.param(
        F2600,
        "set_display_mode",
        [LightStatus.UNKNOWN],
        ValueError,
        id="f2600_display_unknown",
    ),
    pytest.param(
        F2600,
        "set_display_timeout",
        [DisplayTimeout.S20],
        [("4046", "a10121a203021400")],
        id="f2600_display_timeout_20s",
    ),
    pytest.param(
        F2600,
        "set_display_timeout",
        [DisplayTimeout.S1800],
        [("4046", "a10121a203020807")],
        id="f2600_display_timeout_30m",
    ),
    pytest.param(
        F2600,
        "set_display_timeout",
        [DisplayTimeout.UNKNOWN],
        ValueError,
        id="f2600_display_timeout_unknown",
    ),
    pytest.param(
        F2600,
        "turn_display_on",
        [],
        [("4052", "a10121a2020101")],
        id="f2600_display_on",
    ),
    pytest.param(
        F2600,
        "turn_display_off",
        [],
        [("4052", "a10121a2020100")],
        id="f2600_display_off",
    ),
    pytest.param(
        F2600,
        "turn_power_saving_mode_on",
        [],
        [("404e", "a10121a2020101")],
        id="f2600_power_saving_on",
    ),
    pytest.param(
        F2600,
        "turn_power_saving_mode_off",
        [],
        [("404e", "a10121a2020100")],
        id="f2600_power_saving_off",
    ),
    pytest.param(
        F2600,
        "set_ac_charging_power",
        [150],
        [("4044", "a10121a203029600")],
        id="f2600_ac_charge_150w",
    ),
    pytest.param(
        F2600,
        "set_ac_charging_power",
        [700],
        [("4044", "a10121a20302bc02")],
        id="f2600_ac_charge_700w",
    ),
    pytest.param(
        F2600,
        "set_ac_charging_power",
        [50],
        ValueError,
        id="f2600_ac_charge_50w",
    ),
    pytest.param(
        F2600,
        "set_ac_charging_power",
        [1500],
        ValueError,
        id="f2600_ac_charge_1500w",
    ),
]


####################################
# Test device commands & responses #
####################################

# These tests are for sending commands to the device and making sure the correct
# calls are made to the command sending functions, that the response is handled
# appropriately, the correct value is returned, and errors are raised where
# appropriate. See test_send_command_response() in test_commands.py.


F2600_TEST_COMMANDS_RESPONSES = [
    pytest.param(
        F2600,
        "get_status_update",
        [],
        [("4040", "a10121")],
        [("03010f", "c840", "00a10131a2050300000000a3050300000000a403020900a50302a405a603021801a703020000a803020000a903020000aa03020000ab03020000ac03020000ad03020000ae03020000af0302a405b003021801b103020000b203020000b303025a01b403022e01b503027400b603026c00b703020000b803027500b903020000ba03025a01bb03020100bc020102bd020122be020100bf020102c0020100c1020140c2020100c3020164c4020100c5020100c6020100c7020100c8020100c9020100ca020100cb020100cc020100cd020100ce020100cf020100d01100415a56334e4d30463038373030343131d10302a005d203020000d303021400d403023c00d503020000d603020000d7020101d8020100d9020103da02013cdb020100dc020100dd020101de020100f815040000000001000000000000000000000000000000fd0a0041313738315f354168fe0503372b136a")],  # noqa: E501
        {'a1': b'1', 'a2': b'\x03\x00\x00\x00\x00', 'a3': b'\x03\x00\x00\x00\x00', 'a4': b'\x02\t\x00', 'a5': b'\x02\xa4\x05', 'a6': b'\x02\x18\x01', 'a7': b'\x02\x00\x00', 'a8': b'\x02\x00\x00', 'a9': b'\x02\x00\x00', 'aa': b'\x02\x00\x00', 'ab': b'\x02\x00\x00', 'ac': b'\x02\x00\x00', 'ad': b'\x02\x00\x00', 'ae': b'\x02\x00\x00', 'af': b'\x02\xa4\x05', 'b0': b'\x02\x18\x01', 'b1': b'\x02\x00\x00', 'b2': b'\x02\x00\x00', 'b3': b'\x02Z\x01', 'b4': b'\x02.\x01', 'b5': b'\x02t\x00', 'b6': b'\x02l\x00', 'b7': b'\x02\x00\x00', 'b8': b'\x02u\x00', 'b9': b'\x02\x00\x00', 'ba': b'\x02Z\x01', 'bb': b'\x02\x01\x00', 'bc': b'\x01\x02', 'bd': b'\x01"', 'be': b'\x01\x00', 'bf': b'\x01\x02', 'c0': b'\x01\x00', 'c1': b'\x01@', 'c2': b'\x01\x00', 'c3': b'\x01d', 'c4': b'\x01\x00', 'c5': b'\x01\x00', 'c6': b'\x01\x00', 'c7': b'\x01\x00', 'c8': b'\x01\x00', 'c9': b'\x01\x00', 'ca': b'\x01\x00', 'cb': b'\x01\x00', 'cc': b'\x01\x00', 'cd': b'\x01\x00', 'ce': b'\x01\x00', 'cf': b'\x01\x00', 'd0': b'\x00AZV3NM0F08700411', 'd1': b'\x02\xa0\x05', 'd2': b'\x02\x00\x00', 'd3': b'\x02\x14\x00', 'd4': b'\x02<\x00', 'd5': b'\x02\x00\x00', 'd6': b'\x02\x00\x00', 'd7': b'\x01\x01', 'd8': b'\x01\x00', 'd9': b'\x01\x03', 'da': b'\x01<', 'db': b'\x01\x00', 'dc': b'\x01\x00', 'dd': b'\x01\x01', 'de': b'\x01\x00', 'f8': b'\x04\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'fd': b'\x00A1781_5Ah', 'fe': b'\x037+\x13j'},  # noqa: E501, Q000
        id="f2600_status_update",
    ),
    pytest.param(
        F2600,
        "get_status_update",
        [],
        [("4040", "a10121")],
        [("03010f", "c840", None)],
        TimeoutError,
        id="f2600_status_update_error",
    ),
]
