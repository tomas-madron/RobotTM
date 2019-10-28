#GamePad
import evdev
from evdev import InputDevice, categorize, ecodes

#cree un objet gamepad | creates object gamepad
gamepad = InputDevice('/dev/input/event3')

#affiche la liste des device connectes | prints out device info at start
print(gamepad)

# Picon Zero Servo Test
# Use arrow keys to move 2 servos on outputs 0 and 1 for Pan and Tilt
# Use G and H to open and close the Gripper arm
# Press Ctrl-C to stop
#

import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

speed = 20

print ('Tests the servos by using the arrow keys to control')
print ('Press <space> key to centre')
print ('Press Ctrl-C to end')
print

# Define which pins are the servos
levyMotorL = 0
levyMotorR = 1
pravyMotorL = 2
pravyMotorR = 3

pz.init()

# Set output mode to Servo
pz.setOutputConfig(levyMotorL, 1)
pz.setOutputConfig(levyMotorR, 1)
pz.setOutputConfig(pravyMotorL, 1)
pz.setOutputConfig(pravyMotorR, 1)

levyMotorVal = 0
pravyMotorVal = 0


#step = 5

pz.setOutput (levyMotorL, levyMotorVal)
pz.setOutput (levyMotorR, levyMotorVal)
pz.setOutput (pravyMotorL, pravyMotorVal)
pz.setOutput (pravyMotorR, pravyMotorVal)

cas = 0.5 

# main loop
try:
    while True:
        keyp = readkey()
        if keyp == 'w' or ord(keyp) == 16:
            pz.setOutput (levyMotorL, speed)
            pz.setOutput (levyMotorR, 0)
            pz.setOutput (pravyMotorL, 0)
            pz.setOutput (pravyMotorR, speed)
            time.sleep(cas)
            pz.setOutput (levyMotorL, 0)
            pz.setOutput (levyMotorR, 0)
            pz.setOutput (pravyMotorL, 0)
            pz.setOutput (pravyMotorR, 0)
            print ('Up', speed)
        elif keyp == 's':
            pz.setOutput (levyMotorL, 0)
            pz.setOutput (levyMotorR, speed)
            pz.setOutput (pravyMotorL, speed)
            pz.setOutput (pravyMotorR, 0)
            time.sleep(cas)
            pz.setOutput (levyMotorL, 0)
            pz.setOutput (levyMotorR, 0)
            pz.setOutput (pravyMotorL, 0)
            pz.setOutput (pravyMotorR, 0)
            print ('Down', speed)
        elif keyp == 'a':
            speed = speed + 40
            pz.setOutput (levyMotorL, 0)
            pz.setOutput (levyMotorR, speed)
            pz.setOutput (pravyMotorL, 0)
            pz.setOutput (pravyMotorR, speed)
            time.sleep(cas)
            pz.setOutput (levyMotorL, 0)
            pz.setOutput (levyMotorR, 0)
            pz.setOutput (pravyMotorL, 0)
            pz.setOutput (pravyMotorR, 0)
            speed = speed - 40
            print ('Left', speed)
        elif keyp == 'd':
            speed = speed + 40
            pz.setOutput (levyMotorL, speed)
            pz.setOutput (levyMotorR, 0)
            pz.setOutput (pravyMotorL, speed)
            pz.setOutput (pravyMotorR, 0)
            time.sleep(cas)
            pz.setOutput (levyMotorL, 0)
            pz.setOutput (levyMotorR, 0)
            pz.setOutput (pravyMotorL, 0)
            pz.setOutput (pravyMotorR,0)
            speed = speed - 40
            print ('Right', speed)
        elif keyp == ' ':
            levyMotorVal = pravyMotorVal = speed = 0
            pz.setOutput (levyMotorL, levyMotorVal)
            pz.setOutput (levyMotorR, levyMotorVal)
            pz.setOutput (pravyMotorL, pravyMotorVal)
            pz.setOutput (pravyMotorR, pravyMotorVal)
            print ('Centre')
            print ('speed = 0')
        elif ((keyp == '.') or (keyp == '>')):
            speed = min(100, speed+10)
            print ('Speed+', speed)
        elif ((keyp == ',') or (keyp == '<')):
            speed = max (0, speed-10)
            print ('Speed-', speed)
        elif ord(keyp) == 3:
            break

except KeyboardInterrupt:
    print ('Keyboard Interruption')

finally:
    levyMotorVal = pravyMotorVal = speed = 0
    pz.setOutput (levyMotorL, levyMotorVal)
    pz.setOutput (levyMotorR, levyMotorVal)
    pz.setOutput (pravyMotorL, pravyMotorVal)
    pz.setOutput (pravyMotorR, pravyMotorVal)
    pz.cleanup()

