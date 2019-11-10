import pygame

def menu(start):
    pygame.init()

    width = 900
    height = 600
    display = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    white=(255, 255, 255)
    black=(0, 0, 0)
    brown=(150,75,0)
    red=(255, 0, 0)
    yellow=(255, 255, 0)
    blue=(0, 0, 255)
    green=(0, 255, 0)
    grey=(128, 128, 128)

    backgrounds=[]

    anime1=pygame.image.load("Images/tmp-0.gif")
    anime2=pygame.image.load('Images/tmp-1.gif')
    anime3=pygame.image.load('Images/tmp-2.gif')
    anime4=pygame.image.load('Images/tmp-3.gif')
    anime5=pygame.image.load('Images/tmp-4.gif')
    anime6=pygame.image.load('Images/tmp-5.gif')
    anime7=pygame.image.load('Images/tmp-6.gif')
    anime8=pygame.image.load('Images/tmp-7.gif')

    backgrounds.append(pygame.transform.scale(anime1,(width,height)))
    backgrounds.append(pygame.transform.scale(anime2,(width,height)))
    backgrounds.append(pygame.transform.scale(anime3,(width,height)))
    backgrounds.append(pygame.transform.scale(anime4,(width,height)))
    backgrounds.append(pygame.transform.scale(anime5,(width,height)))
    backgrounds.append(pygame.transform.scale(anime6,(width,height)))
    backgrounds.append(pygame.transform.scale(anime7,(width,height)))
    backgrounds.append(pygame.transform.scale(anime8,(width,height)))

    def process_text(message, font, size, color):

        new_font = pygame.font.Font(font, size)
        edited = new_font.render(message, 0, color)

        return edited


    font = "Images/arcade.TTF"
    n=0
    def main_menu(n,start):

        tracker=["start","instructions","highscores","quit"]
        pointer=0

        menu=True
        selected="start"

        while menu:
            if n>6:
              n=0
            else:
              n+=1
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

                    if event.key==pygame.K_DOWN:
                        if pointer<3:
                            pointer+=1
                        selected=tracker[pointer]

                    if event.key==pygame.K_RETURN:
                        if selected=="quit":
                            pygame.quit()
                            quit()
                        if selected=="start":
                            print("start")
                            start=True
                            return start

            display.fill(grey)
            display.blit(backgrounds[n],(0,0))
            #title=process_text("Some shooting game", font, 70, yellow)
            if selected=="start":
                text_start=process_text("START", font, 35, white)
            else:
                text_start = process_text("START", font, 35, yellow)
            if selected=="quit":
                text_quit=process_text("QUIT", font, 35, white)
            else:
                text_quit = process_text("QUIT", font, 35, yellow)
            if selected == "highscores":
                text_highscores=process_text("HIGHSCORES", font, 35, white)
            else:
                text_highscores =process_text("HIGHSCORES", font, 35, yellow)

            if selected =="instructions":
              text_instructions = process_text("INSTRUCTIONS",font,35,white)
            else:
              text_instructions = process_text("INSTRUCTIONS",font,35,yellow)

            #title_rect=title.get_rect()
            start_rect=text_start.get_rect()
            quit_rect=text_quit.get_rect()
            highscores_rect=text_highscores.get_rect()
            instruct_rect=text_instructions.get_rect()


            #display.blit(title, (450 - (title_rect[2]/2), 80))
            display.blit(text_start, (450 - (start_rect[2]/2), 100))
            display.blit(text_instructions, (450 - (instruct_rect[2]/2), 140))
            display.blit(text_highscores, (450 - (highscores_rect[2]/2),180))
            display.blit(text_quit, (450 - (quit_rect[2]/2), 220))
            pygame.display.update()
            clock.tick(6)
            pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")

            #return start

            #def return_start(start):
                #return start

    return main_menu(n,start)
    pygame.quit()
#menu(start)
#quit()
