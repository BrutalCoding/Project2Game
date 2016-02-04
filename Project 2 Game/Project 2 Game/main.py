import sys
import pygame
import options
import random
import pickle
import os
import webbrowser
from Draw import *
from Player import *
from PlayerCards import *
from board import *
from elements import *
from pygame import gfxdraw
from SuperFighters import *
from selectScreen import *
from WindowsScreen import *
from Dice import rollDice

Option = options.Option
pygame.mixer.init()
pygame.init()

#Init variables
gameStatus = 'main'
selectedCharacters = [] #List of selected characters from the "new game" screen
selectedAmountBots = None #How many bots he/she wants to play
currentPlayerCounter = 0 #Default player
tempCurrentPlayerCounter = 0 #Only used in the gamestatus 'fight'
defaultPawnLocations = [] #The top left corner but all with a little bit of offset so the pawns are not on top of each other
defaultTileLocations = [] #All tiles that are possible to move on to (with a pawn)
maxAmountOfBots = 4  #MAX 4 OR GIUSEPPE WILL HAVE YOUR TESTICLES          4 is actually 3. Bots means players, really.                                                                                                                                                     #Minimal 1 and maximum depends on how many characters are in the game, see 'players' variable. E.g. 4 = 3 bots, 1 player.
scoreBoardHeight = 0 #Define the scoreboard height, that's where the lives and conditions of each player gets displayed
randomDiceNumber = 1
firstDieIsThrown = False
mainMenuSize = [800, 600]
botChosen = False
charChosen = False
tileSelected = False
enableSound = True
ruleOpened = False
fighterDieInt = []
fighterCurrentPlayerCounter = 0 #When a player lands on a corner, this variable will be assigned to the current fighter.
fightAttackIsChosen = False #In the fightscreen, where the player has the option to select an attack
playersAlive = 0
counter = 0
#fightIsOver = False #Boolean to check if the both players have fought each other

