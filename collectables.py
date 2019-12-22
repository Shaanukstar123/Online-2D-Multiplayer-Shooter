import pygame
import random

width = 1300
height = 700
class Collectable_list:
    def __init__(self):
        self.items = []

    def add(self, item):
        pass

    def get(self, id):
        pass

class Collectable():
    def __init__(self):
        self.item=None
        self.sprite=None
        self.x=random.randint(0,width-50)
        self.y=random.randint(0,height-50)
        self.type=None
        self.life = random.randint(300,2000)
        self.hitbox=pygame.Rect(self.x,self.y,20,20)
        self.correct_position=False
        self.status=None

    def generate(self,walls):
        self.x=random.randint(0,width)
        self.y=random.randint(0,height)
        self.hitbox=pygame.Rect(self.x,self.y,40,40)
        for wall in walls:
            if self.hitbox.colliderect(wall):
                self.correct_position=False
            else:
                self.correct_position=True
        if self.correct_position==False:
            self.generate(wall)

    def collected(self,player):
        if self.colliderect(player.hitbox,self.hitbox):
            return True


    def display(self,gameDisplay,images,index):
        for image in images:
            gameDisplay.blit(images[index],(self.x,self.y))
        object = pygame.Rect(self.x,self.y,40,40)
        #pygame.draw.rect(gameDisplay,(99,99,99), object)

    #def spawn(self):
