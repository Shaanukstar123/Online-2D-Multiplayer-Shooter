'''Problems that arose: Cannot pickle an image file. Fix: made Surface (self.anime) into string and saved surface data in variable 'image'''
import pygame
from Network import Network
from player import *
from MainMenu import menu
#import os
#import subprocess
import socket
from _thread import *

def main_game():
    width = 1300
    height = 700
    backgrounds=[]

    anime1=pygame.image.load("sprites/Background anime/frame0.gif")
    anime2=pygame.image.load("sprites/Background anime/frame1.gif")
    anime3=pygame.image.load("sprites/Background anime/frame2.gif")
    anime4=pygame.image.load("sprites/Background anime/frame3.gif")
    anime5=pygame.image.load("sprites/Background anime/frame4.gif")
    anime6=pygame.image.load("sprites/Background anime/frame5.gif")
    anime7=pygame.image.load("sprites/Background anime/frame6.gif")
    anime8=pygame.image.load("sprites/Background anime/frame7.gif")

    backgrounds.append(pygame.transform.scale(anime1,(width,height)))
    backgrounds.append(pygame.transform.scale(anime2,(width,height)))
    backgrounds.append(pygame.transform.scale(anime3,(width,height)))
    backgrounds.append(pygame.transform.scale(anime4,(width,height)))
    backgrounds.append(pygame.transform.scale(anime5,(width,height)))
    backgrounds.append(pygame.transform.scale(anime6,(width,height)))
    backgrounds.append(pygame.transform.scale(anime7,(width,height)))
    backgrounds.append(pygame.transform.scale(anime8,(width,height)))

    gameDisplay = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Client")

    def redraw_window(gameDisplay,player, player2,background_index):
        background_index=int(background_index)
        gameDisplay.fill((255,255,255))
        gameDisplay.blit(backgrounds[background_index],(0,0))

        playerObj = player['player']
        secondPlayerObj = player2['player']
        players=[playerObj, secondPlayerObj]

        playerObj.draw(gameDisplay)
        secondPlayerObj.draw(gameDisplay)

        for bullet in playerObj.projectiles:
            bullet.collides(players)
            if bullet.should_remove():
                playerObj.remove_projectile(bullet)
                continue

            bullet.draw_bullet(gameDisplay,players)

        for bullet in player2['player'].projectiles:
            bullet.collides(players)
            if bullet.should_remove():
                secondPlayerObj.remove_projectile(bullet)
                continue
            bullet.draw_bullet(gameDisplay,players)
        #pygame.display.update()
    def endgame():
        print("EndGame")
        gameDisplay.fill((255,255,255))
        start_check()
        '''Change this to return to main menu'''
    def error():
        print("Cannot connect to server")
        gameDisplay.fill((255,255,255))
        start_check()

    def main():
        music=pygame.mixer.music.load("power_music.wav")
        pygame.mixer.music.play(-1)
        host=socket.gethostname()
        IP = socket.gethostbyname(host)
        wall1=Map(400,400,300,100)
        run = True
        try:
            n = Network(IP)
            p= n.getP()
            print(p)
            print(p['player'])
            playerObj = p['player']

        except:
            print("Cannot connect to server")
            error()

        clock = pygame.time.Clock()
        background_index=-1
        movement=True
        while run:
            if background_index>6:
                background_index=0
            else:
                background_index+=0.15
            p2 = n.send(p)
            secondPlayerObj=p2['player']
            #secondPlayerObj = p2['player']
            #wall2=p2['wall']
            events=pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            if playerObj.dead==True or secondPlayerObj.dead==True :
                endgame()
            '''p['player'] = playerObj
            wall1=p['wall']
            wall2=p2['wall']'''
            #print("{},{}".format(playerObj.x,playerObj.y))
            print(playerObj.x)

            #if wall.collision(playerObj) ==True:
                #print("stop")

            #if wall2.collision(secondPlayerObj)==True:
                #print("stop2")

            playerObj.move(events,wall1)
            redraw_window(gameDisplay,p, p2,background_index)
            clock.tick(60)
            pygame.display.update()

    main()

'''def threaded_player():
    while True:
        print("Hello")
start_new_thread(threaded_player,())'''
def start_check():
    message=menu(False)
    if message==True:
        main_game()
start_check()
''' command="Server1.py"
    os.system(command)
    subprocess.Popen(command)'''
