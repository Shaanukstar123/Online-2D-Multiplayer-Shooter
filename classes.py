import pygame
import random
import threading

width=1300
height=700

class Player():
    def __init__(self, x, y,sprite,player,direction,score,health):
        self.x = x
        self.y = y
        self.player=player
        self.projectiles = []
        self.speed = 10
        self.gravity=10
        self.sprite=sprite
        self.direction = direction #1=right, 2=left
        self.health=health
        self.display=sprite[direction]
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
        self.jump_speed=10
        self.jump_direction=None
        self.free_fall = False
        self.counter=0
        self.visible = True
        self.items=[]
        self.speed_power_timer = 0
        self.invisibility_timer = 0
        self.disconnected = False

    def draw(self,game):
        colour=(255,255,255)
        self.hitbox= pygame.Rect(self.x, self.y, 45, 68)
        #image=pygame.image.load(self.display)
        if self.player==1 and self.visible==True: #and game.one_hit==False:
            game.display.blit(game.loaded_player1[self.direction],(self.x,self.y))
        elif self.player==2 and self.visible==True: #and game.two_hit==False:
            game.display.blit(game.loaded_player2[self.direction],(self.x,self.y))
        rect = pygame.Rect(self.x, self.y, 45, 68)

        new_font = pygame.font.Font("Images/arcade.TTF", 28)
        health_p1 = new_font.render("HP "+(str(self.health)), 0, game.yellow)
        health_p2 = new_font.render("HP "+(str(self.health)), 0, game.green)
        if self.player==1:
            game.display.blit(health_p1, (30, 20))
        elif self.player==2:
            game.display.blit(health_p2, (width-110, 20))

    def alpha_transparency(self,display, source, location, opacity):
        x = location[0]
        y = location[1]
        surface = pygame.Surface((source.get_width(), source.get_height())).convert()
        surface.blit(display, (-x, -y))
        surface.blit(source, (0, 0))
        surface.set_alpha(opacity)
        display.blit(surface, location)

    '''def alpha_red(self,game):
        source = game.loaded_player1[self.direction]
        surface = pygame.Surface(source.get_size()).convert_alpha()
        surface.fill((255,0,0))
        source.blit(surface, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
        game.display.blit(game.loaded_player1[self.direction],(self.x,self.y))'''


    def item_use(self):
        for item in self.items:
            if item.type==1:
                self.health+=25
                self.items.remove(item)
            if item.type==2:
                self.visible = False
                self.items.remove(item)
            if item.type == 3:
                self.speed = 22
                self.items.remove(item)

    def stop_item_usage(self):
        if self.visible == False:
            self.invisibility_timer+=1
            if self.invisibility_timer > 200:
                self.visible = True
                self.invisibility_timer=0

        if self.speed > 14:
            self.speed_power_timer+=1
            if self.speed_power_timer>200:
                self.speed = 9
                self.speed_power_timer=0


    def collisions(self,game):
        for wall in game.walls:
        #if rect.colliderect(game.walls[0].rect) or rect.colliderect(game.walls[1].rect):
            if self.hitbox.colliderect(wall.rect):
                self.counter=0

                if self.direction==1: #make setcollision(col_right,col_left...) instead of if statements.
                    self.collision_type(True,False,False,False)

                elif self.direction==2:
                    self.collision_type(False,True,False,False)

                if (wall.y)>(self.y+40) or self.y<(game.height-80):# #<(game.walls[0].y) or (self.y+40)<(game.walls[1].y) and self.collision_up==False:#or(self.y+40)<(game.walls[1].y+game.walls[1].height/2) and self.collision_up==False:
                    self.collision_type(False,False,True,False)
                    #print("UP: {} Down: {}".format(self.collision_up,self.collision_down))

                if (wall.y)<(self.y+34): #or (game.walls[1].y+38)<(self.y): #and self.collision_down==False: #and self.collision_down==False:#<(game.walls[0].y+game.walls[0].height) or (self.y)<(game.walls[1].y+game.walls[1].height): #or (self.y)>(game.walls[1].y+game.walls[1].height/2) and
                    self.collision_type(False,False,False,True)
                    #print("UP: {} Down: {}".format(self.collision_up,self.collision_down))

            else:
                self.counter+=1
                if self.counter>2:
                    self.collision_type(False,False,False,False)


    def collision_type(self,right,left,down,up):
        self.collision_right = right
        self.collision_left = left
        self.collision_down = down
        self.collision_up = up


    def move(self,game):
        if self.y>(game.height-100) or self.collision_down == True:
            self.free_fall=False
        if self.collision_up == True:
            self.free_fall=True

        keys = pygame.key.get_pressed()
        if self.y<(game.height-80) and self.collision_down==False and self.jump==False:
            if self.gravity > 0:
                self.y-=(self.gravity ** 2) * 0.1 * (-1)
                self.gravity -= 0.01
            else:
                self.gravity=10
        else:
            self.gravity=10

        projectile_sound=pygame.mixer.Sound("laser.wav")
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

        if self.jump==False:
            if self.free_fall==False:
                if keys[pygame.K_UP]:
                    self.jump=True
                    self.free_fall==True
                #if self.y>0 and self.collision_up==False:
                    #self.y -= self.speed*3
            if keys [pygame.K_DOWN]:
                if self.y <(height-80) and self.collision_down==False:
                    self.y += self.speed
        else:
            if self.jump_speed > -10 and self.collision_up==False and self.y>0 :
                self.jump_direction=1
                if self.jump_speed<0:
                    self.free_fall = True
                    self.jump_direction=-1
                self.y -= ((self.jump_speed ** 2) * 0.1 * self.jump_direction)+15
                self.jump_speed -= 1

            else:
                self.jump=False
                self.jump_speed=10

        for event in game.events:
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if len(self.projectiles)<4:
                        projectile_sound.play()
                        self.projectiles.append(Projectile(self.x, self.y, self.direction, 'projectile1.png', self.player))

    def remove_projectile(self,proj):
        self.projectiles.remove(proj)

    def damage_taken(self):
        self.health-=10
        if self.health<2:
            self.dead=True
            print("Dead")
        print(self.health)


