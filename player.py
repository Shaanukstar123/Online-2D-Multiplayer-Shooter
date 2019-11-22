import pygame
import random

width=1300
height=700

class Player():
    def __init__(self, x, y,sprite,player,direction):
        self.x = x
        self.y = y
        self.player=player
        self.projectiles = []
        self.speed = 4
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
        self.hitbox=rect = pygame.Rect(self.x, self.y, 45, 68)

    def draw(self,gameDisplay,wall):
        image=pygame.image.load(self.display)
        wall1=pygame.image.load(wall.image)
        rect = pygame.Rect(self.x, self.y, 45, 68)
        wall = pygame.Rect(wall.x,wall.y,228,44)
        gameDisplay.blit(wall1,(wall.x,wall.y))
        #pygame.draw.rect(gameDisplay,(99,99,99), wall)
        #pygame.draw.rect(gameDisplay,(99,99,99), rect)
        gameDisplay.blit(image,(self.x,self.y))
        if rect.colliderect(wall):
            #print("Success!")
            if self.direction==1 and self.collision_down==False:
                self.collision_right=True
                self.collision_left=False
                self.collision_up=False
            if self.direction==2 and self.collision_down==False:
                self.collision_left=True
                self.collision_right=False
                self.collision_up=False
            if (self.y+40)<(wall.y+wall.height/2) and self.collision_up == False:
                self.collision_down=True
                self.collision_left=False
                self.collision_right=False
            if (self.y-20)<(wall.y+wall.height/2) and self.collision_down==False:
                self.collision_up=True
                self.collsion_down=False
                self.collision_right=False
                self.collision_left=False
        else:
            self.collision_right=False
            self.collision_left=False
            self.collision_up=False
            self.collision_down=False

        new_font = pygame.font.Font("Images/arcade.TTF", 28)
        colour=(255,255,255)
        health = new_font.render(str(self.health), 0, colour)
        if self.player==1:
            gameDisplay.blit(health, (230 - (200), 20))
        elif self.player==2:
            gameDisplay.blit(health, (width+100 - (200), 20))

    def move(self,events,wall):
        projectile_sound=pygame.mixer.Sound("laser.wav")
        keys = pygame.key.get_pressed()
        #if pygame.sprite.collide_rect(self.sprite,wall.image)
        '''Dont use pygame.key.pressed for projectiles because fps makes more than one bullet shoot at a time'''
        '''if self.x==(wall.x-wall.width/2) and (wall.y-(height/2))<self.y<(wall.y+(height/2)):
            print("collided right")
            self.collision_right=True
            self.collision_left=False

        elif self.x==(wall.x+wall.width/2) and (wall.y-(height/2))<self.y<(wall.y+(height/2)):
            print("collided left")
            self.collision_left==True
            #self.collison_right=False
        else:
            self.collision_left = False
            self.collision_right=False
        #if self.y<(wall.y+wall.height) and self.y>(wall.y-height):
            #self.collision_y=True'''

        if keys[pygame.K_LEFT]:
            if 0<=self.x and self.collision_left!=True:
                self.x -= self.speed
                self.direction=2
                self.display=self.sprite[2]

        if keys[pygame.K_RIGHT]:
            #print(self.x)
            if self.x<=width-50:
                if self.collision_right==False:
                    self.x += self.speed
                    self.direction=1
                    self.display=self.sprite[1]

        if keys[pygame.K_UP]:
            if self.collision_up==False:
                if self.y>0:
                    '''#if self.y<(wall.y-wall.height/2) or self.y>(wall.x+wall.height/2) and self.collision_x==True:
                        self.collision_x=False
                        self.collision_y = False
                    else:
                        self.collision_y=True'''
                #if self.collision_y==False:
                    self.y -= self.speed*3

        elif keys [pygame.K_DOWN]:
            if self.collision_down==False:
                if self.y <(height-50):
                    self.y += self.speed

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if len(self.projectiles)<4:
                        projectile_sound.play()
                        self.projectiles.append(Projectile(self.x, self.y, self.direction, 'projectile1.png', self.player))

        if self.y <(height-80):
            if self.collision_down==False:
                self.y+=5

    def remove_projectile(self,proj):
        self.projectiles.remove(proj)

    def damage_taken(self):
        if self.health<1:
            self.dead=True
        self.health-=10

    def update(self):
        pass

class Projectile(Player):
    def __init__(self,x,y,direction,sprite,player):
        self.x=x
        self.y=y
        self.direction=direction
        self.speed=20
        self.sprite=sprite
        self.player=player
        self.shouldRemove = False
        self.hit_radius=50
        self.collided=False
        self.hitbox=rect = pygame.Rect(self.x, self.y, 10, 10)

    def draw_bullet(self, gameDisplay,players):
        proj=pygame.image.load("projectile1.png")
        #rect = pygame.Rect(self.x+30, self.y+25, 5, 5)
        #pygame.draw.rect(gameDisplay,(150,159,159), rect)
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

    def collides(self,players):
        for p in players:
            #print(p.health)
            if self.x<=p.x<(self.x+25) and (self.y-self.hit_radius)<p.y<self.y+40 and self.player!=p.player:
                self.shouldRemove=True
                self.collided =True
                print("collided")
                p.damage_taken()
                print(p.health)
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

#to stop player from waling through walls, I need a restriction zone
    def collision(self,player):
        if (self.x-(self.width/2)<player.x<self.x+(self.width/2)) or(self.y-(self.height/2)<player.y<self.y+(self.height/2)):
            return True

class Collectables():
    def __init__(self,item,sprite):
        self.item=item
        self.sprite=sprite
        self.x=0
        self.y=0
        self.hitbox=pygame.Rect(self.x,self.y,20,20)
        self.correct_position=False

    def generate(self,wall1):
        self.x=random.randint(0,width)
        self.y=random.randint(0,height)
        self.hitbox=pygame.Rect(self.x,self.y,20,20)
        if self.hitbox.colliderect(wall1):
            self.correct_position=False
        else:
            self.correct_position=True
        if self.correct_position==False:
            self.generate(wall1)

    def display_items(self,gameDisplay):
        object = pygame.Rect(self.x,self.y,40,40)
        pygame.draw.rect(gameDisplay,(99,99,99), object)

    #def spawn(self):
class Timer():
    def __init__ (self,time):
        self.time=time
        self.start=False
        self.end=False
        self.font=pygame.font.Font("Images/arcade.TTF", 35)

    def show_time(self,player2,gameDisplay):
        colour=(255,255,255)

        if self.start==False:
            if player2.x!=100:
                self.start=True
        if self.start==True:
            if self.time<1:
                print("Time's up")
                self.start=False
            else:
                timer = self.font.render(str(int(self.time)), 0, colour)
                gameDisplay.blit(timer, (width/2 - (200), 20))
                self.time-=(1/60)
                print(int(self.time))
        if self.time<1:
            self.end=True
