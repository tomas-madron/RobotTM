#Ultrasonic sensor
import hcsr04, time
hcsr04.init()

def getDistance():
    return int(hcsr04.getDistance()-6)

def displayDistance():
    print("Distance:", getDistance())

def displaySpeed():
    print("Speed:",speed)


from evdev import InputDevice, categorize, ecodes, KeyEvent

def find_controller():
    event0 = InputDevice('/dev/input/event0')
    event1 = InputDevice('/dev/input/event1')
    controller_list = ["Logitech Logitech Cordless RumblePad 2"]
    for controller in controller_list:
        if event0.name == controller:
            gamepad = event0
        elif event1.name == controller:
            gamepad = event1
        else:
            print("controller not found")
    return gamepad

gamepad = find_controller()


import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios


speed = 20
speedStep = 5


def driveUp(speed):
    pz.setOutput(levyMotorL, speed)
    pz.setOutput(levyMotorR, 0)
    pz.setOutput(pravyMotorL, 0)
    pz.setOutput(pravyMotorR, speed)

def driveDown(speed):
    pz.setOutput(levyMotorL, 0)
    pz.setOutput(levyMotorR, speed)
    pz.setOutput(pravyMotorL, speed)
    pz.setOutput(pravyMotorR, 0)

def driveLeft(speed):
    pz.setOutput (levyMotorL, 0)
    pz.setOutput (levyMotorR, speed)
    pz.setOutput (pravyMotorL, 0)
    pz.setOutput (pravyMotorR, speed)

def driveRight(speed):
    pz.setOutput (levyMotorL, speed)
    pz.setOutput (levyMotorR, 0)
    pz.setOutput (pravyMotorL, speed)
    pz.setOutput (pravyMotorR, 0)

def driveStop():
    pz.setOutput(levyMotorL, 0)
    pz.setOutput(levyMotorR, 0)
    pz.setOutput(pravyMotorL, 0)
    pz.setOutput(pravyMotorR, 0)

def speedUpdate(speedVal, speedStep):
    global speed
    speed = speedVal + speedStep    

    if speed > 100:
        speed = 100
    elif speed < 0:
        speed = 0

    if speedStep > 0:        
        print ("Speed+", speed)
    elif speedStep < 0:
        print ("Speed-", speed)
    else:
        print("Speed", speed)   


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
    while True:        
        for event in gamepad.read_loop():
            #Buttons
            if event.type == ecodes.EV_KEY:
                #print(event)
                if event.value == 1:
                    if event.code == startBtn:
                        print ("fds")                    
                    elif event.code == aBtn:
                        driveDown(speed)
                        displaySpeed()
                        displayDistance()
                        print("A")
                    elif event.code == bBtn:
                        driveRight(60)
                        print("B")
                    elif event.code == xBtn:
                        driveLeft(60)
                        print("X")
                    elif event.code == yBtn:
                        driveUp(speed)
                        print("Y")
                    elif event.code == lbBtn:
                        speedUpdate(speed, -speedStep)                        
                        print("LB")
                    elif event.code == rbBtn:
                        speedUpdate(speed, speedStep)
                        print("RB")
                    elif event.code == backBtn:
                        print("Back")
                    elif event.code == rtBtn:                        
                        driveRight(60)
                        print("RT")
                    elif event.code == ltBtn:
                        driveLeft(60)
                        print("LT")
                elif event.value == 0:
                        driveStop()
                        print("Release")
             #Analog gamepad
            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                #print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
                if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
                    a = absevent.event.value
                    print(a)
                    speedValue = abs(a-128)                    
                  #  if a >= 0 and a <= 127:
                       # speed = speedValue
                   # elif a >= 129 and a <= 255:
                        #speed = speedValue
                  #  else:
                     #   print("STOP X")
                      #  speedValue = 0
                       # speed = 0                    
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
                    a = absevent.event.value
                    print(a)
                    speedValue = abs(a-128)                    
                #    if a >= 0 and a <= 127:
                      #  speed = speedValue
                  #  elif a >= 129 and a <= 255:
                       # speed = speedValue
                 #   else:
                   #     print("STOP Y")
                       # speedValue = 0
                       # speed = 0
                        
                        
                        
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0X":
                    if absevent.event.value == -1:
                        if speed < 60:                            
                            driveLeft(60)
                        else:
                            driveLeft(speed)
                        print("Left")
                    elif absevent.event.value == 1:
                        if speed < 60:
                            driveRight(60)
                        else:
                            driveRight(speed)
                        print("Right")
                    elif (absevent.event.value == 0):
                        driveRight(0)
                        print("Stop")
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0Y":                   
                    if absevent.event.value == -1:
                        driveUp(speed)                        
                        print("Up")
                    elif absevent.event.value == 1:
                        driveDown(speed)                        
                        print("Down")
                    elif (absevent.event.value == 0):
                        driveDown(0)
                        print("Stop")
                    
except KeyboardInterrupt:
    print ('Keyboard Interruption')

finally:
    driveStop()
    pz.cleanup()
    hcsr04.cleanup()
