# RobotTM
4WD robot on rasperry pi platform

# Sources
Socket Programming in Python: Client, Server, and Peer Examples
- https://www.pubnub.com/blog/socket-programming-in-python-client-server-p2p/

Raspberry Pi Tutorial 27 - Socket Communication 1
- https://www.youtube.com/watch?v=PYBZtV2-sLQ

Raspberry Pi Tutorial 28 - Socket Communication 2 - YouTube
- https://www.youtube.com/watch?v=xfQlPWFlSgQ

Raspberry Pi Tutorial 29 - Pratical Socket Communication
- https://www.youtube.com/watch?v=IZX7G77daG0


Basic commands: 
-------------------------------------------------------------------------------------------------
sudo crontab -e
@reboot cd /home/pi/.config && ./numlock.sh
#@reboot sh /home/pi/RobotTM/launcher.sh >/home/pi/logs/cronlog 2>&1
#@reboot sleep 40 && python /home/pi/RobotTM/tomasMotorTest.py >/home/pi/logs/c$
@reboot sleep 40 && /home/pi/neco/mjpg-streamer-master/mjpg-streamer-experiment$
------------------------------------------------------------------------------------------------