diceSound = pygame.mixer.Sound(os.path.join('Sounds','dice_throw.wav'))
bellSound = pygame.mixer.Sound(os.path.join('Sounds','boxing-bell.wav'))

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
def  PawnLocations(selectedCharacters,currentPlayerCounter, randomDiceNumber, firstDieIsThrown, gameStatus, tempCurrentPlayerCounter, playersAlive):
    #Board game main loop. Every movement is here.
    if ev.type == pygame.MOUSEBUTTONDOWN:
        if dieRect.collidepoint(pygame.mouse.get_pos()):
            if selectedCharacters[currentPlayerCounter].Health > 0:
                randomDiceNumber = random.randint(1,6)
                diceSound.play()
                #check steps and ad condition
                newSteps = selectedCharacters[currentPlayerCounter].Steps + randomDiceNumber
                if newSteps >= 40:
                    selectedCharacters[currentPlayerCounter].Condition = 15
                    selectedCharacters[currentPlayerCounter].Steps = 0
                    if newSteps > 40:
                        difference = newSteps - 40
                        selectedCharacters[currentPlayerCounter].Steps += difference
                else:
                    selectedCharacters[currentPlayerCounter].Steps += randomDiceNumber

                currentTile = selectedCharacters[currentPlayerCounter].Tile
                for x in boardtiles.items():
                    if x[1] == currentTile:
                        #To prevent that newTileNumber gets number 40 (Since it goes from 0 to 39)
                        if x[0] + randomDiceNumber < 40:
                            newTileNumber = x[0] + randomDiceNumber
                        else:
                            newTileNumber = 0
                        for pawn in selectedCharacters:
                            if pawn.Name != selectedCharacters[currentPlayerCounter].Name:
                                if boardtiles[newTileNumber] == pawn.Tile and pawn.Health > 0 and boardtiles[newTileNumber] != boardtiles[5] and boardtiles[newTileNumber] != boardtiles[15] and boardtiles[newTileNumber] != boardtiles[25] and boardtiles[newTileNumber] != boardtiles[35]:#If there are 2 pawns on the same tile and the tile is not a fight tile. 
                                    gameStatus = 'fight'
                        selectedCharacters[currentPlayerCounter].Tile = boardtiles[newTileNumber]
                        if selectedCharacters[currentPlayerCounter].Tile == boardtiles[5] or selectedCharacters[currentPlayerCounter].Tile == boardtiles[15] or selectedCharacters[currentPlayerCounter].Tile == boardtiles[25] or selectedCharacters[currentPlayerCounter].Tile == boardtiles[35]:
                            gameStatus = "superfight"
                        curplaypos = selectedCharacters[currentPlayerCounter].Tile #Current player's position on board
                        if curplaypos in (boardtiles[0], boardtiles[1], boardtiles[9], boardtiles[10], boardtiles[11], boardtiles[19], boardtiles[20], boardtiles[21], boardtiles[29], boardtiles[30], boardtiles[31], boardtiles[39]):
                            if currentPlayerCounter == 0 and (curplaypos == boardtiles[0] or curplaypos == boardtiles[39] or curplaypos == boardtiles[1]):
                                #Add HP to the owner
                                playerHP = selectedCharacters[currentPlayerCounter].Health  
                                if playerHP + 10 <= 100:
                                    selectedCharacters[currentPlayerCounter].Health += 10
                                elif playerHP + 10 > 100:
                                    selectedCharacters[currentPlayerCounter].Health = 100
                            elif currentPlayerCounter != 0 and curplaypos in (boardtiles[currentPlayerCounter * 10], boardtiles[(currentPlayerCounter * 10) - 1], boardtiles[(currentPlayerCounter * 10) + 1]):
                                #Add HP to the owner
                                playerHP = selectedCharacters[currentPlayerCounter].Health  
                                if playerHP + 10 <= 100:
                                    selectedCharacters[currentPlayerCounter].Health += 10
                                elif playerHP + 10 > 100:
                                    selectedCharacters[currentPlayerCounter].Health = 100
                            else: #Fight code
                                for x in boardtiles.items():
                                    if x[1] == curplaypos:
                                        if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                                            currentTileOwner = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                                        else:
                                            currentTileOwner = 0 #Going to fight player 0 (first player, that means its going to fight you.
                                if currentTileOwner < len(selectedCharacters):
                                    if selectedCharacters[currentTileOwner].Health > 0:
                                        setDefaultSoundSystem(enableSound, "Sounds\Fight.mp3")
                                        gameStatus = 'fight'
                                    else:
                                        gameStatus = "Game"
                                else:
                                    selectedCharacters[currentPlayerCounter].Health -= 10
                screen.blit(pawnload('Images/' + selectedCharacters[currentPlayerCounter].ImageFace), currentTile)
                pygame.time.delay(150)
                #If the counter is at the last character, start at the first player again.
                firstDieIsThrown = True
                if currentPlayerCounter == len(selectedCharacters) - 1: 
                    currentPlayerCounter = 0
                else:
                    if selectedCharacters[currentPlayerCounter + 1].Health > 0:
                        currentPlayerCounter += 1
                    elif selectedCharacters[currentPlayerCounter]:
                        currentPlayerCounter += 2

                if tempCurrentPlayerCounter == len(selectedCharacters) - 1: 
                    tempCurrentPlayerCounter = 0
                else:
                    tempCurrentPlayerCounter += 1
        return currentPlayerCounter, randomDiceNumber, firstDieIsThrown, gameStatus,tempCurrentPlayerCounter,selectedCharacters[currentPlayerCounter].Health, playersAlive
    else:
        #Update player position
        cntCorner = 1
        cntPlayer = 1

        for p in selectedCharacters:
            if not firstDieIsThrown:
                p.Health = 100
                p.Condition = 15
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
            if p.Health > 0:
                screen.blit(pawnload('Images/' + p.ImageFace), moveToTile)
            cntPlayer += 1
        screen.blit(dice[randomDiceNumber], (725,50))
        playersAlive = 0
        cnt = 0
        for fighter in selectedCharacters:
            if fighter.Health > 0:
                playersAlive += 1
            else:
                fighter.Health = 0 #Reset it to 0 instead of displaying a negative value.
                fighter.IsAlive = False
            if not fighter.Condition > 0:
                fighter.Condition = 0
            if cnt < len(selectedCharacters):
                cnt += 1
        if playersAlive == 1:
            for x in selectedCharacters:
                if x.IsAlive:
                    message = str(x.Name) + " just won the game!"
            ImageBGLink = "Images/EmptyBackground.png"
            brushLink = "Fonts/Brushstrike.ttf"
            screenMessage = WindowsScreen(screen,message,ImageBGLink,brushLink)
            screen.blit(screenMessage.surf, (0, 0))
    return currentPlayerCounter, randomDiceNumber,firstDieIsThrown,gameStatus,tempCurrentPlayerCounter,selectedCharacters[currentPlayerCounter].Health, playersAlive

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

