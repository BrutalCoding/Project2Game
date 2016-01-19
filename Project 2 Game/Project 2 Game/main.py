import sys
import pygame
import options

Option = options.Option
pygame.init()

optionsscreen = pygame.display.set_mode((200, 260))
font = pygame.font.Font(None, 40)


menu = [Option("NEW GAME", (10, 10), font, optionsscreen, 0), Option("LOAD GAME", (10, 65), font, optionsscreen, 1),
           Option("OPTIONS", (10, 120), font, optionsscreen, 2), Option("RULES", (10, 175), font, optionsscreen, 3),
           Option("QUIT", (10, 230), font, optionsscreen, 4)]
while True:#Main game loop
    events = pygame.event.get()
    optionsscreen.fill((0, 0, 0))
    for option in menu:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
        else:
            option.hovered = False
        option.draw()

    for ev in events:
        if ev.type == pygame.MOUSEBUTTONUP:
            for option in menu:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    #Do something with this information, like opening the actual survivor game or opening the rules.
                    #No need for an else, we don't need to know if someone's aim sucks.
                    print(option.id)
                    if(option.id == 0): #New game
                        pass
                    elif(option.id == 1):#Load game
                        pass
                    elif(option.id == 2):#Options
                        pass
                    elif(option.id == 3):#Rules
                        pass
                    elif(option.id == 4):#Quit
                        sys.exit()
                
                option.draw()

    pygame.display.update()






#screensize = width, height = 1000, 600
#startmenusize = width, height = 200, 500
#circle = pygame.transform.scale(pygame.image.load('Images/circle.jpg'), (30,30))
#board = pygame.transform.scale(pygame.image.load('Images/board.png'), (600,600))

#startmenu = pygame.display.set_mode()
#screen = pygame.display.set_mode(screensize)
##screen.fill(black)

#def main():
#    while True:#Main game loop
#       screen.blit(board, (0, 0))
#       screen.blit(circle, (10,10))
#       pygame.display.update()
#main()