class Projectile(Player):
    def __init__(self,x,y,direction,sprite,player):
        self.x=x
        self.y=y
        self.direction=direction
        self.speed=35
        self.sprite=sprite
        #self.loaded_sprite = pygame.image.load(self.sprite)
        self.player=player
        self.shouldRemove = False
        self.hit_radius=50
        self.collided=False
        self.hitbox= pygame.Rect(self.x, self.y, 10, 10)

    def draw_bullet(self, display,players):
        self.hitbox=pygame.Rect(self.x, self.y, 10, 10)
        proj_img=pygame.image.load("projectile1.png")
        display.blit(proj_img, (self.x+10, self.y+20))
        if self.x<width and self.x>0:
            if self.direction==1:
                self.x+=self.speed
            elif self.direction==2:
                self.x-=self.speed
        else:
            self.shouldRemove = True

    def should_remove(self):
        return self.shouldRemove

    def collides(self,game):
        move_left = -25
        move_right = 25
        self.hitbox=pygame.Rect(self.x, self.y, 10, 10)
        for p in game.players:

            if self.hitbox.colliderect(p.hitbox) and self.player!=p.player:
                self.shouldRemove = True
                self.collided = True
                print("collided player {}".format(p.player))
                if p.x<=width-50 and p.x>=0:
                    if self.direction == 1:
                        p.x += move_right
                    elif self.direction == 2:
                        p.x += move_left
                p.damage_taken()
                print("Damage taken")
                if p.player == 1:
                    return True
                elif p.player == 2:
                    return True

            #check the boundaries of the projectile and boundaries of player and if they collide, call player.getdamage()
        for wall in game.walls:
            if self.hitbox.colliderect(wall.rect):
                self.shouldRemove = True
                self.collided = True


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
        game.display.blit(self.img,(self.x, self.y))


'''single underscore under name = private method/attribute'''