randomInt = 1
yourChar = None #First selection made is the player
latestSelectedChar = None #Latest character selection that was made

# A global dict value that will contain all the Pygame
# Surface objects returned by pygame.image.load().
xM = 85
menu =    [Option("NEW GAME", (screen.get_rect().centerx - xM, 180), Option.fontSize(40, "Super"), screen, 0),
           Option("LOAD GAME", (screen.get_rect().centerx - xM, 240), Option.fontSize(40, "Super"), screen, 1),
           Option("OPTIONS", (screen.get_rect().centerx - xM, 300), Option.fontSize(40, "Super"), screen, 2),
           Option("RULES", (screen.get_rect().centerx - xM, 360), Option.fontSize(40, "Super"), screen, 3),
           Option("QUIT", (screen.get_rect().centerx - xM, 420), Option.fontSize(40, "Super"), screen, 4)]

#Define the images
dice =      {1:diceload('Images/Die-1.png'), 2:diceload('Images/Die-2.png'), 3:diceload('Images/Die-3.png'), 4:diceload('Images/Die-4.png'), 5:diceload('Images/Die-5.png'), 6:diceload('Images/Die-6.png')}
boardtiles = Board.tiles()

players =  [Player("Mohammed Ali",100, 15, PlayerCards.MohammedAli,boardtiles[0], 0,"card__mohammed_ali.png", "muhammed_face.png", "muhammed_ali.png", "MuhammedGlow.png"),
            Player("Manny Pecquiao",100, 15, PlayerCards.MannyPecquiao,boardtiles[0], 0,"card__manny_pecquiao.png","manny_face.png", "paquiao.png", "PecquiaoGlow.png"),
            Player("Mike Tysen",100, 15, PlayerCards.MikeTysen,boardtiles[0], 0,"card__mike_tysen.png","mike_face.png", "mike.png", "MikeGlow.png"),
            Player("Rocky Belboa",100,15,PlayerCards.RockyBelboa,boardtiles[0], 0,"card__rocky_belboa.png","rocky_face.png", "rocky.png", "RockyGlow.png")]

#Load all images from the Player class
playerImageCardDict = {}
playerImageFaceDict = {}
playerImageFighterDict = {}
PlayerImageFighterSelectedDict = {}
for player in players:
    playerImageCardDict.update({player.Name: pygame.transform.smoothscale(pygame.image.load("Images\\" + player.ImageCard), (250,300))})
    playerImageFaceDict.update({player.Name: pygame.transform.smoothscale(pygame.image.load("Images\\" + player.ImageFace), (50,50))})
    playerImageFighterDict.update({player.Name: pygame.transform.smoothscale(pygame.image.load("Images\\" + player.ImageFighter), (150,200))})
    PlayerImageFighterSelectedDict.update({player.Name: pygame.transform.smoothscale(pygame.image.load("Images\\" + player.ImageFighterSelected), (150,200))})
#Define entities so that it can also be called again to reset all values such as the selections

