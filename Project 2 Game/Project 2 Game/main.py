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
from rules import *
from pygame import gfxdraw

Option = options.Option
pygame.mixer.init()
pygame.init()

#Init variables
gameStatus = 'main'
rules = Rules
font = pygame.font.Font(None, 40)
selectedCharacters = [] #List of selected characters from the "new game" screen
selectedAmountBots = None #How many bots he/she wants to play
currentPlayerCounter = 1 #Default player
defaultPawnLocations = []
maxAmountOfBots = 8 #Min 1 and maximum depends on how many characters are in the game, see 'players' variable.
pawnLocationsTiles = {}

#The board can be resized every moment by declaring the function here
boardVectorSize = {"x": 600, "y": 600}
def setBoardVectorSize(boardVectorSize):
    return pygame.transform.smoothscale(pygame.image.load('Images/board.png'),(boardVectorSize["x"],boardVectorSize["y"]))
board = setBoardVectorSize(boardVectorSize) #Initialize the board size

#The screen can be resized too by declaring the function here
screenVectorSize = {"x": 200, "y": 260}
def setScreenVectorSize(screenVectorSize, screen):
    background = pygame.image.load("images\cardboard_texture.jpg")
    screen.blit(pygame.transform.scale(background,(screenVectorSize["x"],screenVectorSize["y"])), (0, 0))
    return pygame.display.set_mode((screenVectorSize["x"], screenVectorSize["y"]))
screen = pygame.display.set_mode((screenVectorSize["x"], screenVectorSize["y"]))
screen = setScreenVectorSize(screenVectorSize, screen)

#Define the scoreboard height, that's where the lives and conditions of each player gets displayed
scoreBoardHeight = 0

#Loop through selected characters and place related pawns
def setDefaultPawnLocations(defaultPawnLocations, pawnLocationsTiles):
    for currentPlayer in range(1, len(selectedCharacters) + 1):
        pawnLocationsTiles.update({currentPlayer: (20 + currentPlayer * 5,15 + currentPlayer * 5)})
    for currentPlayer in range(1, len(selectedCharacters) + 1):
        for pawn in pawns:
                if pawn == currentPlayer:
                    pawnLoc = [pawns[pawn], pawnLocationsTiles[pawn]]
                    defaultPawnLocations += pawnLoc    
    return defaultPawnLocations

#Reset the selected and amount of characters to zero again in able to reselect later.
def resetSelections(selectedCharacters, selectedAmountBots):
    if selectedCharacters != None:
        selectedCharacters.clear()
    if selectedAmountBots != None:
        selectedAmountBots = None
    return (selectedCharacters, selectedAmountBots)

#Define the images
pawns = {1:pawnload('Images/Blue.png'), 2:pawnload('Images/Red.png'), 3:pawnload('Images/Green.png'), 4:pawnload('Images/Yellow.png'), 5:pawnload('Images/Blue.png'), 6:pawnload('Images/Red.png'), 7:pawnload('Images/Green.png'), 8:pawnload('Images/Yellow.png')}
dice = {1:diceload('Images/Die-1.png'), 2:diceload('Images/Die-2.png'), 3:diceload('Images/Die-3.png'), 4:diceload('Images/Die-4.png'), 5:diceload('Images/Die-5.png'), 6:diceload('Images/Die-6.png')}
boardtiles = tiles()


#pawnLocations = {1:(20,15), 2:(550,15), 3:(550,540), 4:(20,540), 5: (30,15), 6: (100, 15)}
    

randomInt = 1
yourChar = None
print (tiles)

menu = [Option("NEW GAME", (10, 10), font, screen, 0), Option("LOAD GAME", (10, 65), font, screen, 1),
           Option("OPTIONS", (10, 120), font, screen, 2), Option("RULES", (10, 175), font, screen, 3),
           Option("QUIT", (10, 230), font, screen, 4)]

players =  [Player("Badr Heri",100, 15, PlayerCards.BadrHeri), Player("Manny Pecquiao",150, 15, PlayerCards.MannyPecquiao), 
            Player("Mike Tysen",200, 15, PlayerCards.MikeTysen), Player("Rocky Belboa",250,15,PlayerCards.RockyBelboa), 
            Player("Bunya Sakboa",250,15,PlayerCards.RockyBelboa), Player("Iron Rekt",250,15,PlayerCards.RockyBelboa), 
            Player("Wout The Ripper",250,15,PlayerCards.RockyBelboa), Player("Dane the Banane",250,15,PlayerCards.RockyBelboa)]

