import pygame
from pygame.locals import *

pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

def text_format(message, textFont, textSize, textColor):

    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

font = "freesansbold.ttf"


clock = pygame.time.Clock()
FPS=60

def main_menu():
    tracker=["start","instructions","quit"]
    pointer=0

    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                    if pointer>0:
                        pointer-=1
                    selected=tracker[pointer]
                    print(pointer)
                    print(tracker[pointer])
                if event.key==pygame.K_DOWN:
                    if pointer<2:
                        pointer+=1
                    selected=tracker[pointer]
                    print(pointer)
                    print(tracker[pointer])
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        print("Start")
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(black)
        title=text_format("Some shooting game", font, 70, yellow)
        if selected=="start":
            text_start=text_format("START", font, 55, white)
        else:
            text_start = text_format("START", font, 55, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 55, white)
        else:
            text_quit = text_format("QUIT", font, 55, black)
        if selected =="instructions":
          text_instructions = text_format("INSTRUCTIONS",font,55,white)
        else:
          text_instructions = text_format("INSTRUCTIONS",font,55,black)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
        instruct_rect=text_instructions.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 420))
        screen.blit(text_instructions, (screen_width/2 - (instruct_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")


main_menu()
pygame.quit()
quit()
