import pygame
class Player():
    def __init__(self, x, y,anime,player):
        self.x = x
        self.y = y
        self.player=player
        self.vel = 4
        self.anime=anime
        self.projectile="projectile.png"
        self.projx=0
        self.projy=0
        self.bullet_num=0

    def draw(self,gameDisplay):
        image=pygame.image.load(self.anime)
        gameDisplay.blit(image,(self.x,self.y))



    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            if self.player==1:
                self.anime="left.png"

        elif keys[pygame.K_RIGHT]:
            self.x += self.vel
            if self.player==1:
                self.anime="right.png"

        if keys[pygame.K_UP]:
            self.y -= self.vel*3

        elif keys[pygame.K_DOWN]:
            self.y += self.vel
        if keys[pygame.K_SPACE]:
            bulletnum+=1
            bullets.append(Projectile(self.x,self.y,5,"right","projectile.png",self.bullet_num))

        if self.y <450:
            self.y+=3


        #self.update()
class Projectile():
    def __init__(self,x,y,speed,direction,sprite,num):
        self.x=x
        self.y=y
        self.direction=direction
        self.speed=7
        self.sprite=sprite
        self.num=num

    def draw_bullet(gameDisplay):
        proj=pygame.image.load("projectile1.png")
        pygame.display.blit(proj)


    def shoot(self,gameDisplay):
        if keys[pygame.K_SPACE]:
            while self.x<500:
                projectile=pygame.image.load("projectile.png")
                gameDisplay.blit(projectile,(self.x,self.y))
                self.x+=self.speed













    '''def shoot(self,gameDisplay):
        projectile=pygame.image.load(self.projectile)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            #pygame.display.update()
            #self.shoot(gameDisplay)
            #gameDisplay.blit(projectile,(self.projx,self.projy))
                #while self.projx<500:
            gameDisplay.blit(projectile,(self.projx,self.projy))
            #self.update()
            #gameDisplay.blit(projectile,(self.projx,self.projy))
            #pygame.display.update()
            #self.projx+=5
            #pygame.display.update()
            if self.projx<500:
                #self.shoot(gameDisplay)
                self.update()
                gameDisplay.blit(projectile,(self.projx,self.projy))
    def update(self):
        self.projx+=5'''
