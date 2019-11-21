import pygame
import socket

pygame.init()

broadcastIP = '172.16.1.155'           # IP address to send to, 255 in one or more positions is a broadcast / wild-card
broadcastPort = 9038   

# Setup the connection for sending on
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)       # Create the socket
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                        # Enable broadcasting (sending to many IPs based on wild-cards)
sender.bind(('0.0.0.0', 0))                                                         # Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)

def main():
   

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Joystick Testing / XBOX360 Controller")
 
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
 
    joysticks = []
    clock = pygame.time.Clock()
    keepPlaying = True

 
    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print ("Detected joystick \'",joysticks[-1].get_name(),"\'")
    while keepPlaying:
        clock.tick(60)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print ("Received event 'Quit', exiting.")
                    keepPlaying = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print ("Escape key pressed, exiting.")
                    keepPlaying = False
                elif event.type == pygame.KEYDOWN:
                    print ("Keydown,", event.key)
                elif event.type == pygame.KEYUP:
                    print ("Keyup,", event.key)
                elif event.type == pygame.MOUSEMOTION:
                    print ("Mouse movement detected.")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print ("Mouse button",event.button,"down at",pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    print ("Mouse button",event.button,"up at",pygame.mouse.get_pos())                    
                elif event.type == pygame.JOYAXISMOTION:
                    sendData = str(event.axis).encode()
                    print ("Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion.")
                    sender.sendto(sendData, (broadcastIP, broadcastPort))       
                elif event.type == pygame.JOYBUTTONDOWN:
                    sendData = str(event.button).encode()
                    print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"down.")
                    sender.sendto(sendData, (broadcastIP, broadcastPort))       
                    # if event.button == 0:
                        # background.fill((255, 0, 0))
                    # elif event.button == 1:
                        # background.fill((0, 0, 255))
                elif event.type == pygame.JOYBUTTONUP:
                    sendData = str(event.button).encode()
                    print ("Joystick \'",joysticks[event.joy].get_name(),"\' button",event.button,"up.")
                    sender.sendto(sendData, (broadcastIP, broadcastPort))       
                    # if event.button == 0:
                        # background.fill((255, 255, 255))
                    # elif event.button == 1:
                        # background.fill((255, 255, 255))
                elif event.type == pygame.JOYHATMOTION:
                    print (event.value)
                    sendData = str(event.value).encode()
                    print ("Joystick \'",joysticks[event.joy].get_name(),"\' hat",event.value," moved.")
                    sender.sendto(sendData, (broadcastIP, broadcastPort))       
                     
        screen.blit(background, (0, 0))
        pygame.display.flip()
 
main()
pygame.quit()
