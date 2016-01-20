import sys
import pygame
import options
import random
from board import tiles


Option = options.Option
pygame.mixer.init()
def diceload(file):
    return pygame.transform.scale(pygame.image.load(file), (150,150))
pygame.init()
#Init variables
gameStatus = 'main'
font = pygame.font.Font(None, 40)
board = pygame.transform.scale(pygame.image.load('Images/board.png'),(600,600))
optionscreen = pygame.display.set_mode((200, 260))
dice = {1:diceload('Images/Die-1.png'), 2:diceload('Images/Die-2.png'), 3:diceload('Images/Die-3.png'), 4:diceload('Images/Die-4.png'), 5:diceload('Images/Die-5.png'), 6:diceload('Images/Die-6.png')}
gameElements = {}
randomInt = 1
tiles = {} #test daniel branch






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
                            r = R.rules.LoadAllRules
                        elif(option.id == 4):#Quit
                            sys.exit(); exit()
                            break
                    option.draw()

    elif(gameStatus == 'new'):#This means we're about to start a new game, start initialising the screen and its elements.
            screen = pygame.display.set_mode((1000, 600))
            screen.blit(board,(0,0))
            dieRect = pygame.Rect((725,50,150,150))
            #pygame.draw.rect(screen,(0,255,0),(725,50,150,150))
            screen.blit(dice[randomInt], (725,50))

            for ev in events:#Event listener again.
                keys=pygame.key.get_pressed()
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_ESCAPE:
                        gameStatus = 'main'
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if dieRect.collidepoint(pygame.mouse.get_pos()):
                        for i in range(10):
                            randomInt = random.randint(1,6)
    pygame.display.update()

