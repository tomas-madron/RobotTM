#Ultrasonic sensor
import hcsr04, time
hcsr04.init()

#GamePad
import evdev
from evdev import InputDevice, categorize, ecodes

#cree un objet gamepad | creates object gamepad
gamepad = InputDevice('/dev/input/event0')

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


speed = 20
speedStep = 5

def driveDown():
    pz.setOutput(levyMotorL, speed)
    pz.setOutput(levyMotorR, 0)
    pz.setOutput(pravyMotorL, 0)
    pz.setOutput(pravyMotorR, speed)

def driveUp():
    pz.setOutput(levyMotorL, 0)
    pz.setOutput(levyMotorR, speed)
    pz.setOutput(pravyMotorL, speed)
    pz.setOutput(pravyMotorR, 0)

def driveLeft():
    global speed
    speed = speed + 40
    pz.setOutput (levyMotorL, 0)
    pz.setOutput (levyMotorR, speed)
    pz.setOutput (pravyMotorL, 0)
    pz.setOutput (pravyMotorR, speed)
    speed = speed - 40

def driveRight():
    global speed
    speed = speed + 40
    pz.setOutput (levyMotorL, speed)
    pz.setOutput (levyMotorR, 0)
    pz.setOutput (pravyMotorL, speed)
    pz.setOutput (pravyMotorR, 0)
    speed = speed - 40

def driveStop():
    pz.setOutput(levyMotorL, 0)
    pz.setOutput(levyMotorR, 0)
    pz.setOutput(pravyMotorL, 0)
    pz.setOutput(pravyMotorR, 0)

def speedUp():
    global speed
    global speedStep
    speed = speed + speedStep

def speedDown():
    global speed
    global speedStep
    speed = speed - speedStep

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


#define buttons
aBtn = 305
bBtn = 306
xBtn = 304
yBtn = 307
rbBtn = 309
lbBtn = 308
rtBtn = 311
ltBtn = 310
startBtn = 313
backBtn = 312


# main loop
try:
#affiche les codes interceptes |  display codes
 for event in gamepad.read_loop():
#Buttons
    if event.type == ecodes.EV_KEY:
        print(event)
        if event.value == 1:
            if event.code == startBtn:
                distance = int(hcsr04.getDistance())
                print("Distance", distance)
            elif event.code == aBtn:
                driveDown()
                print("A")
            elif event.code == bBtn:
                driveRight()
                print("B")
            elif event.code == xBtn:
                driveLeft()
                print("X")
            elif event.code == yBtn:
                driveUp()
                print("Y")
            elif event.code == lbBtn:
                speedDown()
#                driveLeft()
                print("LB")
            elif event.code == rbBtn:
                speedUp()
#                driveRight()
                print("RB")
            elif event.code == backBtn:
                print("Back")
            elif event.code == rtBtn:
#                speedUp()
                driveRight()
                print("RT")
            elif event.code == ltBtn:
#                speedDown()
                driveLeft()
                print("LT")
        elif event.value == 0:
             driveStop()
             print("Release")

 #Analog gamepad
    elif event.type == ecodes.EV_ABS:
        absevent = categorize(event)
#        print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
             if absevent.event.value == 0:
                 driveLeft()
                 print("Left")
             elif absevent.event.value == 255:
                 driveRight()
                 print("Right")
             elif (absevent.event.value <= 128):
                 driveStop()
                 print("Stop")
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
             if absevent.event.value == 0:
                driveUp()
                print("Up")
             elif absevent.event.value == 255:
                driveDown()
                print("Down")
             elif (absevent.event.value == 127):
                driveStop()
                print("Stop")
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0X":
             if absevent.event.value == -1:
                 driveLeft()
                 print("Left")
             elif absevent.event.value == 1:
                 driveRight()
                 print("Right")
             elif (absevent.event.value == 0):
                 driveStop()
                 print("Stop")
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0Y":
             if absevent.event.value == -1:
                driveUp()
                print("Up")
             elif absevent.event.value == 1:
                driveDown()
                print("Down")
             elif (absevent.event.value == 0):
                driveStop()
                print("Stop")

except KeyboardInterrupt:
    print ('Keyboard Interruption')

finally:
    driveStop()
    pz.cleanup()
    hcsr04.cleanup()
