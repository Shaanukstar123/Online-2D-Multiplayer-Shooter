'''Problems that arose: Cannot pickle an image file. Fix: made Surface (self.anime) into string and saved surface data in variable 'image'''
import pygame
from Network import Network
from player import Player
from MainMenu import menu
from player import Map

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

    def redraw_window(gameDisplay,player, player2,background_index):
        background_index=int(background_index)
        gameDisplay.fill((255,255,255))
        gameDisplay.blit(backgrounds[background_index],(0,0))

        playerObj = player['player']
        secondPlayerObj = player2['player']
        wall1=player['wall']
        wall2=player['wall']
        print("{},{}".format(playerObj.x,playerObj.y))
        players=[playerObj, secondPlayerObj]
        wall1.collision(playerObj)
        wall2.collision(secondPlayerObj)

        if playerObj.dead==True or secondPlayerObj.dead==True:
            endgame()

        playerObj.draw(gameDisplay)
        secondPlayerObj.draw(gameDisplay)

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
    def endgame():
        print("EndGame")
        clock=pygame.time.Clock()
        while True:
            clock.tick(60)
            gameDisplay.fill((255,255,255))
            gameDisplay.blit(gameover,(0,0))
            pygame.display.update()
        '''Change this to return to main menu'''
    def main():
        run = True
        n = Network()
        p= n.getP()
        print(p)
        print(p['player'])
        playerObj = p['player']
        wall1 = p['wall']

        clock = pygame.time.Clock()
        background_index=-1
        while run:
            if background_index>6:
                background_index=0
            else:
                background_index+=0.15
            clock.tick(60)
            p2 = n.send(p)
            secondPlayerObj = p2['player']
            wall2=p2['wall']
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            playerObj.move()
            p['player'] = playerObj
            p['wall'] = wall1
            redraw_window(gameDisplay,p, p2,background_index)
            pygame.display.update()

    main()
message=menu(False)
if message==True:
    main_game()
