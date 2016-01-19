import sys
import pygame
import options

Option = options.Option
pygame.init()
#Init variables
gameStatus = 'main'

font = pygame.font.Font(None, 40)
board = pygame.transform.scale(pygame.image.load('Images/board.png'),(600,600))
optionscreen = pygame.display.set_mode((200, 260))

menu = [Option("NEW GAME", (10, 10), font, optionscreen, 0), Option("LOAD GAME", (10, 65), font, optionscreen, 1),
           Option("OPTIONS", (10, 120), font, optionscreen, 2), Option("RULES", (10, 175), font, optionscreen, 3),
           Option("QUIT", (10, 230), font, optionscreen, 4)]
while True:#Main game loop
    
    events = pygame.event.get()
    if(gameStatus == 'main'):#This is true if we're in the main menu
        screen = pygame.display.set_mode((200, 260))
        screen.fill((0, 0, 0))
        for option in menu:#Draw all options on the screen
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
        for ev in events:#Get events and check whether or not a mouseclick was on a button.
            if ev.type == pygame.QUIT:#Allow pygame to be closed with the x
                    sys.exit()
            if ev.type == pygame.MOUSEBUTTONUP:
                for option in menu:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        #Do something with this information, like opening the actual survivor game or opening the rules.
                        #No need for an else, we don't need to know if someone's aim sucks.
                        print(option.id)
                        if(option.id == 0): #New game
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
            screen.blit(board,(0,0))
            for ev in events:#Event listener again.
                keys=pygame.key.get_pressed()
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_ESCAPE:
                        gameStatus = 'main'
                    #print('Forward')
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