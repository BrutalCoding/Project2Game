﻿import sys
import pygame
import options
import random
from Player import *
from PlayerCards import *
from board import tiles
from elements import diceload, pawnload, playerload
from Player import *
from PlayerCards import *
from rules import *
from pygame import gfxdraw
from SuperFighters import *
from selectScreen import *
from WindowsScreen import *
from Dice import rollDice
from Draw import *
from Ai import Bot

Option = options.Option
pygame.mixer.init()
pygame.init()

#Init variables
gameStatus = 'main'
AI = Bot
rules = Rules
font = pygame.font.Font(None, 40)
selectedCharacters = [] #List of selected characters from the "new game" screen
selectedAmountBots = None #How many bots he/she wants to play
currentPlayerCounter = 0 #Default player
tempCurrentPlayerCounter = 0 #Only used in the gamestatus 'fight'
defaultPawnLocations = [] #The top left corner but all with a little bit of offset so the pawns are not on top of each other
defaultTileLocations = [] #All tiles that are possible to move on to (with a pawn)
maxAmountOfBots = 4  #MAX 4 OR GIUSEPPE WILL HAVE YOUR TESTICLES          4 is actually 3. Bots means players, really.                                                                                                                                                     #Minimal 1 and maximum depends on how many characters are in the game, see 'players' variable. E.g. 4 = 3 bots, 1 player.
pawnLocationsTiles = {}
scoreBoardHeight = 0 #Define the scoreboard height, that's where the lives and conditions of each player gets displayed
players = Player
randomDiceNumber = 1
firstDieIsThrown = False
mainMenuSize = [800, 600]
background = pygame.image.load("Images\cardboard_texture.jpg")
mainBackground = pygame.image.load("Images\FighterMenu.png")
background = pygame.image.load("Images\Background.png")
selectBackground = pygame.image.load("Images\EmptyBackground.png")
botChosen = False
charChosen = False
tileSelected = False
enableSound = True
fighterDieInt = []
fighterCurrentPlayerCounter = 0 #When a player lands on a corner, this variable will be assigned to the current fighter.
fightAttackIsChosen = False #In the fightscreen, where the player has the option to select an attack
#Font init
pygame.font.init()
font = pygame.font.Font(None, 25)
font_path = "./Fonts/Brushstrike.ttf"
fontSPM = pygame.font.Font(font_path, 35)
font_path = "./Fonts/Superstar.ttf"
font_all = pygame.font.Font(font_path, 40)

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
def  PawnLocations(selectedCharacters, pawns,currentPlayerCounter, randomDiceNumber, firstDieIsThrown, gameStatus, tempCurrentPlayerCounter):
    #Board game main loop. Every movement is here.
    if ev.type == pygame.MOUSEBUTTONDOWN:
        if dieRect.collidepoint(pygame.mouse.get_pos()):
            #randomDiceNumber = random.randint(1,6)
            randomDiceNumber = rollDice(1,6)
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
                    if selectedCharacters[currentPlayerCounter].Tile == boardtiles[5] or selectedCharacters[currentPlayerCounter].Tile == boardtiles[15] or selectedCharacters[currentPlayerCounter].Tile == boardtiles[25] or selectedCharacters[currentPlayerCounter].Tile == boardtiles[35]:
                        superfighter = random.choice(list(SuperFighters))
                        randominteger = random.randint(1,6) #Select random superfighter, soon to be deprecated.
                        damage = superfighter.value[randominteger - 1]
                        print("Fighter is coming! |", superfighter, ' does ', damage)
                        selectedCharacters[currentPlayerCounter].Health -= damage
                    curplaypos = selectedCharacters[currentPlayerCounter].Tile #Current player's position on board
                    if curplaypos in (boardtiles[0], boardtiles[1], boardtiles[9], boardtiles[10], boardtiles[11], boardtiles[19], boardtiles[20], boardtiles[21], boardtiles[29], boardtiles[30], boardtiles[31], boardtiles[39]):
                        if currentPlayerCounter == 0 and (curplaypos == boardtiles[0] or curplaypos == boardtiles[39] or curplaypos == boardtiles[1]):
                            print ("NOT GOING TO FIGHT 1")
                        elif currentPlayerCounter != 0 and curplaypos in (boardtiles[currentPlayerCounter * 10], boardtiles[(currentPlayerCounter * 10) - 1], boardtiles[(currentPlayerCounter * 10) + 1]):
                            print ("NOT GOING TO FIGHT 2")
                        else: #Fight code
                            print('Fight started (else)')
                            setDefaultSoundSystem(enableSound, "Sounds\Fight.mp3")
                            gameStatus = 'fight'
                            #Sequence
                            #Attacker lands on another player's square
                            #Attacker throws die and gets a number
                            #Attacker chooses the amount of damage he'd like to do
                            #Attacker's stamina gets deducted by the amount corresponding to the damage he chose.
                            #Defender throws die and gets number
                            #Defender chooses the amount of damage he'd like to do
                            #Defender's stamina gets deducted by the amount corresponding to the damage he chose.
                            #Game calculates highest damage - lowest damage and deals this to the player with the lowest damage
                            #Preferably make ai choose damage higher than taken damage within stamina limits
            screen.blit(pawns[currentPlayerCounter + 1], currentTile)
            pygame.time.delay(150)
            #If the counter is at the last character, start at the first player again.
            
            
            firstDieIsThrown = True
            if currentPlayerCounter != 1:
                pass
            ###########################AI CONTROL###########################
            print(currentPlayerCounter)
        #if currentPlayerCounter == 0: #Don't call bot to play round, next up is the human player. Finish round as usual.
            if currentPlayerCounter == len(selectedCharacters) - 1: 
                currentPlayerCounter = 0
            else:
                currentPlayerCounter += 1

            if tempCurrentPlayerCounter == len(selectedCharacters) - 1: 
                tempCurrentPlayerCounter = 0
            else:
                tempCurrentPlayerCounter += 1
            #else: #Call bot to play round.
                
            #    randomDiceNumber = botInstances['Bot'+str(currentPlayerCounter-1)].playTurn(gameStatus)

            #    if currentPlayerCounter == len(selectedCharacters) - 1: 
            #        currentPlayerCounter = 0
            #    else:
            #        currentPlayerCounter += 1

            #    if tempCurrentPlayerCounter == len(selectedCharacters) - 1: 
            #        tempCurrentPlayerCounter = 0
            #    else:
            #        tempCurrentPlayerCounter += 1

            return currentPlayerCounter, randomDiceNumber, firstDieIsThrown, gameStatus,tempCurrentPlayerCounter,selectedCharacters[currentPlayerCounter].Health
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
        if randomDiceNumber == None:
                    print("TEST")
        screen.blit(dice[randomDiceNumber], (725,50))
        playersAlive = 0
        for fighter in selectedCharacters:
            if fighter.Health > 0:
                playersAlive += 1
            else:
                fighter.Health = 0 #Reset it to 0 instead of displaying a negative value.
        if playersAlive == 1:
            message = str(selectedCharacters[currentPlayerCounter].Name) + " just won the game!"
            ImageBGLink = "Images/EmptyBackground.png"
            brushLink = "Fonts/Brushstrike.ttf"
            screenMessage = WindowsScreen(screen,message,ImageBGLink,brushLink)
            screen.blit(screenMessage.surf, (0, 0))

    return currentPlayerCounter, randomDiceNumber,firstDieIsThrown,gameStatus,tempCurrentPlayerCounter,selectedCharacters[currentPlayerCounter].Health