#Define entities so that it can also be called again to reset all values such as the selections

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
amountOfCharacters = generateID #This is the amount of players adding + 1 because it started from ID 0


labelAmountPlayers = []
playerNumber = 1 #Starting with min 1 and max 4 players
amountPlayersLabelVector = {"x": 200,"y": 50}
generateID += 1 #Increment the latest generated id by one so it stays unique
labelBotName = "Bot"
for x in range(1,maxAmountOfBots):
    if not playerNumber == 1:
        labelBotName = "Bots"
    labelAmountPlayers.append(Option(str(playerNumber) + ' ' + labelBotName, (amountPlayersLabelVector['x'], amountPlayersLabelVector['y']), font, screen, generateID))
    generateID += 1
    playerNumber += 1
    if amountPlayersLabelVector["x"] > 600:
        amountPlayersLabelVector["x"] = 200
        amountPlayersLabelVector["y"] += 50
    else:
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
    return

gameIsRunning = True #If set to False, the game will stop and the program will exit.
while gameIsRunning:#Main game loop
    #Define the event loop here instead of creating one in each gameStatus (e.g. in the main menu, in the game, in the player select menu etc)
    events = pygame.event.get()
    for ev in events:
            if ev.type == pygame.QUIT:
                    gameIsRunning = False

    #Erase screen, fill everything with black
    screen.fill((0,0,0))

    

    ##Check if the user is focussing on the game again than update the screen, so that the user can switch to other programs/software/windows.
    #if pygame.mouse.get_focused() or ev.type == pygame.MOUSEBUTTONDOWN or (ev.type == pygame.KEYUP and ev.key == pygame.K_ESCAPE):
    #    setScreenVectorSize(screenVectorSize, screen)
      
    if(gameStatus == 'main'):
        screenVectorSize["x"] = 200
        screenVectorSize["y"] = 260
        #Reset option class so no selections get remembered from the previous time that the user selected amount of players and/or character
        for entity in entities:
                for option in entity:
                    option.selected = False

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
                        screenVectorSize["x"] = 1000
                        screenVectorSize["y"] = 600
                        setScreenVectorSize(screenVectorSize, screen)
                    elif(option.id == 1):#Load game
                        pass
                    elif(option.id == 2):#Options
                        pygame.display.toggle_fullscreen
                    elif(option.id == 3):#Rules
                        gameStatus = "rules"
                        screenVectorSize["x"] = 1000
                        screenVectorSize["y"] = 600
                        setScreenVectorSize(screenVectorSize, screen)
                    elif(option.id == 4):#Quit
                        gameIsRunning = False
                    option.draw()

    elif(gameStatus == 'new'):
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                selectedCharacters, selectedAmountBots = resetSelections(selectedCharacters, selectedAmountBots)
                screenVectorSize["x"] = 200
                screenVectorSize["y"] = 260
                setScreenVectorSize(screenVectorSize, screen)
        
        label = font.render("How many bots should play?", 1, (255,255,0))
        screen.blit(label, (350, 10))
        label = font.render("Choose the characters", 1, (255,255,0))
        screen.blit(label, (350, 150))
        

        for entity in entities:
            drawOptions(entity)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for option in entity:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        if option.id > amountOfCharacters and option.id != startGameID: #Set amount of bots
                            if selectedAmountBots != None and selectedAmountBots.id != option.id: #If the player didn't made a choice yet
                                if selectedAmountBots:
                                    selectedAmountBots.selected = False
                                    selectedAmountBots = None
                            option.selected = True
                            selectedAmountBots = option
                        elif option.id <= amountOfCharacters and int(option.id) != startGameID:#Set which character player 1 is.
                            if not players[option.id] in selectedCharacters and selectedAmountBots != None and len(selectedCharacters) < (selectedAmountBots.id - len(players) + 1): #To prevent double (or more) selections, check if the character already got chosen before
                                if len(selectedCharacters) == 0: #Assign first selection to yourChar
                                    yourChar = players[option.id] #Set yourChar to the selected player
                                selectedCharacters.append(players[option.id]) #Add the selected character to the list
                                option.selected = True
                        elif option.id == startGameID and selectedAmountBots != None and len(selectedCharacters) == (selectedAmountBots.id - len(players) + 1):
                            screenVectorSize["x"] = 1000
                            screenVectorSize["y"] = 700
                            setScreenVectorSize(screenVectorSize, screen)
                            gameStatus = 'Game'
                        else:
                            print("Selection menu: Make sure everything is selected.")
            

    elif(gameStatus == 'Game'):#This means we're about to start a new game, start initialising the screen and its elements.
        dieRect = pygame.Rect((725,50,150,150))
        if ev.type == pygame.QUIT:
            gameIsRunning = False
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                screenVectorSize["x"] = 200
                screenVectorSize["y"] = 260
                setScreenVectorSize(screenVectorSize, screen)
                selectedCharacters, selectedAmountBots = resetSelections(selectedCharacters, selectedAmountBots)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if dieRect.collidepoint(pygame.mouse.get_pos()):
                randomInt = random.randint(1,6)
                if currentPlayerCounter == len(selectedCharacters):
                    currentPlayerCounter = 1 #Back to player 1 turn
                else:
                    currentPlayerCounter += 1 #Next player turn

                #After playing turn is determined, add some logic to the game:
                #Hit or kill the current player after its his turn
                #If not dead yet, remove the health with the dice amount
                if not selectedCharacters[currentPlayerCounter - 1].Health <= 0:
                    selectedCharacters[currentPlayerCounter - 1].Health -= randomInt
                else:
                    selectedCharacters[currentPlayerCounter - 1].Health = 0
                pygame.time.delay(75) #The game catches the mousebuttondown event so fast that we need to slow it down.


        screen.blit(board,(0,0))
        dieRect = pygame.Rect((725,50,150,150))
        screen.blit(dice[randomInt], (725,50))

        #draw labels on scoreboard with lifepoints/conditions p/player
        scoreBoardFont = pygame.font.Font(None, 20)
        scoreBoardColor = (255,255,255)

        #default is the player itself
        scoreBoardLabels = []
        name = None
        for x in selectedCharacters:
            if x == yourChar:
                name = str(x.Name) + " (That's you)"
            else:
                name = str(x.Name)
            scoreBoardLabels.append(scoreBoardFont.render(name + " - Lifepoints: " + str(x.Health) + " | Condition: " + str(x.Condition), 1, (0,0,0)))
            pygame.draw.rect(screen, scoreBoardColor, (0,600,screenVectorSize["x"],scoreBoardHeight), 0)

        print(currentPlayerCounter)

        


        #Render the players on the score board
        labelPixelHeight = 605 #First label location on the score board
        scoreBoardHeight = 0
        for label in scoreBoardLabels:
            screen.blit(label, (0, labelPixelHeight)) 
            if labelPixelHeight < 705:
                labelPixelHeight += 25 #5 pixels distance between each label and 20 pixels for the font size which is 20 now.
                scoreBoardHeight += 25
            else:
                #Now it does not fit the score board screen anymore, the height of it got exceeded.
                #boardHeight += 25 #Let's extend the board height first
                if not screenVectorSize["y"] >= labelPixelHeight: #If the window/screen height is NOT good enough
                    screenVectorSize["y"] += 25
                    setScreenVectorSize(screenVectorSize, screen)
                scoreBoardHeight += 25
                labelPixelHeight += 25
        cnt = 0
        #screen.blit(pawns[1], pawnLocations[1])
        
        defaultPawnLocations = setDefaultPawnLocations(defaultPawnLocations, pawnLocationsTiles)
        for x in defaultPawnLocations:
            if cnt == 0:
                source = x
                cnt = 1
            else:
                dest = x
                cnt = 0
                screen.blit(source,(dest[0],dest[1]))
    elif gameStatus == "rules":
        if ev.type == pygame.QUIT:
            gameIsRunning = False
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                screenVectorSize["x"] = 200
                screenVectorSize["y"] = 260
                setScreenVectorSize(screenVectorSize, screen)
        labelHeight = screen.get_rect().midtop[1]
        for rule in rules.LoadAllRules():
            text = font.render(rule, 1, (217, 30, 24))
            textpos = text.get_rect()
            labelHeight += 25
            screen.blit(text, (screen.get_rect().centerx / 2, labelHeight))
        text = font.render("Press 'ESC' to get back to the main menu", 1, (255,255,0))
        textpos = text.get_rect()
        screen.blit(text, (screen.get_rect().centerx / 2, screen.get_size()[1] - 50))
    pygame.display.flip()
pygame.quit()
sys.exit()