import sys
import pygame
import options
import random
from Player import *
from PlayerCards import *
from board import tiles
from elements import diceload, pawnload
from Player import *
from PlayerCards import *

Option = options.Option
pygame.mixer.init()

pygame.init()
#Init variables
gameStatus = 'main'
font = pygame.font.Font(None, 40)

#The board can be resized every moment by declaring the function here
boardVectorSize = {"x": 600, "y": 600}
def setBoardVectorSize(boardVectorSize):
    return pygame.transform.scale(pygame.image.load('Images/board.png'),(boardVectorSize["x"],boardVectorSize["y"]))
board = setBoardVectorSize(boardVectorSize) #Initialize the board size

#The screen can be resized too by declaring the function here
screenVectorSize = {"x": 1000, "y": 700}
def setScreenVectorSize(screenVectorSize):
    return pygame.display.set_mode((screenVectorSize["x"], screenVectorSize["y"]))
screen = setScreenVectorSize(screenVectorSize)

#Define the scoreboard height, that's where the lives and conditions of each player gets displayed
scoreBoardHeight = 100

#Define the images
pawns = {1:pawnload('Images/Blue.png'), 2:pawnload('Images/Red.png'), 3:pawnload('Images/Green.png'), 4:pawnload('Images/Yellow.png')}
dice = {1:diceload('Images/Die-1.png'), 2:diceload('Images/Die-2.png'), 3:diceload('Images/Die-3.png'), 4:diceload('Images/Die-4.png'), 5:diceload('Images/Die-5.png'), 6:diceload('Images/Die-6.png')}
boardtiles = tiles()
pawnLocations = {1:(20,15), 2:(550,15), 3:(550,540), 4:(20,540)}

randomInt = 1
yourChar = None
print (tiles)

menu = [Option("NEW GAME", (10, 10), font, screen, 0), Option("LOAD GAME", (10, 65), font, screen, 1),
           Option("OPTIONS", (10, 120), font, screen, 2), Option("RULES", (10, 175), font, screen, 3),
           Option("QUIT", (10, 230), font, screen, 4)]

players = [Player("Badr Heri",100, 15, PlayerCards.BadrHeri), Player("Manny Pecquiao",150, 15, PlayerCards.MannyPecquiao), 
            Player("Mike Tysen",200, 15, PlayerCards.MikeTysen), Player("Rocky Belboa",250,15,PlayerCards.RockyBelboa), Player("IRON NICOLAAS!",250,15,PlayerCards.RockyBelboa), Player("Daniel Killer",250,15,PlayerCards.RockyBelboa)]

#Draw all player names on the screen
playerLabels = []
playerLabelVector = {"x": 100,"y": 200}#x,y coordinates on the screen for the label to be displayed
generateID = 0 #Generate an ID for each player
for x in players:
    playerLabels.append(Option(x.Name, (playerLabelVector["x"], playerLabelVector["y"]), font, screen, generateID))
    generateID += 1
    playerNameRectWidth = len(x.Name) * 20 
    if playerLabelVector["x"] > 600:
        playerLabelVector["x"] = 50
        playerLabelVector["y"] += 50
    else:
        playerLabelVector["x"] += playerNameRectWidth
amountOfPlayers = generateID #This is the amount of players adding + 1 because it started from ID 0


labelAmountPlayers = []
playerNumber = 1 #Starting with min 1 and max 4 players
amountPlayersLabelVector = {"x": 200,"y": 50}
generateID += 1 #Increment the latest generated id by one so it stays unique
for x in range(0,4):
    labelAmountPlayers.append(Option(str(playerNumber) + ' player', (amountPlayersLabelVector['x'], amountPlayersLabelVector['y']), font, screen, generateID))
    generateID += 1
    playerNumber += 1
    amountPlayersLabelVector['x'] += 150

#Increment the latest generated id and give it to the clickable button
startGameID = generateID + 1
selectScreenButtons = [Option("Start game", (800, 550), font, screen, startGameID)]

entities = [playerLabels, labelAmountPlayers, selectScreenButtons]

def drawOptions(l):
    for option in l:#Draw all options on the screen
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
        else:
            option.hovered = False
        option.draw()   