#Define and initialize the sounds of the game
pygame.mixer.init()
def setDefaultSoundFadeOut(fadeOutms):
    pygame.mixer.music.fadeout(fadeOutms)
    return True
def setDefaultSoundSystem(enableSound, soundFileLocation, fadeOutms=500, volume=1):
    if(setDefaultSoundFadeOut(fadeOutms)) and enableSound:
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(soundFileLocation)
        pygame.mixer.music.play(-1)
setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)

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
playerImages = {1:playerload('Images/mike.png'), 2:playerload('Images/paquiao.png'), 3:playerload('Images/mohammed.png'), 4:playerload('Images/rocky.png')}
boardtiles = tiles()
players =  [Player("Mohammed Ali",100, 15, PlayerCards.MohammedAli,boardtiles[0],"card__mohammed_ali.png", "mohammed.png", "mohammed.png"),
            Player("Manny Pecquiao",100, 15, PlayerCards.MannyPecquiao,boardtiles[0],"card__manny_pecquiao.png","face__manny_pecquiao.jpg", "paquiao.png"),
            Player("Mike Tysen",100, 15, PlayerCards.MikeTysen,boardtiles[0],"card__mike_tysen.png","face__mike_tysen.jpg", "mike.png"),
            Player("Rocky Belboa",100,15,PlayerCards.RockyBelboa,boardtiles[0],"card__rocky_belboa.png","face__rocky_belboa.jpg", "rocky.png")]
            #Player("Bunya Sakboa",100,15,PlayerCards.RockyBelboa,boardtiles[0],"card__mohammed_ali.png", "face__bunya_sakboa.jpg"),
            #Player("Iron Rekt",100,15,PlayerCards.RockyBelboa,boardtiles[0],"card__mohammed_ali.png","face__iron_reckt.jpg"),
            #Player("Wout The Ripper",100,15,PlayerCards.RockyBelboa,boardtiles[0],"card__mohammed_ali.png"),
            #Player("Bad Boy",100,15,PlayerCards.RockyBelboa,boardtiles[0],"card__mohammed_ali.png")]

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
        playerLabelVector["y"] += 50
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
buttonw = [Option("Disable sound!", (300, 100), font, screen, 99), Option("Enable sound!", (300, 200), font, screen, 98)]
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

    #Update()










    #Everything below this has to be gone and divided over multiple classes. Good fucking luck.


    #Define the event loop here instead of creating one in each gameStatus (e.g. in the main menu, in the game, in the player select menu etc)
    events = pygame.event.get()
    for ev in events:
            if ev.type == pygame.QUIT:
                    gameIsRunning = False

    #Erase screen, fill everything with black
    screen.fill((0,0,0))
