import pygame
from Network import Network
from classes import *
from collectables import *
from MainMenu import menu
import time
import socket
from _thread import *
import sqlite3

class Game():
    def __init__(self, ip, username):
        self.username = username
        self.width = 1300
        self.height = 700
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.backgrounds = [
            pygame.image.load("sprites/Background anime/frame0.gif"),
            pygame.image.load("sprites/Background anime/frame1.gif"),
            pygame.image.load("sprites/Background anime/frame2.gif"),
            pygame.image.load("sprites/Background anime/frame3.gif"),
            pygame.image.load("sprites/Background anime/frame4.gif"),
            pygame.image.load("sprites/Background anime/frame5.gif"),
            pygame.image.load("sprites/Background anime/frame6.gif"),
            pygame.image.load("sprites/Background anime/frame7.gif")
        ]
        self.scaled_backgrounds = []
        self.clock = pygame.time.Clock()
        self.fps = 45
        self.count = 100
        self.music = pygame.mixer.music.load("power_music.wav")
        self.ip = ip
        self.p2 = None
        self.p = None
        self.n = None
        self.walls = [
            Map(900, 500, 44, 228, "wall1.png"),
            Map(600, 250, 44, 228, "wall1.png"),
            Map(200, 350, 44, 22, "wall1.png")
        ]
        self.wall_img = pygame.image.load("wall1.png")
        #self.items=[Collectables(1,"sprite.png")]
        self.proj_img = pygame.image.load("projectile1.png")
        self.run = False
        self.countdown_time=100
        self.playerObj = None
        self.secondPlayerObj = None
        self.players = None
        self.movement = False
        self.events = None
        self.loop_count = 0
        self.background_index = 0
        self.player1_sprites = ["sprite1.png", "right.png", "left.png"]
        self.player2_sprites = [
            "sprite2.png", "player2right.png", "player2left.png"
        ]
        self.loaded_player1 = []
        self.loaded_player2 = []
        self.collectable_list=[]
        self.arcade_font = pygame.font.Font("Images/arcade.TTF", 12)
        self.text_font = pygame.font.Font("Images/arcade.TTF", 28)

        self.speed_ball=[
            pygame.image.load("Images/SpeedBall/1.gif"),
            pygame.image.load("Images/SpeedBall/2.gif"),
            pygame.image.load("Images/SpeedBall/3.gif"),
            pygame.image.load("Images/SpeedBall/4.gif"),
            pygame.image.load("Images/SpeedBall/5.gif"),
            pygame.image.load("Images/SpeedBall/6.gif"),
            pygame.image.load("Images/SpeedBall/7.gif"),
            pygame.image.load("Images/SpeedBall/8.gif"),
            pygame.image.load("Images/SpeedBall/9.gif"),
            pygame.image.load("Images/SpeedBall/10.gif")
        ]
        self.invis_potion=pygame.image.load("Images/invisibilitypotion.png")
        self.heart_img = pygame.image.load("Images/heart.png")

        self.image_index = 0
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.yellow = (155,135,12)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.light_blue = (173, 216, 230)

    def load_sprites(self):
        for i in self.player1_sprites:
            image=pygame.image.load(i)
            self.loaded_player1.append(image)

        for j in self.player2_sprites:
            image=pygame.image.load(j)
            self.loaded_player2.append(image)

    def background_scale(self):
        for background in self.backgrounds:
            self.scaled_backgrounds.append(pygame.transform.scale(background,
            (self.width,self.height)))

    def show_username(self):
        self.playerObj.username=self.username
        username = self.arcade_font.render(str(self.username), 0, self.light_blue)
        player2_username=self.arcade_font.render(str(self.secondPlayerObj.username), 0, self.light_blue)
        self.gameDisplay.blit(username, (self.playerObj.x,self.playerObj.y-20))
        self.gameDisplay.blit(player2_username, (self.secondPlayerObj.x,self.secondPlayerObj.y-20))


    def redraw_window(self):
        #self.secondPlayerObj.collisions(self)
        #self.playerObj.jumped()
        #self.secondPlayerObj.jumped()
        #if self.secondPlayerObj==True:
            #self.secondPlayerObj.jump()
        #print("Player1: {} Player2: {}".format(self.player1_score,self.player2_score))
        score1 = self.text_font.render(str(self.playerObj.score), 0, self.white)
        score2 = self.text_font.render(str(self.secondPlayerObj.score), 0, self.white)
        self.gameDisplay.fill((255,255,255))
        index=int(self.background_index)
        self.gameDisplay.blit(self.scaled_backgrounds[index],(0,0))
        self.gameDisplay.blit(score1, (20, 50))
        self.gameDisplay.blit(score2, (self.width-40, 50))
        self.playerObj.draw(self)
        self.secondPlayerObj.draw(self)
        self.backwards_time=(self.countdown_time-(self.timer.time_elapsed))
        time = self.text_font.render(str(self.backwards_time), 0, self.white)
        self.gameDisplay.blit(time, (self.width/2, 20))

        #self.playerObj.collectables(self)
        #self.secondPlayerObj.collectables(self)


        for wall in self.walls:
            wall.draw(self)

        self.collectables()
        self.playerObj.item_use()
        self.playerObj.stop_item_usage()
        self.secondPlayerObj.item_use()
        self.secondPlayerObj.stop_item_usage()

        for bullet in self.playerObj.projectiles:
            if bullet.collides(self)=="hit":
                if self.timer.has_started==True:
                    self.playerObj.score+=10
                '''if self.playerObj.player==1:
                    self.player1_score+=10
                    self.playerObj.score+=10
                elif self.playerObj.player==2:
                    self.player2_score+=10
                    self.secondPlayerObj.score+=10'''
            if bullet.should_remove():
                self.playerObj.remove_projectile(bullet)
                continue

            bullet.draw_bullet(self.gameDisplay,self.players)

        for bullet in self.secondPlayerObj.projectiles:
            if bullet.collides(self)=="hit":
                #if self.secondPlayerObj.player==1:
                    #self.player1_score+=10
                    #self.playerObj.score+=10
                #elif self.playerObj.player==2:
                #self.player2_score+=10
                if self.timer.has_started==True:
                    self.secondPlayerObj.score+=10
                else:
                    print("Can't score yet")
                #self.players,self.walls[0],self.walls[1])
            if bullet.should_remove():
                self.secondPlayerObj.remove_projectile(bullet)
                continue
            bullet.draw_bullet(self.gameDisplay,self.players)
        #if len(items) < 5:
        #shouldSpawn = random.randint(0,5000)
        #if shouldSpawn < SPAWN_PERCENTAGE:
        #    newItem = Collectables(1, "sprite.png")
        #    items.append(newItem)

        #for i in items:
            #if i.life <= 0:
                #items.remove(i)
                #continue
            #i.display_items(gameDisplay)
            # random_time=random.randint(0,15)
            #i.generate(wall)
            # time_end = time.time() + 5
            # if time.time() < time_end:
            #i.display_items(gameDisplay)
                #print("item Displayed!")
            # TODO: Make it for both players
            #if i.x==playerObj.x:
                #items.remove(i)
                #print("Object Collected")

    def collectables(self):
        if self.image_index>8:
            self.image_index=0
        self.image_index+=1
        for item in self.collectable_list:
            item.hitbox=pygame.Rect(item.x,item.y,25,25)
            if item.time < self.timer.time_elapsed:

                if item.hitbox.colliderect(self.playerObj.hitbox):
                    self.playerObj.items.append(item)
                    self.collectable_list.remove(item)
                elif item.hitbox.colliderect(self.secondPlayerObj.hitbox):
                    self.secondPlayerObj.items.append(item)
                    self.collectable_list.remove(item)
                if item.life>0:
                    item.levitate()
                    if item.type == 1:
                        item.display(self.gameDisplay,self.heart_img)

                    if item.type == 2:
                        item.display(self.gameDisplay,self.invis_potion)

                    if item.type == 3:
                        item.display_anime(self.gameDisplay,self.speed_ball,self.image_index)

                    item.life-=1
                else:
                    self.collectable_list.remove(item)

        '''if len(self.collectable_list)>0:
            for item in self.collectable_list:
                item.id = "21"
                if item.hitbox.colliderect(self.playerObj.hitbox):
                    item.collected=True
                    item.life=0
                    self.vanish=True
                    self.playerObj.items.append(item.type)
                    #self.collectable_list.remove(item)
                else:
                    if not item.vanish:
                        item.display(self.gameDisplay,self.speed_ball,self.image_index)'''

    def endgame(self,player1_dead,player1_health,name1,player2_dead,player2_health,name2):
        count=0

        new_font = pygame.font.Font("Images/arcade.TTF", 80)
        player_font=pygame.font.Font("Images/arcade.TTF", 60)
        game_over = new_font.render(str("GAME OVER"), 0, self.black)
        player1=player_font.render(str(name1 +"  wins!"), 0, self.yellow)
        player2=player_font.render(str(name2 +"   wins!"), 0, self.green)
        tie=player_font.render(str("Match    Tied"), 0, self.blue)

        player1_wins=False
        player2_wins=False
        game_tie=False

        if player1_dead==True:
            player2_wins=True
            print("player 2 wins!")
        elif player2_dead==True:
            player1_wins=True
            print("player 1 wins!")

        if player1_dead==False and player2_dead==False:
            if player1_health>player2_health:
                player1_wins=True
                player2_wins=False
            if player1_health<player2_health:
                player2_wins=True
                player1_wins=False
            else:
                player1_wins=False
                player2_wins=False
                game_tie=True
        while True:
            if count==12:
                start_check(self.username)
            count+=1
            self.gameDisplay.fill((255,255,255))
            self.gameDisplay.blit(game_over, ((width/2) - (200), (height/2)))
            if player1_wins==True:
                self.gameDisplay.blit(player1, ((self.width/2) - (200), (self.height/2+100)))
            if player2_wins==True:
                self.gameDisplay.blit(player2, ((self.width/2) - (200), (self.height/2+100)))
            if game_tie==True:
                self.gameDisplay.blit(tie, ((self.width/2) - (200), (self.height/2+100)))

            pygame.mixer.music.stop()
            print("Game Over")
            self.clock.tick(2)
            pygame.display.update()

    def save_score(self):
        with sqlite3.connect('playerdata.db') as db:
            cursor = db.cursor()

        player_search = ('SELECT * FROM player WHERE username = ?')
        cursor.execute(player_search,[(self.username)])
        print(cursor.fetchall())
        #store_score = 'INSERT INTO player(highscore) VALUES(?)'
        #cursor.execute(store_score,[(self.playerObj.score)])
        update_score = 'UPDATE player SET highscores = ? WHERE username = ? AND highscores < ?'
        cursor.execute(update_score,[(self.playerObj.score),(self.username),(self.playerObj.score)])
        db.commit()

    def gameloop(self):
        print(self.username)
        self.load_sprites()
        self.background_scale()
        music=self.music
        pygame.mixer.music.play(-1)
        self.run = True
        try:
            self.n = Network(self.ip)
            self.p= self.n.getP()
            print(self.p)
            print(self.p['player'])
            self.playerObj = self.p['player']
            self.timer = self.p['timer']
            self.collectable_data= self.p['collectable']


        except:
            print("Cannot connect to server")
        self.movement=True
        while self.run:
            self.loop_count+=1


            if self.background_index>6:
                self.background_index=0
            else:
                self.background_index+=0.30
            self.p2 = self.n.send(self.p)
            self.secondPlayerObj=self.p2['player']
            self.timer = self.p2['timer']
            self.collectable_data= self.p2['collectable']

            if self.loop_count == 1:
                for data in self.collectable_data:
                    item=Collectable()
                    item.recreate(data[0],data[1],data[2],data[3],data[4])
                    self.collectable_list.append(item)
                    print(self.collectable_list)
            #print(self.collectable_list)

            self.players=[self.playerObj,self.secondPlayerObj]

            #self.playerObj=self.players[0]
            #self.secondPlayerObj=self.players[1]

            #secondPlayerObj = p2['player']
            #wall2=p2['wall']
            self.events=pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
            self.playerObj.collisions(self)
            self.playerObj.move(self)
            self.redraw_window()

            self.show_username()

            if self.playerObj.dead==True or self.secondPlayerObj.dead==True or self.timer.time_elapsed>self.countdown_time:
                self.save_score()
                self.run=False
                self.endgame(self.playerObj.dead,self.playerObj.health,str(self.playerObj.username),self.secondPlayerObj.dead,self.secondPlayerObj.health,str(self.secondPlayerObj.username))
            self.clock.tick(self.fps)
            pygame.display.update()


def start_check(player):
    host=socket.gethostname()
    ip=socket.gethostbyname(host)#'192.168.1.225'
    message=menu(False)
    if message==True:
        game=Game(ip,player)
        game.gameloop()
#start_check()

'''Things to still fix:

Collectable items
Projectiles going through walls
Disable double jump
Talk about problems with collectables (sending list data instead of running it on the server)
'''
