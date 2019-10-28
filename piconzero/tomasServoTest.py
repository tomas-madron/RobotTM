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

speed = 60

print ('Tests the servos by using the arrow keys to control')
print ('Press <space> key to centre')
print ('Press Ctrl-C to end')
print

# Define which pins are the servos
pan = 1 # swapped
tilt = 0 # swapped
rServo = 2
bServo = 5

#Set rotation
R = 0
L = 0



pz.init()

# Set output mode to Servo
pz.setOutputConfig(pan, 2)
pz.setOutputConfig(tilt, 2)
pz.setOutputConfig(rServo, 2)
pz.setOutputConfig(bServo, 2)

# Centre all servos
panVal = 90
tiltVal = 90
rServoVal = 90
bServoVal = 90

step = 5

pz.setOutput (pan, panVal)
pz.setOutput (tilt, tiltVal)
pz.setOutput (rServo, rServoVal)
pz.setOutput (bServo, bServoVal)

# main loop
try:
    while True:
        keyp = readkey()
        if keyp == 'w' or ord(keyp) == 16:
            panVal = max (0, panVal - step)
            print ('Up', panVal, 'Pin', pan)
        elif keyp == 'z' or ord(keyp) == 17:
            panVal = min (180, panVal + step)
            print ('Down', panVal, 'Pin', pan)
        elif keyp == 's' or ord(keyp) == 18:
            tiltVal = max (0, tiltVal - step)
            print ('Right', tiltVal, 'Pin', tilt)
        elif keyp == 'a' or ord(keyp) == 19:
            tiltVal = min (180, tiltVal + step)
            print ('Left', tiltVal, 'Pin', tilt)
        elif keyp == 'k':
            rServoVal = max (0, rServoVal - step)
            print ('Right', rServoVal, 'Pin', rServo)            
        elif keyp == 'l':
            rServoVal = max (0, rServoVal + step)
            print ('Left', rServoVal, 'Pin', rServo)            
        elif keyp == 'g':
            bServoVal = max (0, bServoVal - step)
            print ('Right', bServoVal)
        elif keyp == 'h':
            bServoVal = min (180, bServoVal + step)
            print ('Left', bServoVal)
        elif keyp == ' ':
            panVal = tiltVal = rServoVal = bServoVal = 90
            speed = 0
            if L == 1:
                pz.spinLeft(speed)
            if R == 1:
                pz.spinRight(speed)     
            print ('Centre')
        elif keyp == 'o':
            tiltVal = max (0, tiltVal + step)
            rServoVal = max (0, rServoVal + step)
            bServoVal = max (0, bServoVal + step)
            print ('Left', tiltVal, 'Pin', bServo)
            print ('Left', rServoVal, 'Pin', rServo)
            print ('Left', bServoVal, 'Pin', bServo)            
        elif keyp == 'p':
            tiltVal = max (0, tiltVal - step)
            rServoVal = max (0, rServoVal - step)
            bServoVal = max (0, bServoVal - step)
            print ('Right', tiltVal, 'Pin', tilt)
            print ('Right', rServoVal, 'Pin', rServo)
            print ('Right', bServoVal, 'Pin', bServo)
        elif keyp == 'r':
            pz.spinRight(speed)
            L = 0
            R = 1
            print ('Spin Motor Right', speed)
        elif keyp == 't':
            pz.spinLeft(speed)
            R = 0
            L = 1
            print ('Spin Motor Left', speed)
        elif ((keyp == '.') or (keyp == '>')):            
            speed = min(100, speed+10)
            if L == 1:
                pz.spinLeft(speed)
            if R == 1:
                pz.spinRight(speed)       
            print ('Speed+', speed)
        elif ((keyp == ',') or (keyp == '<')):
            speed = max (0, speed-10)
            if L == 1:
                pz.spinLeft(speed)
            if R == 1:
                pz.spinRight(speed)                
            print ('Speed-', speed)            
        elif ord(keyp) == 3:
            break
        
        
        pz.setOutput (pan, panVal)
        pz.setOutput (tilt, tiltVal)
        pz.setOutput (rServo, rServoVal)
        pz.setOutput (bServo, bServoVal)
        

except KeyboardInterrupt:
    print

finally:
    panVal = tiltVal = rServoVal = bServoVal = 90
    pz.cleanup()
    