gameIsRunning = True #If set to False, the game will stop and the program will exit.

while gameIsRunning:#Main game loop
    #Define the event loop here instead of creating one in each gameStatus (e.g. in the main menu, in the game, in the player select menu etc)
    events = pygame.event.get()
    for ev in events:
            if ev.type == pygame.QUIT:
                    gameIsRunning = False

    #Erase screen, fill everything with black
    screen.fill((0, 0, 0))

    #If the user is focussing on the game again than update the screen, so that the user can switch to other programs/software/windows.
    if pygame.mouse.get_focused() or ev.type == pygame.MOUSEBUTTONDOWN:
        setScreenVectorSize(screenVectorSize)
    
    if(gameStatus == 'main'):
        screenVectorSize["x"] = 200
        screenVectorSize["y"] = 260
        
        for option in menu:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()

        if ev.type == pygame.MOUSEBUTTONUP:
            for option in menu:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    #Do something with this information, like opening the actual survivor game or opening the rules.
                    #No need for an else, we don't need to know if someone's aim sucks.
                    if(option.id == 0): #New game
                        gameStatus = 'new'
                    elif(option.id == 1):#Load game
                        pass
                    elif(option.id == 2):#Options
                        pygame.display.toggle_fullscreen
                    elif(option.id == 3):#Rules
                        r = R.rules.LoadAllRules
                    elif(option.id == 4):#Quit
                        gameIsRunning = False
                    option.draw()
    elif(gameStatus == 'new'):
            screenVectorSize["x"] = 1000
            screenVectorSize["y"] = 600

            label = font.render("Choose amount players", 1, (255,255,0))
            screen.blit(label, (350, 10))
            label = font.render("Choose your character", 1, (255,255,0))
            screen.blit(label, (350, 150))
            for entity in entities:
                drawOptions(entity)
                for ev in events:
                    if ev.type == pygame.MOUSEBUTTONUP:
                        for option in entity:
                            if option.rect.collidepoint(pygame.mouse.get_pos()):
                                if option.id <= amountOfPlayers and int(option.id) != startGameID:#Set which character player 1 is.
                                    yourChar = players[option.id] #Set yourChar to the selected player
                                elif option.id == startGameID:
                                    gameStatus = 'Game'
                                option.selected = True
    elif(gameStatus == 'Game'):#This means we're about to start a new game, start initialising the screen and its elements.
            screenVectorSize["x"] = 1000
            screenVectorSize["y"] = 700
            
            screen.blit(board,(0,0))
            dieRect = pygame.Rect((725,50,150,150))
            screen.blit(dice[randomInt], (725,50))

            #draw labels on scoreboard with lifepoints/conditions p/player
            scoreBoardFont = pygame.font.Font(None, 20)
            scoreBoardColor = (255,255,255)

            #default is the player itself   
            currentPlayerCounter = 1
            scoreBoardLabels = []
            name = None
            for x in players:
                if x == yourChar:
                    name = str(x.Name) + " (That's you)"
                    print("You are: " + str(x.Name))
                else:
                    name = str(x.Name)
                scoreBoardLabels.append(scoreBoardFont.render(name + " - Lifepoints: " + str(x.Health) + " | Condition: " + str(x.Condition), 1, (0,0,0)))
                pygame.draw.rect(screen, scoreBoardColor, (0,600,screenVectorSize["x"],scoreBoardHeight), 0)
                currentPlayerCounter += 1

            #Render the players on the score board
            labelPixelHeight = 605 #First label location on the score board
            for label in scoreBoardLabels:
                screen.blit(label, (0, labelPixelHeight)) 
                if labelPixelHeight < 705:
                    labelPixelHeight += 25 #5 pixels difference between each label and 20 pixels for the font size which is 20 now.
                else:
                    #Now it does not fit the score board screen anymore, the height of it got exceeded.
                    #boardHeight += 25 #Let's extend the board height first
                    screenVectorSize["y"] += 25
                    scoreBoardHeight += 25
                    labelPixelHeight += 25
                    
            for pawn in pawns:#Loop for all pawns
                screen.blit(pawns[pawn], (pawnLocations[pawn]))

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
    
pygame.quit()
sys.exit()