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
pygame.font.init()

#Init variables
gameStatus = 'main'
rules = Rules
font = pygame.font.Font(None, 25)
font_path = "./Fonts/Brushstrike.ttf"
fontSPM = pygame.font.Font(font_path, 35)
font_path = "./Fonts/Superstar.ttf"
font_all = pygame.font.Font(font_path, 40)
selectedCharacters = [] #List of selected characters from the "new game" screen
selectedAmountBots = None #How many bots he/she wants to play
currentPlayerCounter = 0 #Default player
defaultPawnLocations = [] #The top left corner but all with a little bit of offset so the pawns are not on top of each other
defaultTileLocations = [] #All tiles that are possible to move on to (with a pawn)
maxAmountOfBots = 4 #Minimal 1 and maximum depends on how many characters are in the game, see 'players' variable. E.g. 4 = 3 bots, 1 player.
pawnLocationsTiles = {}
scoreBoardHeight = 0 #Define the scoreboard height, that's where the lives and conditions of each player gets displayed
players = Player
randomDiceNumber = 1
firstDieIsThrown = False
mainMenuSize = [800, 600]
mainBackground = pygame.image.load("Images\FighterMenu.png")
background = pygame.image.load("Images\Background.png")
selectBackground = pygame.image.load("Images\EmptyBackground.png")
botChosen = False
charChosen = False



#The board can be resized every moment by declaring the function here
boardVectorSize = {"x": 600, "y": 600}
def setBoardVectorSize(boardVectorSize):
    return pygame.transform.smoothscale(pygame.image.load('Images/board.png'),(boardVectorSize["x"],boardVectorSize["y"]))
board = setBoardVectorSize(boardVectorSize) #Initialize the board size

#The screen can be resized too by declaring the function here
screenVectorSize = {"x": mainMenuSize[0], "y": mainMenuSize[1]}
def setScreenVectorSize(screenVectorSize, screen):
    return pygame.display.set_mode((screenVectorSize["x"], screenVectorSize["y"]))
screen = pygame.display.set_mode((screenVectorSize["x"], screenVectorSize["y"]))
screen = setScreenVectorSize(screenVectorSize, screen)

#Loop through selected characters and place related pawns
def PawnLocations(selectedCharacters, pawns,currentPlayerCounter, randomDiceNumber, firstDieIsThrown):
    #Board game main loop. Every movement is here.
    if ev.type == pygame.MOUSEBUTTONDOWN:
        if dieRect.collidepoint(pygame.mouse.get_pos()):
            randomDiceNumber = random.randint(1,6)
            currentTile = selectedCharacters[currentPlayerCounter].Tile
            for x in boardtiles.items():
                if x[1] == currentTile:
                    #To prevent that newTileNumber gets number 40 (Since it goes from 0 to 39)
                    if x[0] + randomDiceNumber < 40:
                        newTileNumber = x[0] + randomDiceNumber
                    else:
                        newTileNumber = 0
                    print("Player #" + str(currentPlayerCounter) +  " - Current tile: " + str(x[1]) + " - Next tile: " + str(boardtiles[newTileNumber]))
                    selectedCharacters[currentPlayerCounter].Tile = boardtiles[newTileNumber]
                    print("Player #" + str(currentPlayerCounter) +  " moved to next tile: " + str(boardtiles[newTileNumber]))
            screen.blit(pawns[currentPlayerCounter + 1], currentTile)
            pygame.time.delay(150)
            #If the counter is at the last character, start at the first player again.
            if currentPlayerCounter == len(selectedCharacters) - 1: 
                currentPlayerCounter = 0
            else:
                currentPlayerCounter += 1
            firstDieIsThrown = True
            return currentPlayerCounter, randomDiceNumber, firstDieIsThrown
    elif( pygame.key.get_pressed()[pygame.K_SPACE] != 0 ):
        print("SPACE PRESSED")
        currentTile = selectedCharacters[currentPlayerCounter].Tile
        for x in boardtiles.items():
            if x[1] == currentTile:
                #To prevent that newTileNumber gets number 40 (Since it goes from 0 to 39)
                if x[0] + 1 != 40:
                    newTileNumber = x[0] + 1
                else:
                    newTileNumber = 0
                print("Player #" + str(currentPlayerCounter) +  " - Current tile: " + str(x[1]) + " - Next tile: " + str(boardtiles[newTileNumber]))
                selectedCharacters[currentPlayerCounter].Tile = boardtiles[newTileNumber]
                print("Player #" + str(currentPlayerCounter) +  " moved to next tile: " + str(boardtiles[newTileNumber]))
        screen.blit(pawns[currentPlayerCounter + 1], currentTile)
        pygame.time.delay(150)

        #If the counter is at the last character, start at the first player again.
        if currentPlayerCounter == len(selectedCharacters) - 1: 
            currentPlayerCounter = 0
        else:
            currentPlayerCounter += 1
        return currentPlayerCounter, randomDiceNumber,firstDieIsThrown
    else:
        #Update player position
        cntCorner = 1
        cntPlayer = 1
        for p in selectedCharacters:
            if not firstDieIsThrown:
                #If no one has thrown the die yet, give each player their own tile.
                if cntCorner == 1:
                    moveToTile = boardtiles[0]
                elif cntCorner == 2:
                    moveToTile = boardtiles[10]
                elif cntCorner == 3:
                    moveToTile = boardtiles[20]
                elif cntCorner == 4:
                    moveToTile = boardtiles[30]

                #Reset to corner 1 if the latest corner (4) has been reached already.
                if cntCorner == 4:
                    cntCorner = 1
                else:
                    cntCorner += 1
            else:
                moveToTile = p.Tile
            p.Tile = moveToTile
            screen.blit(pawns[cntPlayer], moveToTile)
            cntPlayer += 1
        screen.blit(dice[randomDiceNumber], (725,50))

    return currentPlayerCounter, randomDiceNumber,firstDieIsThrown

