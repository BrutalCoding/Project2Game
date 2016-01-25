import sys
import pygame
import options
import random
from board import tiles
from elements import diceload, pawnload


Option = options.Option
pygame.mixer.init()

pygame.init()
#Init variables
gameStatus = 'main'
font = pygame.font.Font(None, 40)
board = pygame.transform.scale(pygame.image.load('Images/board.png'),(600,600))
optionscreen = pygame.display.set_mode((200, 260))
pawns = {1:pawnload('Images/1.jpg'), 2:pawnload('Images/Red.png'), 3:pawnload('Images/Green.png'), 4:pawnload('Images/Yellow.png')}
dice = {1:diceload('Images/Die-1.png'), 2:diceload('Images/Die-2.png'), 3:diceload('Images/Die-3.png'), 4:diceload('Images/Die-4.png'), 5:diceload('Images/Die-5.png'), 6:diceload('Images/Die-6.png')}
boardtiles = tiles()
tempInt = 0
#pawnLocations = {1:boardtiles[tempInt], 2:(0,0), 3:(0,0), 4:(0,0)} #The number is the pawn, the other thing is the location of said pawn.
#pawnLocations = {1:(20,15), 2:(550,15), 3:(550,540), 4:(20,540)}
pawnLocations = {1:boardtiles[1], 2:(0,0), 3:(0,0), 4:(0,0)}
print(boardtiles)

randomInt = 1
amountPlayers = 0
yourChar = 0
chosen = []

print (tiles)

menu = [Option("NEW GAME", (10, 10), font, optionscreen, 0), Option("LOAD GAME", (10, 65), font, optionscreen, 1),
           Option("OPTIONS", (10, 120), font, optionscreen, 2), Option("RULES", (10, 175), font, optionscreen, 3),
           Option("QUIT", (10, 230), font, optionscreen, 4)]

player = [Option('1 player', (200, 50), font, optionscreen, 1), Option('2 players', (350, 50), font, optionscreen, 2),
            Option('3 players', (500, 50), font, optionscreen, 3), Option('4 player', (650, 50), font, optionscreen, 4)]

buttons = [Option("Start game", (800, 550), font, optionscreen, 10)]

characters = [Option('Jacky', (200, 200), font, optionscreen, 5), Option('Daniel', (350, 200), font, optionscreen, 6),
            Option('Iron', (500, 200), font, optionscreen, 7), Option('Bunyamin', (650, 200), font, optionscreen, 8)]

entities = [characters, player, buttons]

def drawOptions(l):
    for option in l:#Draw all options on the screen
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
        else:
            option.hovered = False
        option.draw()   

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
                print('asdf')
                for option in menu:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        #Do something with this information, like opening the actual survivor game or opening the rules.
                        #No need for an else, we don't need to know if someone's aim sucks.
                        print(option.id)
                        if(option.id == 0): #New game
                            gameStatus = 'new'
                        elif(option.id == 1):#Load game
                            gameStatus = 'game'
                        elif(option.id == 2):#Options
                            pass
                        elif(option.id == 3):#Rules
                            r = R.rules.LoadAllRules
                        elif(option.id == 4):#Quit
                            sys.exit(); exit()
                            break
                    option.draw()
    elif(gameStatus == 'new'):
            screen = pygame.display.set_mode((1000, 600))
            label = font.render("Choose amount players", 1, (255,255,0))
            screen.blit(label, (350, 10))
            label = font.render("Choose your character", 1, (255,255,0))
            screen.blit(label, (350, 150))
            for x in entities:
                drawOptions(x)
                for ev in events:
                    if ev.type == pygame.MOUSEBUTTONUP:
                        for option in x:
                            if option.rect.collidepoint(pygame.mouse.get_pos()):
                                if int(option.id) <= 4:
                                    amountPlayers = int(option.id)
                                    chosen.append(amountPlayers)
                                elif int(option.id) > 4 and int(option.id) < 10:
                                    yourCharID = int(option.id)
                                    chosen.append(yourCharID)
                                elif option.id == 10:
                                    gameStatus = 'Game'
                                option.selected = True #Character selection screen
    elif(gameStatus == 'game'):#This means we're about to start a new game, start initialising the screen and its elements.      
             #The number is the pawn, the other thing is the location of said pawn.  
            
            screen.blit(pawns[1], (pawnLocations[1]))
            screen = pygame.display.set_mode((1000, 600))           
            screen.blit(board,(0,0))
            dieRect = pygame.Rect((725,50,150,150))
            ##pygame.draw.rect(screen,(0,255,0),(725,50,150,150))
            screen.blit(dice[randomInt], (725,50))
            for ev in events:#Event listener again.
                keys=pygame.key.get_pressed()
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_ESCAPE:
                        gameStatus = 'main'
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    #print('mouse detect', tempInt, pawnLocations[1])
                    #print(pygame.mouse.get_pos())
                    #tempInt += 1
                    if dieRect.collidepoint(pygame.mouse.get_pos()):
                        for i in range(10):
                            randomInt = random.randint(1,6)
                            for pawn in pawns:#Loop for all pawns
                            #print(pawnLocations[1])
                            #screen.blit(pygame.transform.rotate(pawns[1], 90), (pawnLocations[pawn]))
                                
                                tempInt += randomInt
        
    pygame.display.update()

