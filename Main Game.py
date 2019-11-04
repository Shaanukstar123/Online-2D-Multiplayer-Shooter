'''Problems that arose: Cannot pickle an image file. Fix: made Surface (self.anime) into string and saved surface data in variable 'image'''
import pygame
from Network import Network
from player import Player
from MainMenu import menu

def main_game():
    width = 900
    height = 550
    gameDisplay = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Client")
    background=pygame.image.load('forest_background.jpg')
    gameover=pygame.image.load("gameover.jpg")
    gameover=pygame.transform.scale(background,(width,height))
    #background=pygame.transform.scale(background,(width, height))

    def redraw_window(gameDisplay,player, player2):
        gameDisplay.fill((255,255,255))
        gameDisplay.blit(background,(0,0))

        playerObj = player['player']
        secondPlayerObj = player2['player']

        players=[playerObj, secondPlayerObj]

        if playerObj.dead==True or secondPlayerObj.dead==True:
            endgame()

        playerObj.draw(gameDisplay)
        secondPlayerObj.draw(gameDisplay)

        for bullet in playerObj.projectiles:
            bullet.collides(players)
            if bullet.should_remove():
                playerObj.remove_projectile(bullet)
                continue
            #if bullet.collided==True: #collisions
                #playerObj.remove_projectile(bullet)
                #bullet.collided=False
                #continue
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

        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            p2 = n.send(p)
            secondPlayerObj = p2['player']
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            playerObj.move()
            p['player'] = playerObj
            redraw_window(gameDisplay,p, p2)
            pygame.display.update()

    main()
message=menu(False)
if message==True:
    main_game()