#Define and initialize the sounds of the game
pygame.mixer.init()
def setDefaultSoundFadeOut(fadeOutms):
    pygame.mixer.music.fadeout(fadeOutms)
    return True
def setDefaultSoundSystem(soundFileLocation, fadeOutms=500, volume=1):
    if(setDefaultSoundFadeOut(fadeOutms)):
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(soundFileLocation)
        pygame.mixer.music.play(-1)
    return
setDefaultSoundSystem("Sounds\Intro_Soft_Touch.mp3", 1000)

#Reset the selected and amount of characters to zero again in able to reselect later.
def resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar):
    if selectedCharacters is not None:
        selectedCharacters.clear()
    if selectedAmountBots is not None:
        selectedAmountBots = None
    if latestSelectedChar is not None:
        latestSelectedChar = None
    return (selectedCharacters, selectedAmountBots, latestSelectedChar)

randomInt = 1
yourChar = None #First selection made is the player
latestSelectedChar = None #Latest character selection that was made

# A global dict value that will contain all the Pygame
# Surface objects returned by pygame.image.load().
xM = 85
menu =    [Option("NEW GAME", (screen.get_rect().centerx - xM, 180), font_all, screen, 0),
           Option("LOAD GAME", (screen.get_rect().centerx - xM, 240), font_all, screen, 1),
           Option("OPTIONS", (screen.get_rect().centerx - xM, 300), font_all, screen, 2),
           Option("RULES", (screen.get_rect().centerx - xM, 360), font_all, screen, 3),
           Option("QUIT", (screen.get_rect().centerx - xM, 420), font_all, screen, 4)]

#Define the images
pawns =     {1:pawnload('Images/Blue.png'), 2:pawnload('Images/Red.png'), 3:pawnload('Images/Green.png'), 4:pawnload('Images/Yellow.png'), 5:pawnload('Images/Blue.png'), 6:pawnload('Images/Red.png'), 7:pawnload('Images/Green.png'), 8:pawnload('Images/head__iron_rekt.png')}
dice =      {1:diceload('Images/Die-1.png'), 2:diceload('Images/Die-2.png'), 3:diceload('Images/Die-3.png'), 4:diceload('Images/Die-4.png'), 5:diceload('Images/Die-5.png'), 6:diceload('Images/Die-6.png')}
boardtiles = tiles()
players =  [Player("Muhammad Ali",100, 15, PlayerCards.BadrHeri,boardtiles[0],"card__badr_heri.jpg", "muhammed_ali.png"),
            Player("Manny Pecquiao",150, 15, PlayerCards.MannyPecquiao,boardtiles[0],"card__manny_pecquiao.jpg","pecquiao.png"),
            Player("Mike Tysen",200, 15, PlayerCards.MikeTysen,boardtiles[0],"card__mike_tysen.jpg","mike.png"),
            Player("Rocky Belboa",250,15,PlayerCards.RockyBelboa,boardtiles[0],"card__rocky_belboa.jpg","rocky.png")]

#Load all images from the Player class
playerImageCardDict = {}
playerImageFaceDict = {}
for player in players:
    playerImageCardDict.update({player.Name: pygame.transform.smoothscale(pygame.image.load("Images\\" + player.ImageCard), (250,300))})
    playerImageFaceDict.update({player.Name: pygame.transform.smoothscale(pygame.image.load("Images\\" + player.ImageFace), (250,300))})

