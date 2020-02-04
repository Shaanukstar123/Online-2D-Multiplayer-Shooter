import pygame
import os
import subprocess
from tkinter import*
import sqlite3
from highscores import *
from _thread import *
from Server1 import *
import socket
from socket import timeout as TimeoutError

def menu(start):
    pygame.init()

    width = 900
    height = 550
    display = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    white=(255, 255, 255)
    black=(0, 0, 0)
    brown=(150,75,0)
    red=(255, 0, 0)
    yellow=(255, 255, 0)
    blue=(0, 0, 255)
    green=(0, 255, 0)
    grey=(128, 128, 128)

    music=pygame.mixer.music.load("fire.wav")
    pygame.mixer.music.play(-1)

    backgrounds=[]

    anime1=pygame.image.load("Images/tmp-0.gif")
    anime2=pygame.image.load("Images/tmp-1.gif")
    anime3=pygame.image.load("Images/tmp-2.gif")
    anime4=pygame.image.load("Images/tmp-3.gif")
    anime5=pygame.image.load("Images/tmp-4.gif")
    anime6=pygame.image.load("Images/tmp-5.gif")
    anime7=pygame.image.load("Images/tmp-6.gif")
    anime8=pygame.image.load("Images/tmp-7.gif")

    backgrounds.append(pygame.transform.scale(anime1,(width,height)))
    backgrounds.append(pygame.transform.scale(anime2,(width,height)))
    backgrounds.append(pygame.transform.scale(anime3,(width,height)))
    backgrounds.append(pygame.transform.scale(anime4,(width,height)))
    backgrounds.append(pygame.transform.scale(anime5,(width,height)))
    backgrounds.append(pygame.transform.scale(anime6,(width,height)))
    backgrounds.append(pygame.transform.scale(anime7,(width,height)))
    backgrounds.append(pygame.transform.scale(anime8,(width,height)))

    def process_text(message, font, size, color):

        new_font = pygame.font.Font(font, size)
        edited = new_font.render(message, 0, color)

        return edited


    font = "Images/arcade.TTF"
    n=0


    def main_menu(n,start):
        multicast_group = '224.3.29.71'
        server_address = ('', 10000)

        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        sock.bind(server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        global servers
        servers = {}
        server_started = False

        tracker=["start","Create Server","instructions","highscores","quit"]
        pointer=0

        menu=True
        selected="start"
        start_scan = False
        while menu:
            if n>6:
              n=0
            else:
              n+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP:
                        selected="start"
                        if pointer>0:
                            pointer-=1
                        selected=tracker[pointer]

                    if event.key==pygame.K_DOWN:
                        if pointer<4:
                            pointer+=1
                        selected=tracker[pointer]

                    if event.key==pygame.K_RETURN:
                        if selected=="quit":
                            pygame.quit()
                            quit()
                        if selected =="start":
                            address_of_server=run_scan(multicast_group,server_address,group,mreq,sock)
                            print("start")
                            start_scan=True
                            if len(servers)>0:
                                print("Servers: ")
                                for server in servers:
                                    print(server)
                                selected = input("Chose a server: ")
                                if selected in servers:
                                    start=True
                                    return [start,servers[selected]]
                                else:
                                    print(servers)
                                    print("Server does not exists")
                            else:
                                print("No servers running")
                        if selected == "highscores":
                            start_new_thread(run_table,())

                        if selected =="Create Server":
                            #name=input("Server name: ")
                            name = input("Server Name: ")
                            if server_started == False:
                                server_started = True
                                start_new_thread(run,(name,))
                            else:
                                print("Server already started")

            display.fill(grey)
            display.blit(backgrounds[n],(0,0))
            font_size=32
            #title=process_text("Some shooting game", font, 70, yellow)
            if selected=="start":
                text_start=process_text("JOIN GAME", font, font_size, white)
            else:
                text_start = process_text("JOIN GAME", font, font_size, yellow)
            if selected=="quit":
                text_quit=process_text("QUIT", font, font_size, white)
            else:
                text_quit = process_text("QUIT", font, font_size, yellow)
            if selected == "highscores":
                text_highscores=process_text("HIGHSCORES", font, font_size, white)

            else:
                text_highscores =process_text("HIGHSCORES", font, font_size, yellow)

            if selected =="instructions":
              text_instructions = process_text("INSTRUCTIONS",font,font_size,white)
            else:
              text_instructions = process_text("INSTRUCTIONS",font,font_size,yellow)

            if selected == "Create Server":
                 text_createserver = process_text("CREATE  SERVER",font,font_size,white)
            else:
                text_createserver = process_text("CREATE  SERVER",font,font_size,yellow)


            #title_rect=title.get_rect()
            start_rect=text_start.get_rect()
            quit_rect=text_quit.get_rect()
            highscores_rect=text_highscores.get_rect()
            instruct_rect=text_instructions.get_rect()
            create_rect = text_createserver.get_rect()

            pos=width/2
            #display.blit(title, (450 - (title_rect[2]/2), 80))
            display.blit(text_start, (pos - (start_rect[2]/2), 80))
            display.blit(text_createserver,(pos - (create_rect[2]/2),120))
            display.blit(text_instructions, ( pos- (instruct_rect[2]/2), 160))
            display.blit(text_highscores, (pos - (highscores_rect[2]/2),200))
            display.blit(text_quit, (pos -(quit_rect[2]/2),240))
            pygame.display.update()
            clock.tick(5)
            pygame.display.set_caption("Main Menu")

            #return start

            #def return_start(start):
                #return start

    return main_menu(n,start)
    pygame.quit()
    #menu(start)
    #quit()
#def server_scan():

    # Receive/respond loop
def run_scan(multicast_group,server_address,group,mreq,sock):
    data = []
    address = None
    sock.settimeout(5)
    print (sys.stderr, '\nwaiting to receive message')
    try:
        data, address = sock.recvfrom(1024)
        #print (sys.stderr, 'received %s bytes from %s' % (len(data), address))
        #print (sys.stderr, data)
        data = data.decode("utf-8")
        servers.update({data:address[0]})

        #print (sys.stderr, 'sending acknowledgement to', address)
        sock.sendto('ack'.encode("utf-8"), address)
    except TimeoutError:
        print("No servers found")
        end = input("Enter c to cancel search ")