#Draw all player names on the screen
playerLabels = selectScreen.makePlayerLabels(players, Option, screen)
generateID = playerLabels[1]
amountOfCharacters = generateID

#Draw all bots on the screen
labelAmountPlayers = selectScreen.makeBotLabels(generateID, maxAmountOfBots, screen, Option)
generateID = labelAmountPlayers[1]

#Increment the latest generated id and give it to the clickable button
startGameID = generateID + 1
mainMenuGameID = startGameID + 1
selectScreenButtons = [Option("Start game", (575, 550), Option.fontSize(40, "Super"), screen, startGameID),
                       Option("Main", (25, 550), Option.fontSize(40, "Super"), screen, mainMenuGameID)] # go back to main menu
buttonsOptionScreen = [Option("Disable sound!", (300, 150), Option.fontSize(30, "Super"), screen, 99), Option("Enable sound!", (300, 200), Option.fontSize(30, "Super"), screen, 98), Option("Main", (25, 550), Option.fontSize(40, "Super"), screen, mainMenuGameID)]
entities = [playerLabels[0], labelAmountPlayers[0], selectScreenButtons]

gameIsRunning = True #If set to False, the game will stop and the program will exit.

#--------------------#
# ↓ Main game loop ↓ #
#--------------------#
while gameIsRunning:
    events = pygame.event.get()
    for ev in events:
            if ev.type == pygame.QUIT:
                    gameIsRunning = False
    screen.fill((0,0,0))
    #Main menu
    if(gameStatus == 'main'):
        Draw.drawImage(screen, "FighterMenu.png", (screenVectorSize["x"],screenVectorSize["y"]), (0, 0))
        for entity in entities:
                for option in entity:
                    option.selected = False
        selectScreen.drawOptions(menu)
        if ev.type == pygame.MOUSEBUTTONUP:
            for option in menu:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    if(option.id == 0):#New game
                        gameStatus = 'new'
                        screenVectorSize["x"] = mainMenuSize[0]
                        screenVectorSize["y"] = mainMenuSize[1]
                        setScreenVectorSize(screenVectorSize, screen)
                        setDefaultSoundSystem(enableSound,"Sounds\Intro_1_Hyped.mp3", 300)
                    elif(option.id == 1):#Load game
                        gameStatus = "load"
                        screenVectorSize["x"] = 1000
                        screenVectorSize["y"] = 700
                        setScreenVectorSize(screenVectorSize, screen)
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
    #New game / Select characters
    elif(gameStatus == 'new'):
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                setDefaultSoundSystem(enableSound, "Sounds\Intro_Soft_Touch.mp3", 300)

        #select screen background and labels.
        Draw.drawImage(screen, "EmptyBackground.png", (screenVectorSize["x"],screenVectorSize["y"]), (0, 0))
        label = Option.fontSize(35, "Brush").render("Choose extra players", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 2 + 50, 20))
        label = Option.fontSize(35, "Brush").render("Choose your characters", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 2, 150))

        for entity in entities:
            #Draw and display character images and player labels.
            selectScreen.displayPlayers(screen, playerImageFighterDict, PlayerImageFighterSelectedDict, entities[0], selectedCharacters, Option.fontSize(25, None))
            selectScreen.drawOptions(entity)
            if botChosen == True:#If there is no bot selected
                selectchar = Option.fontSize(25, None).render("Make sure that you chose player(s)", 1,(255,0,0))
                screen.blit(selectchar, (screen.get_rect().centerx / 2, 500))
            elif charChosen == True:#If there is no characters selected
                selectchar = Option.fontSize(25, None).render("Make sure the character(s) is selected", 1,(255,0,0))
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
                        elif option.id == startGameID and selectedAmountBots != None and len(selectedCharacters) == (selectedAmountBots.id - len(players) + 1):#If Start game button is clicked, game will be started.
                            screenVectorSize["x"] = 1000
                            screenVectorSize["y"] = 700
                            setScreenVectorSize(screenVectorSize, screen)
                            gameStatus = 'Game'
                            setDefaultSoundSystem(enableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                        elif option.id == mainMenuGameID:
                            gameStatus = 'main'
                            setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
                        else:
                            if selectedAmountBots == None:
                                botChosen = True
                            elif latestSelectedChar == None:
                                charChosen = True  
    #Display board game
    elif(gameStatus == 'Game'):
        Draw.drawImage(screen, "EmptyBackground.png", (1000,700), (0, 0))
        dieRect = pygame.Rect((725,50,150,150))
        screen.blit(board,(0,0))
        if tileSelected:
            screen.blit(playerImageCardDict[displayScoreCard[1]],(660,289))
        currentPlayerCounter, randomDiceNumber, firstDieIsThrown, gameStatus,tempCurrentPlayerCounter,selectedCharacters[currentPlayerCounter].Health, playersAlive = PawnLocations(selectedCharacters, currentPlayerCounter, randomDiceNumber,firstDieIsThrown, gameStatus,tempCurrentPlayerCounter, playersAlive)

        #Draw the gameboard buttons: stop, pause and rules
        screenImg = [("BoxingBell.png", (25,25), (950,10)), ("Pause.png", (25,25), (915,10)), ("Rules.png", (25,25), (880,10))]
        for property in screenImg:
            Draw.drawImage(screen, property[0], property[1], property[2])   
        bellRec = pygame.Rect((950, 10, 25, 25))
        pauseImg = pygame.Rect((915, 10, 25, 25))
        ruleImg = pygame.Rect((880, 10, 25, 25))

        #Draw score board and render players on the board
        scoreBoardLabels = Board.drawScoreBoard(screen, selectedCharacters, yourChar, currentPlayerCounter, playersAlive, playerImageFaceDict)
        Board.renderPlayers(screen, scoreBoardLabels)

        if ev.type == pygame.QUIT:
            gameIsRunning = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            clickPosition = pygame.mouse.get_pos()#Check if player tile is selected and display score card of that player's character
            displayScoreCard = Board.displayCharacterScoreCard(clickPosition, selectedCharacters)
            tileSelected = displayScoreCard[0]

            #Pause and stop game button logic
            if bellRec.collidepoint(pygame.mouse.get_pos()) or pauseImg.collidepoint(pygame.mouse.get_pos()):
                bellSound.play()
                if pauseImg.collidepoint(pygame.mouse.get_pos()):
                    if(os.path.isfile('save.txt')):
                        os.remove('save.txt')
                    pickle.dump((selectedCharacters, currentPlayerCounter,enableSound), open('save.txt', "wb"))
                gameStatus = 'main'
                setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
                screenVectorSize["x"] = mainMenuSize[0]
                screenVectorSize["y"] = mainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
                selectedCharacters, selectedAmountBots, latestSelectedChar = selectScreen.resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar)
                selectedCharacters = [] #List of selected characters from the "new game" screen
                firstDieIsThrown = False
                yourChar = None
                currentPlayerCounter = 0
            elif ruleImg.collidepoint(pygame.mouse.get_pos()):
                webbrowser.open_new('Documenten\Rules.pdf')
    elif gameStatus == "options":
        Draw.drawImage(screen, "EmptyBackground.png", (screenVectorSize["x"],screenVectorSize["y"]), (0, 0))
        label = Option.fontSize(50, "Brush").render("Option menu", 1, (255, 0, 0))
        screen.blit(label, (260, 50))
        if enableSound == True:
            buttonsOptionScreen[1].selected = True
        elif enableSound == False:
            buttonsOptionScreen[0].selected = True
        selectScreen.drawOptions(buttonsOptionScreen)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for option in buttonsOptionScreen:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    for button in buttonsOptionScreen:
                        button.selected = False
                    if option.id == 99:
                        enableSound = False
                        pygame.mixer.music.stop()
                        option.selected = True
                    elif option.id == 98:
                        enableSound = True
                        option.selected = True
                    elif option.id == mainMenuGameID:
                            gameStatus = 'main'
                            #mainMenuSound
                            setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 1000)
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                #mainMenuSound
                setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
    #Display rules
    elif gameStatus == "rules":
        ruleOpened = True
        if ruleOpened:
            webbrowser.open_new('Documenten\Rules.pdf')
            ruleOpened = False
            gameStatus = 'main'
    #Fight
    elif gameStatus == "fight":
        if(selectedCharacters[currentPlayerCounter].IsAlive == True):
            dieRect = None
            fightIsOver = False
            if tempCurrentPlayerCounter == 4:
                tempCurrentPlayerCounter = 3
            else:
                tempCurrentPlayerCounter = currentPlayerCounter - 1
            bottomLeftFighter = tempCurrentPlayerCounter
            Draw.drawImage(screen, "EmptyBackground.png", (1000,700), (0, 0))
            ImageFighter = pygame.image.load("Images\\" + selectedCharacters[tempCurrentPlayerCounter].ImageFighter)
        
            landedTile = selectedCharacters[tempCurrentPlayerCounter].Tile
            curplaypos = selectedCharacters[tempCurrentPlayerCounter].Tile #currentPlayerCounter got updated to the next player, but we want the previous player.
            screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + selectedCharacters[tempCurrentPlayerCounter].ImageCard),(250,295)), (screen.get_width() - 250, screen.get_height() - 295))
        
            #Find index number in boardtiles
            tempTempCurrentPlayerCounter = tempCurrentPlayerCounter
            for x in boardtiles.items():
                if x[1] == curplaypos:
                    if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                        tempCurrentPlayerCounter = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                        if not tempCurrentPlayerCounter < len(selectedCharacters):
                            #The new tempcurrentplayercounter is higher than what exists
                            tempCurrentPlayerCounter = tempTempCurrentPlayerCounter
                    else:
                        tempCurrentPlayerCounter = 0 #Going to fight player 0 (first player, that means its going to fight you.

            #HP and Condition labels for the player and the owner of the corner
            textPlayerHP = Option.fontSize(25, None).render("HP: " + str(selectedCharacters[bottomLeftFighter].Health), 1, (255,255,0))
            textPlayerCondition = Option.fontSize(25, None).render("Condition: " + str(selectedCharacters[bottomLeftFighter].Condition), 1, (255,255,0))
            textOpponentHP = Option.fontSize(25, None).render("HP: " + str(selectedCharacters[tempCurrentPlayerCounter].Health), 1, (255,255,0))
            textOpponentCondition = Option.fontSize(25, None).render("Condition: " + str(selectedCharacters[tempCurrentPlayerCounter].Condition), 1, (255,255,0))

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
                diePlaceholder = pygame.image.load("Images\\DIE-1.png")
                screen.blit(diePlaceholder, (((screen.get_width() /2)-95), (screen.get_height()/2)-95))
            else:
                screen.blit(dice[fighterDieInt[fighterCurrentPlayerCounter - 1]], (((screen.get_width() /2)-95), (screen.get_height()/2)-95))

            fightDie = pygame.Rect(((screen.get_width() /2)-95), (screen.get_height()/2)-95, 190, 190)
            if fightDie.collidepoint(pygame.mouse.get_pos()) and fighterCurrentPlayerCounter < 2: #If there are still turns left and
                if ev.type == pygame.MOUSEBUTTONDOWN:
                        fighterDieInt.append(random.randint(1,6))
                        diceSound.play()
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
                        textOpponentAttack.append(Option.fontSize(25, None).render("Attack " + str(cnt + 1) + ": Damage:" + str(attack[1]['damage']) + " | Condition: " + str(attack[1]['condition']), 1, (255,255,255)))
                        cnt += 1
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
                            if attackOption.collidepoint(pygame.mouse.get_pos()) and fightIsOver == False:
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
                    textPlayerAttack.append(Option.fontSize(25, None).render("Attack " + str(cnt + 1) + ": Damage:" + str(attack[1]['damage']) + " | Condition: " + str(attack[1]['condition']),1, (255,255,255)))
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
                    if ev.type == pygame.MOUSEBUTTONDOWN and fightIsOver == False:
                        if attackOption.collidepoint(pygame.mouse.get_pos()):
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
                        fightIsOver = True
        else:
            gameStatus = 'Game'
    elif gameStatus == 'superfight':
        if(selectedCharacters[currentPlayerCounter].IsAlive == True): #Players alive?
            dieRect = None
            fightIsOver = False
            screen.fill((0,0,0))
            if tempCurrentPlayerCounter == 4:
                tempCurrentPlayerCounter = 3
            else:
                tempCurrentPlayerCounter = currentPlayerCounter - 1
            bottomLeftFighter = tempCurrentPlayerCounter
            ImageFighter = pygame.image.load("Images\\" + selectedCharacters[tempCurrentPlayerCounter].ImageFighter)
        
            landedTile = selectedCharacters[tempCurrentPlayerCounter].Tile

            curplaypos = selectedCharacters[tempCurrentPlayerCounter].Tile #currentPlayerCounter got updated to the next player, but we want the previous player.
            screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + selectedCharacters[tempCurrentPlayerCounter].ImageCard),(250,295)), (screen.get_width() - 250, screen.get_height() - 295)) #Current player's card etc.
        
            #Find index number in boardtiles
            tempTempCurrentPlayerCounter = tempCurrentPlayerCounter
            for x in boardtiles.items():
                if x[1] == curplaypos:
                    if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                        tempCurrentPlayerCounter = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                        if not tempCurrentPlayerCounter < len(selectedCharacters):
                            #The new tempcurrentplayercounter is higher than what exists
                            tempCurrentPlayerCounter = tempTempCurrentPlayerCounter
                    else:
                        tempCurrentPlayerCounter = 0 #Going to fight player 0 (first player, that means its going to fight you.

            #HP and Condition labels for the player and the owner of the corner
            textPlayerHP = Option.fontSize(25, None).render("HP: " + str(selectedCharacters[bottomLeftFighter].Health), 1, (255,255,0))
            textPlayerCondition = Option.fontSize(25, None).render("Condition: " + str(selectedCharacters[bottomLeftFighter].Condition), 1, (255,255,0))
            textOpponentHP = Option.fontSize(25, None).render("HP: " + str(selectedCharacters[tempCurrentPlayerCounter].Health), 1, (255,255,0))
            textOpponentCondition = Option.fontSize(25, None).render("Condition: " + str(selectedCharacters[tempCurrentPlayerCounter].Condition), 1, (255,255,0))

            screen.blit(textPlayerHP, (200,600))
            screen.blit(textPlayerCondition, (200,630))

            if(counter == 0):
                superfighter = random.choice(list(SuperFighters))
                randomFighterDamage = random.randint(1,6)-1
            counter += 1
            randomSuperFighter = Option.fontSize(25, None).render(superfighter.name+" deals "+str(superfighter.value[randomFighterDamage])+" damage!", 1, (255,255,0))
            defendText = Option.fontSize(25, None).render("Roll to defend!", 1, (255,255,0))
            screen.blit(randomSuperFighter, (450, 35))
            screen.blit(defendText, (450, 60))


            screen.blit(ImageFighter, (0,450)) #Blit player at superfight in bottom left
           
            if fighterCurrentPlayerCounter == 0:
                diePlaceholder = pygame.image.load("Images\\head__iron_rekt.png")
                screen.blit(diePlaceholder, (((screen.get_width() /2)-95), (screen.get_height()/2)-95))
            else:
                screen.blit(dice[fighterDieInt[fighterCurrentPlayerCounter - 1]], (((screen.get_width() /2)-95), (screen.get_height()/2)-95))

            fightDie = pygame.Rect(((screen.get_width() /2)-95), (screen.get_height()/2)-95, 190, 190)
            if fightDie.collidepoint(pygame.mouse.get_pos()) and fighterCurrentPlayerCounter < 1: #If there are still turns left and
                if ev.type == pygame.MOUSEBUTTONDOWN:
                        fighterDieInt.append(random.randint(1,6))
                        pygame.time.delay(150)
                        fighterCurrentPlayerCounter += 1
            if fighterDieInt != [] and fightIsOver == False:
                #When the die is thrown, show which attacks are available.
                attackOptions = selectedCharacters[bottomLeftFighter].Card.value[fighterDieInt[0]]
                textPlayerAttack = []
                textOpponentAttack = []
                if len(fighterDieInt) == 2: #This is very irrelevant in superfight. Dirty fix right here.
                    donothing = True
                #For the boxer in the bottom left corner
                cnt = 0
                labelHeight = 600
                for attack in attackOptions.items():
                    textPlayerAttack.append(Option.fontSize(25, None).render("Attack " + str(cnt + 1) + ": Damage:" + str(attack[1]['damage']) + " | Condition: " + str(attack[1]['condition']),1, (255,255,255)))
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
                    if ev.type == pygame.MOUSEBUTTONDOWN and fightIsOver == False:
                        if attackOption.collidepoint(pygame.mouse.get_pos()):
                            print("You chose: " + str(attackOptions[cnt]))
                            bottomLeftAttackOptions.clear()
                            bottomLeftAttackOptions.append(attackOptions[cnt])
                            bottomLeftCornerDamage = attackOptions[cnt]['damage']
                            bottomLeftCornerCondition = attackOptions[cnt]['condition']
                            fightIsOver = True
                    cnt += 1
                
                labelHeight = 600
                for label in textPlayerAttack:
                    screen.blit(label, (400,labelHeight))
                    labelHeight += 25
            
                labelHeight = 25
                for label in textOpponentAttack:
                    screen.blit(label, (350,labelHeight))
                    labelHeight += 25

            #This happens when the attack is chosen.
            if(fightIsOver):
                bottomLeftFighter = selectedCharacters[bottomLeftFighter]
                if bottomLeftFighter.Condition >= bottomLeftCornerCondition: #Attacker has enough condition to perform the attack
                    if bottomLeftCornerDamage > superfighter.value[randomFighterDamage]: #The attackers damage is better than the superfighter
                        fighterCurrentPlayerCounter = 0
                        fighterDieInt = []
                        gameStatus = 'Game'
                        counter = 0
                        #Nothing has to happen here. Superfighters don't take damage.
                    elif superfighter.value[randomFighterDamage] > bottomLeftCornerDamage:
                        bottomLeftFighter.Condition += bottomLeftCornerCondition #New condition for the attacker
                        bottomLeftFighter.Health -= (superfighter.value[randomFighterDamage]-bottomLeftCornerDamage)
                        fighterCurrentPlayerCounter = 0
                        fighterDieInt = []
                        gameStatus = 'Game'
                        counter = 0
                else:
                    print("Cannot attack, you have not enough condition left!")
                    fighterCurrentPlayerCounter = 0
                    fighterDieInt = []
                    gameStatus = 'Game'
                    counter = 0

            if(tempCurrentPlayerCounter == 3):
                tempCurrentPlayerCounter = 0

            if currentPlayerCounter == len(selectedCharacters) - 1:
                currentPlayerCounter == 0

            #Player 0 and Player 1 exists, if it is 2 (which means both players have had their turns already) then reset it back to 0 for the next fight
            if fighterCurrentPlayerCounter == 1:
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_SPACE:
                        setDefaultSoundSystem(enableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                        fighterCurrentPlayerCounter = 0
                        fighterDieInt = []
                        gameStatus = 'Game'
                        counter = 0
                        fightIsOver = True
        else:
            gameStatus = 'Game'

    elif gameStatus == 'load':
        selectedCharacters,currentPlayerCounter,enableSound = pickle.load(open('save.txt', 'rb'))
        firstDieIsThrown = True
        gameStatus = 'Game'
    pygame.display.flip()
pygame.quit()
sys.exit()