#Define entities so that it can also be called again to reset all values such as the selections

#Draw all player names on the screen
playerLabels = []
playerLabelVector = {"x": 100,"y": 200}#x,y coordinates on the screen for the label to be displayed
generateID = 0 #Generate an ID for each player
for x in players:
    playerLabels.append(Option(x.Name, (playerLabelVector["x"], playerLabelVector["y"]), font, screen, generateID))
    generateID += 1
    playerNameRectWidth = len(x.Name) * 15 
    if playerLabelVector["x"] > 600:
        playerLabelVector["x"] = 50
    else:
        playerLabelVector["x"] += playerNameRectWidth
amountOfCharacters = generateID #This is the amount of players adding + 1 because it started from ID 0


labelAmountPlayers = []
playerNumber = 1 #Starting with min 1 and max 4 players
amountPlayersLabelVector = {"x": 150,"y": 50}
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
mainMenuGameID = startGameID + 1
selectScreenButtons = [Option("Start game", (575, 550), font_all, screen, startGameID),
                       Option("Main", (25, 550), font_all, screen, mainMenuGameID)] # go back to main menu
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

#--------------------#
# ↓ Main game loop ↓ #
#--------------------#
while gameIsRunning:
    #Define the event loop here instead of creating one in each gameStatus (e.g. in the main menu, in the game, in the player select menu etc)
    events = pygame.event.get()
    for ev in events:
            if ev.type == pygame.QUIT:
                    gameIsRunning = False

    #Erase screen, fill everything with black
    screen.fill((0,0,0))
# main menu
    if(gameStatus == 'main'):
        screen.blit(pygame.transform.scale(mainBackground,(screenVectorSize["x"],screenVectorSize["y"])), (0, 0))
        #screenVectorSize["x"] = 200
        #screenVectorSize["y"] = 260
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
                    if(option.id == 0): #New game
                        gameStatus = 'new'
                        screenVectorSize["x"] = mainMenuSize[0]
                        screenVectorSize["y"] = mainMenuSize[1]
                        setScreenVectorSize(screenVectorSize, screen)
                        setDefaultSoundSystem("Sounds\Intro_1_Hyped.mp3", 1000)
                        
                    elif(option.id == 1):#Load game
                        pass
                    elif(option.id == 2):#Options
                        pass
                    elif(option.id == 3):#Rules
                        gameStatus = "rules"
                        screenVectorSize["x"] = mainMenuSize[0]
                        screenVectorSize["y"] = mainMenuSize[1]
                        setScreenVectorSize(screenVectorSize, screen)
                    elif(option.id == 4):#Quit
                        gameIsRunning = False
                    option.draw()
