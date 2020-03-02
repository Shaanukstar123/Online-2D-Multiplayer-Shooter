import pygame
import random

width = 1300
height = 700

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
        self.frame_counter=0
        self.time = random.randint(0,100) #Indicates at what time from timer the item will spawn

    def generate(self,walls):
        self.type = random.randint(1,3)
        self.x=random.randint(0,width-50)
        self.y=random.randint(0,height-50)
        self.hitbox=pygame.Rect(self.x,self.y,25,25)

        for wall in walls:
            if self.hitbox.colliderect(wall):
                return False
            else:
                return True

    def recreate(self,x,y,time,life,type):
        self.x = x
        self.y = y
        self.time = time
        self.life = life
        self.type = type

    def levitate(self):
        self.frame_counter+=1
        if self.frame_counter<40:
            self.y+=0.2
        else:
            self.y-=0.2
            if self.frame_counter>80:
                self.frame_counter=0

    def display(self,display,image):
        display.blit(image,(self.x,self.y))


    def display_anime(self,display,images,index):
        for image in images:
            display.blit(images[index],(self.x,self.y))
            #pygame.draw.rect(display,(99,99,99), self.hitbox)
