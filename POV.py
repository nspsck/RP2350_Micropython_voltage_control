import machine
from micropython import const

"""
Useful cheat sheets:

# The POWMAN registers start at a base address of 0x40100000.
# The regulator can be directly controlled by software, but
# must first be unlocked by writing a 1 to the UNLOCK field in
# the VREG_CTRL register. Once unlocked, the regulator can be
# controlled via the VREG register.
base = const(0x40100000)
VREG_CTRL = const(base + 0x04) #[13]: UNLOCK. It cannot be relocked when it is unlocked.
VREG = const(base + 0x0c) #[8:4]: VSEL. 0.55V
 (0b00000) - 3.30V
 (0b11111)

"""

class VoltageError(Exception):
    pass


# The voltage and chip reset control address
VREG_CTRL = const(0x40100004)
VREG = const(0x4010000c)

# Possible voltage
_VREG_VOLTAGE_0_55 = const(0b00000)    #< 0_55v
_VREG_VOLTAGE_0_60 = const(0b00001)    #< 0_60v
_VREG_VOLTAGE_0_65 = const(0b00010)    #< 0_65v
_VREG_VOLTAGE_0_70 = const(0b00011)    #< 0_70v
_VREG_VOLTAGE_0_75 = const(0b00100)    #< 0_75v
_VREG_VOLTAGE_0_80 = const(0b00101)    #< 0_80v
_VREG_VOLTAGE_0_85 = const(0b00110)    #< 0_85v
_VREG_VOLTAGE_0_90 = const(0b00111)    #< 0_90v
_VREG_VOLTAGE_0_95 = const(0b01000)    #< 0_95v
_VREG_VOLTAGE_1_00 = const(0b01001)    #< 1_00v
_VREG_VOLTAGE_1_05 = const(0b01010)    #< 1_05v
_VREG_VOLTAGE_1_10 = const(0b01011)    #< 1_10v
_VREG_VOLTAGE_1_15 = const(0b01100)    #< 1_15v
_VREG_VOLTAGE_1_20 = const(0b01101)    #< 1_20v
_VREG_VOLTAGE_1_25 = const(0b01110)    #< 1_25v
_VREG_VOLTAGE_1_30 = const(0b01111)    #< 1_30v
_VREG_VOLTAGE_1_35 = const(0b10000)    #< 1_35v
_VREG_VOLTAGE_1_40 = const(0b10001)    #< 1_40v
_VREG_VOLTAGE_1_50 = const(0b10010)    #< 1_50v
_VREG_VOLTAGE_1_60 = const(0b10011)    #< 1_60v
_VREG_VOLTAGE_1_65 = const(0b10100)    #< 1_65v
_VREG_VOLTAGE_1_70 = const(0b10101)    #< 1_70v
_VREG_VOLTAGE_1_80 = const(0b10110)    #< 1_80v
_VREG_VOLTAGE_1_90 = const(0b10111)    #< 1_90v
_VREG_VOLTAGE_2_00 = const(0b11000)    #< 2_00v
_VREG_VOLTAGE_2_35 = const(0b11001)    #< 2_35v
_VREG_VOLTAGE_2_50 = const(0b11010)    #< 2_50v
_VREG_VOLTAGE_2_65 = const(0b11011)    #< 2_65v
_VREG_VOLTAGE_2_80 = const(0b11100)    #< 2_80v
_VREG_VOLTAGE_3_00 = const(0b11101)    #< 3_00v
_VREG_VOLTAGE_3_15 = const(0b11110)    #< 3_15v
_VREG_VOLTAGE_3_30 = const(0b11111)    #< 3_30v

# The masks to extract/replace the voltage settings
_CLEAN_VSEL_VALUE_MASK = const(0xfffffe0f)
_CLEAN_RAMDOM_BITS_MASK = const(0x000001f0)


def read_mem(mem_addr):
    return machine.mem32[mem_addr]


def voltage_control_bits(volt_bits):
    return (volt_bits << 5) & _CLEAN_RAMDOM_BITS_MASK


def clean_vsel_bits():
    return read_mem(VREG) & _CLEAN_VSEL_VALUE_MASK


def isclose(a, b):
    if abs(a - b) < 0.004:
        return True
    else:
        return False
    

def set_voltage_bits(volt):

    if isclose(volt, 0.85):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_0_85)

    elif isclose(volt, 0.90):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_0_90)

    elif isclose(volt, 0.95):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_0_95)

    elif isclose(volt, 1.00):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_1_00)

    elif isclose(volt, 1.05):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_1_05)

    elif isclose(volt, 1.10):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_1_10)

    elif isclose(volt, 1.15):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_1_15)

    elif isclose(volt, 1.20):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_1_20)

    elif isclose(volt, 1.25):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_1_25)

    elif isclose(volt, 1.30):
        return clean_vsel_bits() ^ voltage_control_bits(_VREG_VOLTAGE_1_30)

    else:
        raise ValueError("Unsupported inputs. Valid inputs has to be close to: 0.85 ~ 1.30, with a 0.05 increment each step. Voltage unchanged.")


def enable_voltage_control():
    try:
        # 0b0000_0000_0000_0000_0010_0000_0000_0000 = 0x00_00_20_00
        machine.mem32[VREG_CTRL] = read_mem(VREG_CTRL) | 0x5afe2000 
        return True
    except:
        return False


def disable_voltage_control():
    try:
        # 0b0000_0000_0000_0000_0010_0000_0000_0000 = 0x00_00_20_00
        machine.mem32[VREG_CTRL] = (read_mem(VREG_CTRL) - 0x2000) | 0x5afe0000 
        return True
    except:
        return False


def set_voltage(volt):
    try:
        machine.mem32[VREG] = set_voltage_bits(volt) | 0x5afe0000
        return True
    except ValueError as e:
        print("Error: ", str(e))
        return False


def test_non_stop(freq):
    if freq >= 1000:
        print("The unit used is MHz, please try again.")
        return
    elif freq <= 0:
        print("The input must be positiv")
        return
    try:
        import OCTestMultiThread as OC
        OC.run_non_stop(freq)
    except ImportError as e:
        print("ImportError", str(e))
        print("You can get the test on: ")
        

def test(freq):
    if freq >= 1000:
        print("The unit used is Mhz, please try again.")
        return
    elif freq <= 0:
        print("The input must be positiv")
        return
    try:
        import OCTestMultiThread as OC
        OC.run(freq)
    except ImportError as e:
        print(str(e))
        print("You can get the test on: https://github.com/nspsck/RP2350_Micropython_voltage_control")
        

def find_valid_clocks(limit):
    try:
        import OCTestMultiThread as OC
        OC.find_clock_freq(limit)
    except ImportError as e:
        print(str(e))
        print("You can get the test on: https://github.com/nspsck/RP2350_Micropython_voltage_control")
        
                
                
