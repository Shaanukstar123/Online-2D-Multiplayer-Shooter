'''Problems that arose: Cannot pickle an image file. Fix: made Surface (self.anime) into string and saved surface data in variable 'image'''
import pygame
from Network import Network
from player import *
from MainMenu import menu
import time
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
    #pygame.display.toggle_fullscreen()

    def redraw_window(gameDisplay,player, player2,background_index,wall):
        playerObj = player['player']
        secondPlayerObj = player2['player']
        players=[playerObj, secondPlayerObj]
        #if (pygame.sprite.collide_rect(playerObj.sprite,wall)):
            #print("Success!")
        background_index=int(background_index)
        gameDisplay.fill((255,255,255))
        gameDisplay.blit(backgrounds[background_index],(0,0))

        playerObj = player['player']
        secondPlayerObj = player2['player']
        players=[playerObj, secondPlayerObj]

        playerObj.draw(gameDisplay,wall)
        secondPlayerObj.draw(gameDisplay,wall)

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
    '''def threaded_timer(count,gameDisplay,clock):
        #font = pygame.font.Font("Images/arcade.TTF", 35)
        colour=(255,255,255)
        count=100
        print("hello")
        font = pygame.font.Font("Images/arcade.TTF", 35)
        while True:
            #display_time(count,gameDisplay)
            colour=(255,255,255)
            timer = font.render(str(int(count)), 0, colour)
            #gameDisplay.blit(timer, (300 - (200), 20))
            if count<1:
                print("Done")
            else:
                #time.sleep(1)
                gameDisplay.blit(timer, (width/2 - (200), 20))
                count-=(1/65)
                print(int(count))
                clock.tick(65)
            #pygame.display.update()'''


    '''def display_time(count,gameDisplay):
        colour=(255,255,255)
        font = pygame.font.Font("Images/arcade.TTF", 35)
        timer = font.render(str(count), 0, colour)
        while True:
            gameDisplay.blit(timer, (300 - (200), 20))
            time.sleep(1)
            break'''

    def endgame(player,gameDisplay):
        colour=(0,0,0)
        yellow=(255,255,0)
        green=(0,255,0)
        blue=(0, 0, 255)
        clock = pygame.time.Clock()
        count=0
        while True:
            if count==12:
                start_check()
            count+=1
            gameDisplay.fill((255,255,255))
            new_font = pygame.font.Font("Images/arcade.TTF", 80)
            player_font=pygame.font.Font("Images/arcade.TTF", 60)

            game_over = new_font.render(str("GAME OVER"), 0, colour)
            player2=player_font.render(str("Green   wins!"), 0, green)
            player1=player_font.render(str("Yellow   wins!"), 0, yellow)
            gameDisplay.blit(game_over, ((width/2) - (200), (height/2)))
            tie =player_font.render(str("Match Tied"), 0, blue)
            pygame.mixer.music.stop()
            print("Game Over")
            if player.player==1:
                if player.dead==True:
                    gameDisplay.blit(player2, ((width/2) - (200), (height/2+100)))
                    print("player 2 wins!")
                else:
                    print("player 1 wins!")
                    gameDisplay.blit(player1, ((width/2) - (200), (height/2+100)))
            elif player.player ==2:
                if player.dead==True:
                    print("player 1 wins!")
                    gameDisplay.blit(player1, ((width/2) - (200), (height/2+100)))
                else:
                    print("player 2 wins!")
                    gameDisplay.blit(player2, ((width/2) - (200), (height/2+100)))
            else:
                gameDisplay.blit(tie, ((width/2) - (200), (height/2+100)))

            clock.tick(2)
            pygame.display.update()
        #gameDisplay.fill((255,255,255))
        #start_check()

    def threaded_collectables(items,gameDisplay,player,wall):
        for i in items:
            i.display_items(gameDisplay)
            random_time=random.randint(0,15)
            i.generate(wall)
            time_end = time.time() + 10
            while time.time() < time_end:
                i.display_items(gameDisplay)
                #print("item Displayed!")
                if i.x==player.x:
                    print("Object Collected")

        #'''Change this to return to main menu'''
    def error():
        print("Cannot connect to server")
        gameDisplay.fill((255,255,255))
        start_check()

    def main():
        stopclock=Timer(100)
        new_font = pygame.font.Font("Images/arcade.TTF", 50)
        count=100
        timer=False
        music=pygame.mixer.music.load("power_music.wav")
        pygame.mixer.music.play(-1)
        host=socket.gethostname()
        IP = socket.gethostbyname(host)
        wall1=Map(400,400,300,100,"wall1.png")
        wall_rect = pygame.Rect(wall1.x,wall1.y,228,44)
        health_item=Collectables(1,"sprite.png")
        random_list=[]
        item_list=[health_item]
        #for i in range(0,count+1):
            #random_list.append(i)
        #print(random_list)
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
        start_new_thread(threaded_collectables,((item_list,gameDisplay,playerObj,wall_rect)))
        #timer=False
        while run:
            if background_index>6:
                background_index=0
            else:
                background_index+=0.15
            p2 = n.send(p)
            secondPlayerObj=p2['player']
            #secondPlayerObj = p2['player']
            #wall2=p2['wall']
            '''if timer==False:
                if secondPlayerObj.x!=100:
                    start_new_thread(threaded_timer,((100,gameDisplay,clock)))
                    timer=True'''
            events=pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            if playerObj.dead==True or secondPlayerObj.dead==True :
                run=False
                endgame(playerObj,gameDisplay)
            '''p['player'] = playerObj
            wall1=p['wall']
            wall2=p2['wall']'''
            #print("{},{}".format(playerObj.x,playerObj.y))
            #print(playerObj.x)
            #if wall.collision(playerObj) ==True:
                #print("stop")
            #if wall2.collision(secondPlayerObj)==True:
                #print("stop2")

            playerObj.move(events,wall1)
            redraw_window(gameDisplay,p, p2,background_index,wall1)
            stopclock.show_time(secondPlayerObj,gameDisplay)
            #if stopclock.time
            #health_item.generate(wall_rect)
            #health_item.display_items(gameDisplay,stopclock.time)
            if stopclock.end==True:
                run=False
                endgame(playerObj,gameDisplay)
            clock.tick(60)
            pygame.display.update()


    main()

def start_check():
    message=menu(False)
    if message==True:
        main_game()

start_check()
''' command="Server1.py"
    os.system(command)
    subprocess.Popen(command)'''
