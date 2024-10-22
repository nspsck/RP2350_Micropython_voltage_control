# WARNING:
To overclock the rp2350, you have to unlock the voltage control in the first place. To do so:
```python
POV.enable_voltage_control()
```

This is a **PERMANENT** operation. The [documentation](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf#page=460&zoom=100,153,197) clearly states the following:
```
UNLOCK: unlocks the VREG control interface after power up
0 - Locked (default)
1 - Unlocked
**It cannot be relocked when it is unlocked.**
```

Even if you lock it again using:
```python
POV.disable_voltage_control()
```
according to the harware designers, [the regulator remains unlocked even though VREG_CTRL.UNLOCK now reads as 0.](https://github.com/raspberrypi/pico-feedback/issues/424#issuecomment-2429674640)

# RP2350_Micropython_voltage_control
This script let you control the voltage (0.85v ~ 1.30v) of any rp2350 based board using Micropython.

# Warning
**This warning is just a theory for rp2040, unsure if it is still true for rp2350.** 

Even this script only let you use voltages in a range that is specified by the documentations, there is no guarantee that operating the chip at certain voltage won't damage the board.

If you wish to operate the chip on a higher clock such as 300+ Mhz, please set the `PICO_FLASH_SPI_CLKDIV` to at least `4`. And this is how you do it:
```shell
cd micropython/lib/pico-sdk/src/boards/include/boards
vim pico.h
```
now change the `PICO_FLASH_SPI_CLKDIV 2` to `PICO_FLASH_SPI_CLKDIV 4` and quit, you can also use nano or the editor you prefer.


# Usage
The POV.py (well, not point of view, but Pico-overvoltaging) is used to control voltage and combined with OCTestMultiThread.py, you may try to overclock and test your boards. 
You can just upload the 2 files to your pico through thonny or other IDE/commands.

Examples:
1. setting voltage. Note: this chip seems to be temperature sensitive, that means, you can achieve higher frequency if you provide lower temperature.
```python
import POV
POV.enable_voltage_control()
POV.set_voltage(1.10)
"""
Returns:
True
"""
```
2. find valid inputs for `machine.freq()`.
```python
import POV
POV.find_valid_clocks(270)
"""
Output:
18 MHz is valid
20 MHz is valid
21 MHz is valid
22 MHz is valid
...
264 MHz is valid
266 MHz is valid
267 MHz is valid
268 MHz is valid
"""
```

3. run a multi-threaded test for a given frequency.
```python
import POV
POV.test(270)
"""
Output:
The test goes for 100 rounds total.
Current frequency (OC): 266MHz
Current frequency (OC): 266MHz
Round: 1, time used: 1674 ms, done by thread 0.
Current frequency: 125MHz Temperature: 36.41
Current frequency (OC): 266MHz
Round: 2, time used: 2252 ms, done by thread 1.
Current frequency: 125MHz Temperature: 39.68
Current frequency (OC): 266MHz
Round: 3, time used: 1685 ms, done by thread 0.
Current frequency: 125MHz Temperature: 41.56
...
"""
```
4. run a multi-threaded test for a given frequency non stop.
```python
import POV
POV.test_non_stop(266)
```
5. little example on testing the functionality of the built-in flash
```python
import POV, machine
POV.enable_voltage_control()
POV.set_voltage(1.30)

machine.freq(312_000_000)

f = open("some_text.txt", 'w')
f.write("some random data")
f.close()

f = open("some_text.txt")
text = f.read()
f.close()

print(text)
"""
Output:
'some random data'
"""
```
