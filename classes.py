import pygame
import random
import threading

width=1300
height=700

class Player():
    def __init__(self, x, y,sprite,player,direction,score):
        self.x = x
        self.y = y
        self.player=player
        self.projectiles = []
        self.speed = 9
        self.gravity=8
        self.sprite=sprite
        self.direction = direction #1=right, 2=left
        self.health=100
        self.display=sprite[direction]
        self.bullet_count=2 #limits number of bullets per shot
        self.dead=False
        self.collision_left=False
        self.collision_right=False
        self.collision_up=False
        self.collision_down=False
        self.hitbox=pygame.Rect(self.x, self.y, 45, 68)
        self.username=None
        self.score=score
        self.jump=False
        self.jump_position=10
        self.counter=0

    def draw(self,game):
        self.hitbox= pygame.Rect(self.x, self.y, 45, 68)
        wallie=pygame.Rect(game.walls[0].x, game.walls[0].y+35, 10,10 )
        #loaded=[pygame.image.load(sprite[0]),pygame.image.load(sprite[1])]
        image=pygame.image.load(self.display)
        if self.player==1:
            game.gameDisplay.blit(game.loaded_player1[self.direction],(self.x,self.y))
        elif self.player==2:
            game.gameDisplay.blit(game.loaded_player2[self.direction],(self.x,self.y))
        rect = pygame.Rect(self.x, self.y, 45, 68)
        rect2=pygame.Rect(game.walls[1].x,game.walls[1].y,25,25)
        #for wall in walls:
        #wallimg=pygame.image.load(wall.image)
        #pygame.draw.rect(game.gameDisplay,(0,255,0),rect2)
        pygame.draw.rect(game.gameDisplay,(0,255,0),game.walls[0].rect)
        #pygame.draw.rect(game.gameDisplay,(99,99,99), wallie)
        #print(game.walls[0].x,game.walls[0].y,self.y)
            #print("Not collided")
        #print(self.collision_up,self.collision_down,self.collision_right,self.collision_right)
        new_font = pygame.font.Font("Images/arcade.TTF", 28)
        colour=(255,255,255)
        health = new_font.render((str(self.health)+"%"), 0, colour)
        if self.player==1:
            game.gameDisplay.blit(health, (30, 20))
        elif self.player==2:
            game.gameDisplay.blit(health, (width-110, 20))
        #print("{} {}".format(self.collision_down,self.collision_up))

    def collisions(self,game):

        for wall in game.walls:
        #if rect.colliderect(game.walls[0].rect) or rect.colliderect(game.walls[1].rect):
            if self.hitbox.colliderect(wall):
                self.counter=0
                #if wall==game.walls[0]:
                    #print("collided")
                if self.direction==1: #make setcollision(col_right,col_left...) instead of if statements.
                    self.collision_type(True,False,False,False)

                elif self.direction==2:
                    self.collision_type(False,True,False,False)

                if (wall.y)>(self.y+40):# #<(game.walls[0].y) or (self.y+40)<(game.walls[1].y) and self.collision_up==False:#or(self.y+40)<(game.walls[1].y+game.walls[1].height/2) and self.collision_up==False:
                    self.collision_type(False,False,True,False)
                    print("UP: {} Down: {}".format(self.collision_up,self.collision_down))

                if (wall.y)<(self.y-34): #or (game.walls[1].y+38)<(self.y): #and self.collision_down==False: #and self.collision_down==False:#<(game.walls[0].y+game.walls[0].height) or (self.y)<(game.walls[1].y+game.walls[1].height): #or (self.y)>(game.walls[1].y+game.walls[1].height/2) and
                    self.collision_type(False,False,False,True)
                    print("UP: {} Down: {}".format(self.collision_up,self.collision_down))

            else:
                self.counter+=1
                if self.counter>2:
                    self.collision_type(False,False,False,False)

                '''if self.x>wall.x+wall.width/2 or self.x<wall.x-wall.width/2:
                    self.collision_down=False
                    self.collsion_up=False
                print("UP: {} Down: {}".format(self.collision_up,self.collision_down))
                #self.collision_type(False,False,False,False)'''


    def collision_type(self,right,left,down,up):
        self.collision_right = right
        self.collision_left = left
        self.collision_down = down
        self.collision_up = up

    '''def collision_check(self,wall):
        if self.x>=wall.x-wall.width/2 and self.x<=wall.x+wall.width/2:
            if self.y+30<=wall.y+wall.height/2 and self.y-30>=wall.y-wall.height/2:
                return True
            else:
                return False'''

    def move(self,game):

        projectile_sound=pygame.mixer.Sound("laser.wav")
        keys = pygame.key.get_pressed()
        #if pygame.sprite.collide_rect(self.sprite,wall.image)
        if self.y<(height-80) and self.collision_down==False:
            self.y+=self.gravity
        if keys[pygame.K_LEFT]:
            if 0<=self.x and self.collision_left==False:
                self.x -= self.speed
                self.direction=2
                self.display=self.sprite[2]

        if keys[pygame.K_RIGHT]:
            if self.x<=width-50 and self.collision_right==False:
                self.x += self.speed
                self.direction=1
                self.display=self.sprite[1]

        #if keys[pygame.K_UP]:
            #if self.y>0 and self.collision_up==False:
                #self.y -= self.speed*3

        if keys [pygame.K_DOWN]:
            if self.y <(height-50) and self.collision_down==False:
                self.y += self.speed

        for event in game.events:
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if len(self.projectiles)<4:
                        projectile_sound.play()
                        self.projectiles.append(Projectile(self.x, self.y, self.direction, 'projectile1.png', self.player))

                if event.key==pygame.K_UP:
                    if self.collision_up==False:
                        self.jump=True
                        self.jump_positon=self.y

    def jumped(self):
        if self.jump==True and self.collision_up==False:
            self.y-=self.speed*2.5
        if self.collision_up==True:
            self.jump=False

        if self.y<self.jump_position+100 and self.jump==True:
            self.jump=False

    def remove_projectile(self,proj):
        self.projectiles.remove(proj)

    def damage_taken(self):
        if self.health<2:
            self.dead=True
        self.health-=10

    def update(self):
        pass

    def update_username(self,username):
        self.username=username

