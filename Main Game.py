import pygame
from Network import Network
from player import *
from MainMenu import menu
import time
import socket
from _thread import *

class Game():
    def __init__(self,ip):
        self.width=1300
        self.height=700
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.backgrounds=[pygame.image.load("sprites/Background anime/frame0.gif"),pygame.image.load("sprites/Background anime/frame1.gif"),pygame.image.load("sprites/Background anime/frame2.gif"),pygame.image.load("sprites/Background anime/frame3.gif"),pygame.image.load("sprites/Background anime/frame4.gif"),pygame.image.load("sprites/Background anime/frame5.gif"),pygame.image.load("sprites/Background anime/frame6.gif"),pygame.image.load("sprites/Background anime/frame7.gif")]
        self.scaled_backgrounds=[]
        self.clock=pygame.time.Clock()
        self.stopclock=Timer(100)
        self.timer=False
        self.count =100
        self.music=pygame.mixer.music.load("power_music.wav")
        self.ip=ip
        self.p2=None
        self.p=None
        self.n=None
        self.walls=[Map(400,400,300,100,"wall1.png"),Map(600,600,300,100,"wall1.png")]
        self.wall_rect=[self.walls[0].rect,self.walls[1].rect]
        self.wall_img=pygame.image.load("wall1.png")
        #self.items=[Collectables(1,"sprite.png")]
        self.proj_img=pygame.image.load("projectile1.png")
        self.run=False
        self.playerObj=None
        self.secondPlayerObj=None
        self.players=None
        self.movement=False
        self.events=None
        self.background_index=0
    def background_add(self):
        for background in self.backgrounds:
            self.scaled_backgrounds.append(pygame.transform.scale(background,
            (self.width,self.height)))

    def redraw_window(self):
        self.gameDisplay.fill((255,255,255))
        index=int(self.background_index)
        print(index)
        self.gameDisplay.blit(self.scaled_backgrounds[index],(0,0))
        #if (pygame.sprite.collide_rect(playerObj.sprite,wall)):
            #print("Success!")
        #background_index=int(background_index)
        #gameDisplay.fill((255,255,255))
        #gameDisplay.blit(backgrounds[background_index],(0,0))

        #playerObj = player['player']
        #secondPlayerObj = player2['player']
        #players=[playerObj, secondPlayerObj]

        self.playerObj.draw(self.gameDisplay,self.walls[0],self.walls[1],self.wall_img)
        self.secondPlayerObj.draw(self.gameDisplay,self.walls[0],self.walls[1],self.wall_img)

        '''if len(items) < 5:
            shouldSpawn = random.randint(0,5000)
            if shouldSpawn < SPAWN_PERCENTAGE:
                newItem = Collectables(1, "sprite.png")
                items.append(newItem)

        for i in items:
            if i.life <= 0:
                items.remove(i)
                continue
            #i.display_items(gameDisplay)
            # random_time=random.randint(0,15)
            #i.generate(wall)
            # time_end = time.time() + 5
            # if time.time() < time_end:
            i.display_items(gameDisplay)
                #print("item Displayed!")
            # TODO: Make it for both players
            if i.x==playerObj.x:
                items.remove(i)
                print("Object Collected")'''

        for bullet in self.playerObj.projectiles:
            bullet.collides(self.players,self.walls[0],self.walls[1])
            if bullet.should_remove():
                self.playerObj.remove_projectile(bullet)
                continue

            bullet.draw_bullet(self.gameDisplay,self.players)

        for bullet in self.secondPlayerObj.projectiles:
            bullet.collides(self.players,self.walls[0],self.walls[1])
            if bullet.should_remove():
                self.secondPlayerObj.remove_projectile(bullet)
                continue
            bullet.draw_bullet(self.gameDisplay,self.players)
        #pygame.display.update()
    def endgame(self):
        colour=(0,0,0)
        yellow=(255,255,0)
        green=(0,255,0)
        blue=(0, 0, 255)
        count=0
        while True:
            if count==12:
                start_check()
            count+=1
            self.gameDisplay.fill((255,255,255))
            new_font = pygame.font.Font("Images/arcade.TTF", 80)
            player_font=pygame.font.Font("Images/arcade.TTF", 60)

            game_over = new_font.render(str("GAME OVER"), 0, colour)
            player2=player_font.render(str("Green   wins!"), 0, green)
            player1=player_font.render(str("Yellow   wins!"), 0, yellow)
            self.gameDisplay.blit(game_over, ((width/2) - (200), (height/2)))
            tie =player_font.render(str("Match Tied"), 0, blue)
            pygame.mixer.self.music.stop()
            print("Game Over")
            if self.player.player==1:
                if self.player.dead==True:
                    self.gameDisplay.blit(self.player2, ((self.width/2) - (200), (self.height/2+100)))
                    print("player 2 wins!")
                else:
                    print("player 1 wins!")
                    self.gameDisplay.blit(player1, ((self.width/2) - (200), (self.height/2+100)))
            elif self.player.player ==2:
                if self.player.dead==True:
                    print("player 1 wins!")
                    self.gameDisplay.blit(player1, ((self.width/2) - (200), (self.height/2+100)))
                else:
                    print("player 2 wins!")
                    self.gameDisplay.blit(player2, ((self.width/2) - (200), (self.height/2+100)))
            else:
                self.gameDisplay.blit(tie, ((width/2) - (200), (height/2+100)))

            self.clock.tick(2)
            self.pygame.display.update()

    def gameloop(self):
        self.background_add()
        self.run = True
        try:
            self.n = Network(self.ip)
            self.p= self.n.getP()
            print(self.p)
            print(self.p['player'])
            self.playerObj = self.p['player']

        except:
            print("Cannot connect to server")
            #self.error()

        #background_index=-1
        self.movement=True
        while self.run:
            if self.background_index>6:
                self.background_index=0
            else:
                self.background_index+=0.15
            self.p2 = self.n.send(self.p)
            self.secondPlayerObj=self.p2['player']
            self.players=[self.playerObj,self.secondPlayerObj]
            #secondPlayerObj = p2['player']
            #wall2=p2['wall']
            '''if timer==False:
                if secondPlayerObj.x!=100:
                    start_new_thread(threaded_timer,((100,self.gameDisplay,clock)))
                    timer=True'''
            self.events=pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()

            if self.playerObj.dead==True: #or self.secondPlayerObj.dead==True :
                self.run=False
                self.endgame()#(playerObj,gameDisplay)

            self.playerObj.move(self.events)
            self.redraw_window()#(gameDisplay,p, p2,background_index,wall1,wall2,wall_image,projimg)
            self.stopclock.show_time(self.secondPlayerObj,self.gameDisplay)
            #if stopclock.time
            #health_item.generate(wall_rect)
            #health_item.display_items(gameDisplay,stopclock.time)
            if self.stopclock.end==True:
                self.run=False
                self.endgame()#(playerObj,gameDisplay)
            self.clock.tick(60)
            pygame.display.update()


def start_check():
    host=socket.gethostname()
    ip=socket.gethostbyname(host)
    message=menu(False)
    if message==True:
        game=Game(ip)
        game.gameloop()
start_check()
