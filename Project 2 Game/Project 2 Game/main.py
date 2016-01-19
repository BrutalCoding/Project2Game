import sys
import pygame
import options

Option = options.Option
pygame.init()
#Init variables
main = True
screen = pygame.display.set_mode((200, 260))
font = pygame.font.Font(None, 40)
board = ('Images/board.png')


menu = [Option("NEW GAME", (10, 10), font, screen, 0), Option("LOAD GAME", (10, 65), font, screen, 1),
           Option("OPTIONS", (10, 120), font, screen, 2), Option("RULES", (10, 175), font, screen, 3),
           Option("QUIT", (10, 230), font, screen, 4)]
while True:#Main game loop
    events = pygame.event.get()
    screen.fill((0, 0, 0))
    if(main):#This is true if we're in the main menu
        for option in menu:#Draw all options on the screen
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
        for ev in events:#Get events and check whether or not a mouseclick was on a button.
            if ev.type == pygame.MOUSEBUTTONUP:
                for option in menu:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        #Do something with this information, like opening the actual survivor game or opening the rules.
                        #No need for an else, we don't need to know if someone's aim sucks.
                        print(option.id)
                        if(option.id == 0): #New game
                            main = False
                            gameStatus = 'new'
                        elif(option.id == 1):#Load game
                            pass
                        elif(option.id == 2):#Options
                            pass
                        elif(option.id == 3):#Rules
                            pass
                        elif(option.id == 4):#Quit
                            sys.exit(); exit()
                            break
                    option.draw()

    elif(gameStatus == 'new'):#This means we're about to start a new game, start initialising the screen and its elements.
            screen = pygame.display.set_mode((1000, 600))


    #if(gameStatus == 'new'):
       # pass
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