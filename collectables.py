import pygame
import random

width = 1300
height = 700
class Collectable_list:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get(self, id):
        pass
    def remove(self, item):
        self.items.remove(item)

class Collectable():
    def __init__(self):
        self.type=random.randint(1,3) # health, super-speed and invulnerability
        self.sprite=None
        self.x=random.randint(0,width-50)
        self.y=random.randint(0,height-50)
        self.type=None
        self.life = random.randint(300,2000)
        self.hitbox=pygame.Rect(self.x,self.y,25,25)
        self.correct_position=False
        self.status=None
        self.collected=False
        self.counter=0
        self.vanish=False
        self.id = random.randint(0,10)
        self.time = random.randint(0,100) #Indicates at what time from timer the item will spawn
        self.active=None

    def generate(self,walls):
        self.type = random.randint(1,3)
        self.x=random.randint(0,width-50)
        self.y=random.randint(0,height-50)
        self.hitbox=pygame.Rect(self.x,self.y,25,25)

        for wall in walls:
            if self.hitbox.colliderect(wall):
                self.correct_position=False
                return False
                #self.generate(walls)
            else:
                self.correct_position=True
                return True
    def recreate(self,x,y,time,life,type):
        self.x = x
        self.y = y
        self.time = time
        self.life = life
        self.type = type

    def levitate(self):
        self.counter+=1
        if self.counter<40:
            self.y+=0.2
        else:
            self.y-=0.2
            if self.counter>80:
                self.counter=0

    def collect(self,player):
        pass
        '''if self.hitbox.colliderect(player.hitbox):
            self.collected=True
            print("Item Collected")
            return True'''

    def display(self,gameDisplay,image):
        gameDisplay.blit(image,(self.x,self.y))


    def display_anime(self,gameDisplay,images,index):
        for image in images:
            gameDisplay.blit(images[index],(self.x,self.y))
            #pygame.draw.rect(gameDisplay,(99,99,99), self.hitbox)