class Projectile(Player):
    def __init__(self,x,y,direction,sprite,player):
        self.x=x
        self.y=y
        self.direction=direction
        self.speed=35
        self.sprite=sprite
        self.player=player
        self.shouldRemove = False
        self.hit_radius=50
        self.collided=False
        self.hitbox= pygame.Rect(self.x, self.y, 10, 10)

    def draw_bullet(self, gameDisplay,players):
        self.hitbox=pygame.Rect(self.x, self.y, 10, 10)
        proj=pygame.image.load("projectile1.png")
        #rect = pygame.Rect(self.x+30, self.y+25, 5, 5)
        #pygame.draw.rect(gameDisplay,(150,159,159), self.hitbox)
        gameDisplay.blit(proj, (self.x+10, self.y+20))
        if self.x<width and self.x>0:
            if self.direction==1:
                self.x+=self.speed
            elif self.direction==2:
                self.x-=self.speed
        else:
            self.shouldRemove = True
            for p in players:
                p.bullet_count=2

    def should_remove(self):
        return self.shouldRemove

    def collides(self,game):#self,players,wall,wall2):
        '''if self.hitbox.colliderect(game.walls[0].rect) or self.hitbox.colliderect(game.walls[1].rect):
            self.shouldRemove=True
            self.collided=True
            #print(players)
        if self.x<=p.x<(self.x+25) and (self.y-self.hit_radius)<p.y<self.y+40 and self.player!=p.player:
            print("collided")
            game.secondPlayerObj.score+=10
            game.playerObj.damage_taken()
            self.collided=True
        if self.hitbox.colliderect(game.secondPlayerObj.hitbox):
            print("collided")
            game.playerObj.score+=10
            game.secondPlayerObj.damage_taken()
            self.collided=True'''
            #if game.playerObj.health<10:
                #print("DEAD")'''


        for p in game.players:
            #print(p.health)
            if self.x<=p.x<(self.x+25) and (self.y-self.hit_radius)<p.y<self.y+40 and self.player!=p.player:
                self.shouldRemove=True
                self.collided =True
                print("collided player {}".format(p.player))
                print(p.player)
                p.damage_taken()

                if p.player==1:
                    return ("hit")
                elif p.player==2:
                    return("hit")
                #print(p.health)
                #if p.health<10:
                    #print("DEAD")
            #check the boundaries of the projectile and boundaries of player and if they collide, call player.getdamage()
class Map():
    def __init__(self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image=image
        self.rect = pygame.Rect(self.x,self.y,228,44)
        self.img = pygame.image.load("wall1.png")

    def collision(self,player):
        if (self.x-(self.width/2)<player.x<self.x+(self.width/2)) or(self.y-(self.height/2)<player.y<self.y+(self.height/2)):
            return True

    def draw(self,game):
        game.gameDisplay.blit(self.img,(self.x, self.y))

        #game.gameDisplay.blit(game.wall_img,(game.walls[0].x,game.walls[0].y))
        #wall2img=pygame.image.load(wall2.image)
        #game.gameDisplay.blit(game.wall_img,(game.walls[1].x,game.walls[1].y))

    '''def draw(self,gameDisplay):
        wall1=pygame.image.load(self.image)
        wall = pygame.Rect(self.x,self.y,228,44)
        gameDisplay.blit(wall1,(self.x,self.y))'''

class CollectableList():
    def __init__(self):
        self.items = []

    def add(self, item):
        pass

    def get(self, id):
        pass

class Collectable():
    def __init__(self,item,sprite):
        self.item=item
        self.sprite=sprite
        self.x=random.randint(0,width)
        self.y=random.randint(0,height)
        self.life = 300
        self.hitbox=pygame.Rect(self.x,self.y,20,20)
        self.correct_position=False

    def generate(self,wall):
        self.x=random.randint(0,width)
        self.y=random.randint(0,height)
        self.hitbox=pygame.Rect(self.x,self.y,40,40)
        if self.hitbox.colliderect(wall):
            self.correct_position=False
        else:
            self.correct_position=True
        if self.correct_position==False:
            self.generate(wall)

    def display_items(self,gameDisplay):
        object = pygame.Rect(self.x,self.y,40,40)
        self.life -= 1
        pygame.draw.rect(gameDisplay,(99,99,99), object)

    #def spawn(self):

'''single underscore under name = private method/attribute'''