# main menu
    #print(gameStatus)
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
                        setDefaultSoundSystem(enableSound,"Sounds\Intro_1_Hyped.mp3", 300)
                        
                    elif(option.id == 1):#Load game
                        pass
                    elif(option.id == 2):#Options
                        gameStatus = "options"
                        screenVectorSize["x"] = mainMenuSize[0]
                        screenVectorSize["y"] = mainMenuSize[1]
                        setScreenVectorSize(screenVectorSize, screen)
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
                setDefaultSoundSystem(enableSound, "Sounds\Intro_Soft_Touch.mp3", 300)
        screen.blit(pygame.transform.scale(selectBackground,(screenVectorSize["x"],screenVectorSize["y"])), (0, 0))
        label = fontSPM.render("Choose bots", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 6, 20))
        label = fontSPM.render("Choose your fighter", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 2, 150))
        
        if latestSelectedChar != None:
            screen.blit(playerImageFaceDict[latestSelectedChar.Name],(100,300)) #Image of the character
            screen.blit(playerImageCardDict[latestSelectedChar.Name],(350,300)) #Image of the score card
            
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
                            setDefaultSoundSystem(enableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                        elif option.id == mainMenuGameID:
                            selectedCharacters, selectedAmountBots, latestSelectedChar = resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar)
                            gameStatus = 'main'
                            setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
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
                setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
                screenVectorSize["x"] = mainMenuSize[0]
                screenVectorSize["y"] = mainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
                selectedCharacters, selectedAmountBots, latestSelectedChar = resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar)
                selectedCharacters = [] #List of selected characters from the "new game" screen
                firstDieIsThrown = False
                yourChar = None
                #latestSelectedChar = None
                player = Player #Reset all lives/conditions etc by recreating the Player class

        if ev.type == pygame.MOUSEBUTTONDOWN:
            clickPosition = pygame.mouse.get_pos()#Check if player tile is selected
            if (clickPosition[0] >= 0 and clickPosition[0] <= 75) and (clickPosition[1] >= 0 and clickPosition[1] <= 75):
                tileSelected = True
                cardName = selectedCharacters[0].Name
            elif (clickPosition[0] >= 525 and clickPosition[0] <= 600) and (clickPosition[1] >= 0 and clickPosition[1] <= 75):
                tileSelected = True
                cardName = selectedCharacters[1].Name
            elif (clickPosition[0] >= 525 and clickPosition[0] <= 600) and (clickPosition[1] >= 525 and clickPosition[1] <= 600):
                if len(selectedCharacters) >= 3:
                    tileSelected = True
                    cardName = selectedCharacters[2].Name
            elif (clickPosition[0] >= 0 and clickPosition[0] <= 75) and (clickPosition[1] >= 525 and clickPosition[1] <= 600):
                if len(selectedCharacters) >= 4:
                    tileSelected = True
                    cardName = selectedCharacters[3].Name
            else:
                print(pygame.mixer.get_num_channels())
                tileSelected = False
        screen.blit(board,(0,0))
        if tileSelected:#If player tile is selected, display character card referenced to character chosen by player
            screen.blit(playerImageCardDict[cardName],(660,289))
        #Return the new player number so that the global variable can be updated instead of local.
        currentPlayerCounter, randomDiceNumber, firstDieIsThrown, gameStatus,tempCurrentPlayerCounter,selectedCharacters[currentPlayerCounter].Health = PawnLocations(selectedCharacters, pawns, currentPlayerCounter, randomDiceNumber,firstDieIsThrown, gameStatus,tempCurrentPlayerCounter)
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
    elif gameStatus == "options":
        label = font.render("Option menu", 1, (255,255,0))
        screen.blit(label, (300, 50))
        geluid = pygame.mixer.get_num_channels()
        selectScreen.drawOptions(buttonw)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for option in buttonw:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    if option.id == 99:
                        enableSound = False
                        pygame.mixer.music.stop()
                    elif option.id == 98:
                        enableSound = True
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                #mainmenusound#
                setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
                screenVectorSize["x"] = mainMenuSize[0]
                screenVectorSize["y"] = mainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
                selectedCharacters, selectedAmountBots = selectScreen.resetSelections(selectedCharacters, selectedAmountBots)
                selectedCharacters = [] #List of selected characters from the "new game" screen
                firstDieIsThrown = False
                yourChar = None
                latestSelectedChar = None
                player = Player #Reset all lives/conditions etc by recreating the Player class
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

    elif gameStatus == "fight":
        dieRect = None
        screen.fill((0,0,0))
        if tempCurrentPlayerCounter == 4:
            tempCurrentPlayerCounter = 3
        else:
            tempCurrentPlayerCounter = currentPlayerCounter - 1
        bottomLeftFighter = tempCurrentPlayerCounter
        ImageFighter = pygame.image.load("Images\\" + selectedCharacters[tempCurrentPlayerCounter].ImageFighter)
        
        landedTile = selectedCharacters[tempCurrentPlayerCounter].Tile

        curplaypos = selectedCharacters[tempCurrentPlayerCounter].Tile #currentPlayerCounter got updated to the next player, but we want the previous player.
        screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + selectedCharacters[tempCurrentPlayerCounter].ImageCard),(250,295)), (screen.get_width() - 250, screen.get_height() - 295))
        
        #Boolean to check if the both players have fought each other
        fightIsOver = False

        
        #Find index number in boardtiles
        for x in boardtiles.items():
            if x[1] == curplaypos:
                if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                    tempCurrentPlayerCounter = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                else:
                    tempCurrentPlayerCounter = 0 #Going to fight player 0 (first player, that means its going to fight you.

        #HP and Condition labels for the player and the owner of the corner
        textPlayerHP = font.render("HP: " + str(selectedCharacters[bottomLeftFighter].Health), 1, (255,255,0))
        textPlayerCondition = font.render("Condition: " + str(selectedCharacters[bottomLeftFighter].Condition), 1, (255,255,0))
        textOpponentHP = font.render("HP: " + str(selectedCharacters[tempCurrentPlayerCounter].Health), 1, (255,255,0))
        textOpponentCondition = font.render("Condition: " + str(selectedCharacters[tempCurrentPlayerCounter].Condition), 1, (255,255,0))

        #Blit the HP/Condition labels
        screen.blit(textPlayerHP, (200,600))
        screen.blit(textPlayerCondition, (200,630))
        screen.blit(textOpponentHP, (650, 35))
        screen.blit(textOpponentCondition, (650,65))

        ImageOpponent = pygame.image.load("Images\\" + selectedCharacters[tempCurrentPlayerCounter].ImageFighter)
        screen.blit(ImageFighter, (0,450)) #Blit attacker in bottom down
        screen.blit(ImageOpponent, (800,0)) #Blit defender in top right

        screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + selectedCharacters[currentPlayerCounter].ImageCard),(250,295)), (0,0))
        
        
        #If the first turn has not begun yet, display a placeholder for the dice. Else show what dice was thrown.
        if fighterCurrentPlayerCounter == 0:
            diePlaceholder = pygame.image.load("Images\\head__iron_rekt.png")
            screen.blit(diePlaceholder, (((screen.get_width() /2)-95), (screen.get_height()/2)-95))
        else:
            screen.blit(dice[fighterDieInt[fighterCurrentPlayerCounter - 1]], (((screen.get_width() /2)-95), (screen.get_height()/2)-95))

        fightDie = pygame.Rect(((screen.get_width() /2)-95), (screen.get_height()/2)-95, 190, 190)
        if fightDie.collidepoint(pygame.mouse.get_pos()) and fighterCurrentPlayerCounter < 2: #If there are still turns left and
            if ev.type == pygame.MOUSEBUTTONDOWN:
                    fighterDieInt.append(random.randint(1,6))
                    pygame.time.delay(150)
                    fighterCurrentPlayerCounter += 1
        if fighterDieInt != [] and fightIsOver == False:
            #When the die is thrown, show which attacks are available.
            attackOptions = selectedCharacters[bottomLeftFighter].Card.value[fighterDieInt[0]]
            textPlayerAttack = []
            textOpponentAttack = []
            if len(fighterDieInt) == 2:
                #For the boxer in the top right corner
                attackOpponentOptions = selectedCharacters[tempCurrentPlayerCounter].Card.value[fighterDieInt[1]]
                cnt = 0
                for attack in attackOpponentOptions.items():
                    textOpponentAttack.append(font.render("Attack " + str(cnt + 1) + ": Damage:" + str(attack[1]['damage']) + " | Condition: " + str(attack[1]['condition']), 1, (255,255,255)))
                    cnt += 1

                #Create clickable rectangles
                labelHeight = 25
                topRightAttackOptions = []
                cnt = 0
                while cnt <= len(textOpponentAttack):
                    topRightAttackOptions.append(pygame.Rect(400,labelHeight,240,20))
                    labelHeight += 25
                    cnt += 1

                #Show what the topright corner boxer has chosen
                cnt = 1
                for attackOption in topRightAttackOptions:
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if attackOption.collidepoint(pygame.mouse.get_pos()):
                            print("You chose: " + str(attackOpponentOptions[cnt]))
                            topRightAttackOptions.clear()
                            topRightAttackOptions.append(attackOpponentOptions[cnt])
                            topRightCornerDamage = attackOpponentOptions[cnt]['damage']
                            topRightCornerCondition = attackOpponentOptions[cnt]['condition']
                            fightIsOver = True
                    cnt += 1
            #For the boxer in the bottom left corner
            cnt = 0
            labelHeight = 600
            for attack in attackOptions.items():
                textPlayerAttack.append(font.render("Attack " + str(cnt + 1) + ": Damage:" + str(attack[1]['damage']) + " | Condition: " + str(attack[1]['condition']),1, (255,255,255)))
                labelHeight += 25
                cnt += 1
            
            labelHeight = 600
            bottomLeftAttackOptions = []
            cnt = 0
            while cnt <= len(textPlayerAttack):
                bottomLeftAttackOptions.append(pygame.Rect(400,labelHeight,240,20))
                labelHeight += 25
                cnt += 1

            cnt = 1
            for attackOption in bottomLeftAttackOptions:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if attackOption.collidepoint(pygame.mouse.get_pos()):
                        print("You chose: " + str(attackOptions[cnt]))
                        bottomLeftAttackOptions.clear()
                        bottomLeftAttackOptions.append(attackOptions[cnt])
                        bottomLeftCornerDamage = attackOptions[cnt]['damage']
                        bottomLeftCornerCondition = attackOptions[cnt]['condition']
                cnt += 1

            labelHeight = 600
            for label in textPlayerAttack:
                screen.blit(label, (400,labelHeight))
                labelHeight += 25
            
            labelHeight = 25
            for label in textOpponentAttack:
                screen.blit(label, (350,labelHeight))
                labelHeight += 25

        #When both players decided which attacks they want, calculate the damage/condition for each player.
        if(fightIsOver):
            bottomLeftFighter = selectedCharacters[bottomLeftFighter]
            topRightFighter = selectedCharacters[tempCurrentPlayerCounter]
            if bottomLeftFighter.Condition >= bottomLeftCornerCondition: #Attacker has enough condition to perform the attack
                if bottomLeftCornerDamage > topRightCornerDamage: #The attackers damage is better than the defender
                    bottomLeftFighter.Condition += bottomLeftCornerCondition #New condition for the attacker
                    if topRightFighter.Condition >= topRightCornerCondition: #Has the opponent enough condition to perform the attack?
                        topRightFighter.Condition += topRightCornerCondition
                        bottomLeftCornerDamage = bottomLeftCornerDamage - topRightCornerDamage #New damage for the attacker
                    else:
                        #The defender has not enough condition to attack back
                        bottomLeftCornerDamage = bottomLeftCornerDamage #Damage remains the same
                    topRightFighter.Health -= bottomLeftCornerDamage
                elif topRightCornerDamage > bottomLeftCornerDamage:
                    bottomLeftFighter.Condition += bottomLeftCornerCondition #New condition for the attacker
                    if topRightFighter.Condition >= topRightCornerCondition: #Has the opponent enough condition to perform the attack?
                        topRightFighter.Condition += topRightCornerCondition
                        topRightCornerDamage = topRightCornerDamage - bottomLeftCornerDamage #New damage for the attacker
                    else:
                        #The defender has not enough condition to attack back
                        topRightCornerDamage = topRightCornerDamage #Damage remains the same
                    bottomLeftFighter.Health -= topRightCornerDamage
            else:
                print("Cannot attack, you have not enough condition left!")

        if(tempCurrentPlayerCounter == 3):
            tempCurrentPlayerCounter = 0

        if currentPlayerCounter == len(selectedCharacters) - 1:
            currentPlayerCounter == 0

        #Player 0 and Player 1 exists, if it is 2 (which means both players have had their turns already) then reset it back to 0 for the next fight
        if fighterCurrentPlayerCounter == 2:
            if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_SPACE:
                    setDefaultSoundSystem(enableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                    fighterCurrentPlayerCounter = 0
                    fighterDieInt = []
                    gameStatus = 'Game'

    Update()
pygame.quit()
sys.exit()