# New game/ select player
    elif(gameStatus == 'new'):
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                selectedCharacters, selectedAmountBots, latestSelectedChar = resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar)
                screenVectorSize["x"] = mainMenuSize[0]
                screenVectorSize["y"] = mainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
                setDefaultSoundSystem("Sounds\Intro_Soft_Touch.mp3", 1000)

        screen.blit(pygame.transform.scale(selectBackground,(screenVectorSize["x"],screenVectorSize["y"])), (0, 0))
        label = fontSPM.render("Choose bots", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 6, 20))
        label = fontSPM.render("Choose your fighter", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 2, 150))
        

        if latestSelectedChar != None:
            screen.blit(playerImageFaceDict[latestSelectedChar.Name],(100,300)) #Image of the character
            screen.blit(playerImageCardDict[latestSelectedChar.Name],(350,300)) #Image of the score card

        playerX = 70
        for fighter in players:
                screen.blit(playerImageFaceDict[fighter.Name],(playerX,200))
                playerX += 200

        for entity in entities:
            drawOptions(entity)

            if botChosen == True:
                selectchar = font.render("Make sure a bot is selected", 1,(255,0,0))
                screen.blit(selectchar, (screen.get_rect().centerx / 2, 500))
            elif charChosen == True:
                selectchar = font.render("Make sure a character is selected", 1,(255,0,0))
                screen.blit(selectchar, (screen.get_rect().centerx / 2, 500))

            if ev.type == pygame.MOUSEBUTTONDOWN:
                for option in entity:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        if option.id > amountOfCharacters and option.id != startGameID and option.id != mainMenuGameID: #Set amount of bots
                            if selectedAmountBots != None and selectedAmountBots.id != option.id: #If the player didn't made a choice yet
                                if selectedAmountBots:
                                    selectedAmountBots.selected = False
                                    selectedAmountBots = None
                            selectedAmountBots = option
                            yourChar = None
                            latestSelectedChar = None
                            selectedCharacters = []
                            botChosen = False
                            for character in entities[0]:
                                character.selected = False
                            option.selected = True
                        elif option.id <= amountOfCharacters and int(option.id) != startGameID and option.id != mainMenuGameID:#Set which character player 1 is.
                            #To prevent double (or more) selections, check if the character already got chosen before
                            if not players[option.id] in selectedCharacters and selectedAmountBots != None and len(selectedCharacters) < (selectedAmountBots.id - len(players) + 1): 
                                if len(selectedCharacters) == 0: #Assign first selection to yourChar
                                    yourChar = players[option.id] #Set yourChar to the selected player
                                
                                latestSelectedChar = players[option.id]
                                charChosen = False
                                selectedCharacters.append(latestSelectedChar) #Add the selected character to the list
                                option.selected = True
                        elif option.id == startGameID and selectedAmountBots != None and len(selectedCharacters) == (selectedAmountBots.id - len(players) + 1):
                            screenVectorSize["x"] = 1000
                            screenVectorSize["y"] = 600
                            setScreenVectorSize(screenVectorSize, screen)
                            gameStatus = 'Game'
                            setDefaultSoundSystem("Sounds\Intro_1_Soft_Pump.mp3", 1000, 0.3)
                        elif option.id == mainMenuGameID:
                            selectedCharacters, selectedAmountBots, latestSelectedChar = resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar)
                            gameStatus = 'main'
                            setDefaultSoundSystem("Sounds\Intro_Soft_Touch.mp3", 1000)
                        else:
                            if selectedAmountBots == None:#check if bot is selected
                                botChosen = True
                            elif latestSelectedChar == None:# check if character is selected
                                charChosen = True
            
# Display board game
    elif(gameStatus == 'Game'):#This means we're about to start a new game, start initialising the screen and its elements.
        dieRect = pygame.Rect((725,50,150,150))
        if ev.type == pygame.QUIT:
            gameIsRunning = False
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                setDefaultSoundSystem("Sounds\Intro_Soft_Touch.mp3", 1000)
                screenVectorSize["x"] = mainMenuSize[0]
                screenVectorSize["y"] = mainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
                selectedCharacters, selectedAmountBots, latestSelectedChar = resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar)
                selectedCharacters = [] #List of selected characters from the "new game" screen
                firstDieIsThrown = False
                yourChar = None
                player = Player #Reset all lives/conditions etc by recreating the Player class
        screen.blit(board,(0,0))

        #Return the new player number so that the global variable can be updated instead of local.
        currentPlayerCounter, randomDiceNumber, firstDieIsThrown = PawnLocations(selectedCharacters, pawns, currentPlayerCounter, randomDiceNumber,firstDieIsThrown)
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
            if x == selectedCharacters[currentPlayerCounter]:
                labelColor = (217, 30, 24) #'Thunderbird' red
            else:
                labelColor = (0,0,0) #Black
            scoreBoardLabels.append(scoreBoardFont.render(name + " - Lifepoints: " + str(x.Health) + " | Condition: " + str(x.Condition), 1, labelColor))
            pygame.draw.rect(screen, scoreBoardColor, (0,600,screenVectorSize["x"],scoreBoardHeight), 0)

        #Render the players on the score board
        labelPixelHeight = 605 #First label location on the score board
        scoreBoardHeight = 0
        for label in scoreBoardLabels:
            screen.blit(label, (0, labelPixelHeight)) 
            if labelPixelHeight < screenVectorSize["y"]:
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
# display rules
    elif gameStatus == "rules":
        screen.blit(pygame.transform.scale(selectBackground,(screenVectorSize["x"],screenVectorSize["y"])), (0, 0))
        if ev.type == pygame.QUIT:
            gameIsRunning = False
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                screenVectorSize["x"] = mainMenuSize[0]
                screenVectorSize["y"] = mainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
        labelHeight = screen.get_rect().midtop[1]
        for rule in rules.LoadAllRules():
            text = font.render(rule, 1, (217, 30, 24))
            textpos = text.get_rect()
            labelHeight += 25
            screen.blit(text, (screen.get_rect().centerx / 4, labelHeight))
        text = font.render("Press 'ESC' to get back to the main menu", 1, (255,255,0))
        textpos = text.get_rect()
        screen.blit(text, (screen.get_rect().centerx / 4, screen.get_size()[1] - 50))
    pygame.display.flip()
pygame.quit()
sys.exit()