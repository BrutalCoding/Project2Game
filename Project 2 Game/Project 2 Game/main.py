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
from GameInit import *

init = GameInit()
Option = options.Option
pygame.mixer.init()
pygame.init()

#fightIsOver = False #Boolean to check if the both players have fought each other

diceSound = pygame.mixer.Sound(os.path.join('Sounds','dice_throw.wav'))
bellSound = pygame.mixer.Sound(os.path.join('Sounds','boxing-bell.wav'))

#The board can be resized every moment by declaring the function here
boardVectorSize = {"x": 600, "y": 600}
def setBoardVectorSize(boardVectorSize):
    return pygame.transform.smoothscale(pygame.image.load('Images/board.png'),(boardVectorSize["x"],boardVectorSize["y"]))
board = setBoardVectorSize(boardVectorSize) #Initialize the board size

#The screen can be resized too by declaring the function here
screenVectorSize = {"x": init.MainMenuSize[0], "y": init.MainMenuSize[1]}
def setScreenVectorSize(screenVectorSize, screen):
    return pygame.display.set_mode((screenVectorSize["x"], screenVectorSize["y"]))
screen = pygame.display.set_mode((screenVectorSize["x"], screenVectorSize["y"]))
screen = setScreenVectorSize(screenVectorSize, screen)

#Define and initialize the sounds of the game
pygame.mixer.init()
def setDefaultSoundFadeOut(fadeOutms):
    pygame.mixer.music.fadeout(fadeOutms)
    return True
def setDefaultSoundSystem(EnableSound, soundFileLocation, fadeOutms=500, volume=1):
    if(setDefaultSoundFadeOut(fadeOutms)) and init.EnableSound:
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(soundFileLocation)
        pygame.mixer.music.play(-1)
setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_Soft_Touch.mp3", 300)

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
labelAmountPlayers = selectScreen.makeBotLabels(generateID, init.MaxAmountOfBots, screen, Option)
generateID = labelAmountPlayers[1]

#Increment the latest generated id and give it to the clickable button
startGameID = generateID + 1
mainMenuGameID = startGameID + 1
selectScreenButtons = [Option("Start game", (575, 550), Option.fontSize(40, "Super"), screen, startGameID),
                       Option("Main", (25, 550), Option.fontSize(40, "Super"), screen, mainMenuGameID)] # go back to main menu
buttonsOptionScreen = [Option("Disable sound!", (300, 150), Option.fontSize(30, "Super"), screen, 99), Option("Enable sound!", (300, 200), Option.fontSize(30, "Super"), screen, 98), Option("Main", (25, 550), Option.fontSize(40, "Super"), screen, mainMenuGameID)]
entities = [playerLabels[0], labelAmountPlayers[0], selectScreenButtons]


#--------------------#
# ↓ Main game loop ↓ #
#--------------------#
while init.GameIsRunning:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            init.GameIsRunning = False
    screen.fill((0,0,0))
    #Main menu
    if(init.GameStatus == 'main'):
        Draw.drawImage(screen, "FighterMenu.png", (screenVectorSize["x"],screenVectorSize["y"]), (0, 0))
        for entity in entities:
                for option in entity:
                    option.selected = False
        selectScreen.drawOptions(menu)
        if ev.type == pygame.MOUSEBUTTONUP:
            for option in menu:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    if(option.id == 0):#New game
                        init.GameStatus = 'new'
                        screenVectorSize["x"] = init.MainMenuSize[0]
                        screenVectorSize["y"] = init.MainMenuSize[1]
                        setScreenVectorSize(screenVectorSize, screen)
                        setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_1_Hyped.mp3", 300)
                    elif(option.id == 1):#Load game
                        init.GameStatus = "load"
                        screenVectorSize["x"] = 1000
                        screenVectorSize["y"] = 700
                        setScreenVectorSize(screenVectorSize, screen)
                    elif(option.id == 2):#Options
                        init.GameStatus = "options"
                        screenVectorSize["x"] = init.MainMenuSize[0]
                        screenVectorSize["y"] = init.MainMenuSize[1]
                        setScreenVectorSize(screenVectorSize, screen)
                    elif(option.id == 3):#Rules
                        init.GameStatus = "rules"
                        screenVectorSize["x"] = init.MainMenuSize[0]
                        screenVectorSize["y"] = init.MainMenuSize[1]
                        setScreenVectorSize(screenVectorSize, screen)
                    elif(option.id == 4):#Quit
                        init.GameIsRunning = False
                    option.draw()
    #New game / Select characters
    elif(init.GameStatus == 'new'):
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                init.GameStatus = 'main'
                setDefaultSoundSystem(init.EnableSound, "Sounds\Intro_Soft_Touch.mp3", 300)

        #select screen background and labels.
        Draw.drawImage(screen, "EmptyBackground.png", (screenVectorSize["x"],screenVectorSize["y"]), (0, 0))
        label = Option.fontSize(35, "Brush").render("Choose extra players", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 2 + 50, 20))
        label = Option.fontSize(35, "Brush").render("Choose your characters", 1, (255,0,0))
        screen.blit(label, (screen.get_rect().centerx / 2, 150))

        for entity in entities:
            #Draw and display character images and player labels.
            selectScreen.displayPlayers(screen, playerImageFighterDict, PlayerImageFighterSelectedDict, entities[0], init.SelectedCharacters, Option.fontSize(25, None))
            selectScreen.drawOptions(entity)
            if init.BotChosen == True:#If there is no bot selected
                selectchar = Option.fontSize(25, None).render("Make sure that you chose player(s)", 1,(255,0,0))
                screen.blit(selectchar, (screen.get_rect().centerx / 2, 500))
            elif init.CharChosen == True:#If there is no characters selected
                selectchar = Option.fontSize(25, None).render("Make sure the character(s) is selected", 1,(255,0,0))
                screen.blit(selectchar, (screen.get_rect().centerx / 2, 500))
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for option in entity:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        if option.id > amountOfCharacters and option.id != startGameID and option.id != mainMenuGameID: #Set amount of bots
                            if init.SelectedAmountBots != None and init.SelectedAmountBots.id != option.id: #If the player didn't made a choice yet
                                if init.SelectedAmountBots: 
                                    init.SelectedAmountBots.selected = False
                                    init.SelectedAmountBots = None
                            init.SelectedAmountBots = option
                            yourChar = None
                            latestSelectedChar = None
                            init.SelectedCharacters = []
                            init.BotChosen = False
                            for character in entities[0]:
                                character.selected = False
                            option.selected = True
                        elif option.id <= amountOfCharacters and int(option.id) != startGameID and option.id != mainMenuGameID:#Set which character player 1 is.
                            #To prevent double (or more) selections, check if the character already got chosen before
                            if not players[option.id] in init.SelectedCharacters and init.SelectedAmountBots != None and len(init.SelectedCharacters) < (init.SelectedAmountBots.id - len(players) + 1): 
                                if len(init.SelectedCharacters) == 0: #Assign first selection to yourChar
                                    yourChar = players[option.id] #Set yourChar to the selected player
                                latestSelectedChar = players[option.id]
                                init.CharChosen = False
                                init.SelectedCharacters.append(latestSelectedChar) #Add the selected character to the list
                                option.selected = True
                        elif option.id == startGameID and init.SelectedAmountBots != None and len(init.SelectedCharacters) == (init.SelectedAmountBots.id - len(players) + 1):#If Start game button is clicked, game will be started.
                            screenVectorSize["x"] = 1000
                            screenVectorSize["y"] = 700
                            setScreenVectorSize(screenVectorSize, screen)
                            init.GameStatus = 'Game'
                            setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                        elif option.id == mainMenuGameID:
                            init.GameStatus = 'main'
                            setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
                        else:
                            if init.SelectedAmountBots == None:
                                init.BotChosen = True
                            elif latestSelectedChar == None:
                                init.CharChosen = True  
    #Display board game
    elif(init.GameStatus == 'Game'):
        Draw.drawImage(screen, "EmptyBackground.png", (1000,700), (0, 0))
        dieRect = pygame.Rect((725,50,150,150))
        screen.blit(board,(0,0))
        if init.TileSelected:
            screen.blit(playerImageCardDict[displayScoreCard[1]],(660,289))
        init.CurrentPlayerCounter, init.RandomDiceNumber, init.FirstDieIsThrown, init.GameStatus,init.TempCurrentPlayerCounter,init.SelectedCharacters[init.CurrentPlayerCounter].Health, init.PlayersAlive = boardLogic(init.SelectedCharacters, init.CurrentPlayerCounter, init.RandomDiceNumber,init.FirstDieIsThrown, init.GameStatus, init.TempCurrentPlayerCounter, init.PlayersAlive,ev,init,boardtiles,screen, pawnload, dice, dieRect, diceSound)
        #Draw the gameboard buttons: stop, pause and rules
        screenImg = [("BoxingBell.png", (25,25), (950,10)), ("Pause.png", (25,25), (915,10)), ("Rules.png", (25,25), (880,10))]
        for property in screenImg:
            Draw.drawImage(screen, property[0], property[1], property[2]) 
        bellRec = pygame.Rect((950, 10, 25, 25))
        pauseImg = pygame.Rect((915, 10, 25, 25))
        ruleImg = pygame.Rect((880, 10, 25, 25))

        #Draw score board and render players on the board
        scoreBoardLabels = Board.drawScoreBoard(screen, init.SelectedCharacters, yourChar, init.CurrentPlayerCounter, init.PlayersAlive, playerImageFaceDict)
        Board.renderPlayers(screen, scoreBoardLabels)

        if ev.type == pygame.QUIT:
            init.GameIsRunning = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            clickPosition = pygame.mouse.get_pos()#Check if player tile is selected and display score card of that player's character
            displayScoreCard = Board.displayCharacterScoreCard(clickPosition, init.SelectedCharacters)
            init.TileSelected = displayScoreCard[0]

            #Pause and stop game button logic
            if bellRec.collidepoint(pygame.mouse.get_pos()) or pauseImg.collidepoint(pygame.mouse.get_pos()):
                bellSound.play()
                if pauseImg.collidepoint(pygame.mouse.get_pos()):
                    if(os.path.isfile('save.txt')):
                        os.remove('save.txt')
                    pickle.dump((init.SelectedCharacters, init.CurrentPlayerCounter,init.EnableSound), open('save.txt', "wb"))
                init.GameStatus = 'main'
                setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
                screenVectorSize["x"] = init.MainMenuSize[0]
                screenVectorSize["y"] = init.MainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
                init.SelectedCharacters, init.SelectedAmountBots, latestSelectedChar = selectScreen.resetSelections(init.SelectedCharacters, init.SelectedAmountBots, latestSelectedChar)
                init.SelectedCharacters = [] #List of selected characters from the "new game" screen
                init.FirstDieIsThrown = False
                yourChar = None
                init.CurrentPlayerCounter = 0
            elif ruleImg.collidepoint(pygame.mouse.get_pos()):
                webbrowser.open_new('Documenten\Rules.pdf')
    elif init.GameStatus == "options":
        Draw.drawImage(screen, "EmptyBackground.png", (screenVectorSize["x"],screenVectorSize["y"]), (0, 0))
        label = Option.fontSize(50, "Brush").render("Option menu", 1, (255, 0, 0))
        screen.blit(label, (260, 50))
        if init.EnableSound == True:
            buttonsOptionScreen[1].selected = True
        elif init.EnableSound == False:
            buttonsOptionScreen[0].selected = True
        selectScreen.drawOptions(buttonsOptionScreen)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for option in buttonsOptionScreen:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    for button in buttonsOptionScreen:
                        button.selected = False
                    if option.id == 99:
                        init.EnableSound = False
                        pygame.mixer.music.stop()
                        option.selected = True
                    elif option.id == 98:
                        init.EnableSound = True
                        option.selected = True
                    elif option.id == mainMenuGameID:
                            init.GameStatus = 'main'
                            #mainMenuSound
                            setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_Soft_Touch.mp3", 1000)
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                init.GameStatus = 'main'
                #mainMenuSound
                setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
    #Display rules
    elif init.GameStatus == "rules":
        ruleOpened = True
        if ruleOpened:
            webbrowser.open_new('Documenten\Rules.pdf')
            ruleOpened = False
            init.GameStatus = 'main'
    #Fight
    elif init.GameStatus == "fight":
        if(init.SelectedCharacters[init.CurrentPlayerCounter].IsAlive == True):
            dieRect = None
            fightIsOver = False
            if init.TempCurrentPlayerCounter == 4:
                init.TempCurrentPlayerCounter = 3
            else:
                init.TempCurrentPlayerCounter = init.CurrentPlayerCounter - 1
            bottomLeftFighter = init.TempCurrentPlayerCounter
            Draw.drawImage(screen, "EmptyBackground.png", (1000,700), (0, 0))
            ImageFighter = pygame.image.load("Images\\" + init.SelectedCharacters[init.TempCurrentPlayerCounter].ImageFighter)
        
            landedTile = init.SelectedCharacters[init.TempCurrentPlayerCounter].Tile
            curplaypos = init.SelectedCharacters[init.TempCurrentPlayerCounter].Tile #init.CurrentPlayerCounter got updated to the next player, but we want the previous player.
            screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + init.SelectedCharacters[init.TempCurrentPlayerCounter].ImageCard),(250,295)), (screen.get_width() - 250, screen.get_height() - 295))
        
            #Find index number in boardtiles
            init.tempTempCurrentPlayerCounter = init.TempCurrentPlayerCounter
            for x in boardtiles.items():
                if x[1] == curplaypos:
                    if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                        init.TempCurrentPlayerCounter = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                        if not init.TempCurrentPlayerCounter < len(init.SelectedCharacters):
                            #The new init.Tempinit.CurrentPlayerCounter is higher than what exists
                            init.TempCurrentPlayerCounter = init.tempTempCurrentPlayerCounter
                    else:
                        init.TempCurrentPlayerCounter = 0 #Going to fight player 0 (first player, that means its going to fight you.

            #HP and Condition labels for the player and the owner of the corner
            textPlayerHP = Option.fontSize(25, None).render("HP: " + str(init.SelectedCharacters[bottomLeftFighter].Health), 1, (255,255,0))
            textPlayerCondition = Option.fontSize(25, None).render("Condition: " + str(init.SelectedCharacters[bottomLeftFighter].Condition), 1, (255,255,0))
            textOpponentHP = Option.fontSize(25, None).render("HP: " + str(init.SelectedCharacters[init.TempCurrentPlayerCounter].Health), 1, (255,255,0))
            textOpponentCondition = Option.fontSize(25, None).render("Condition: " + str(init.SelectedCharacters[init.TempCurrentPlayerCounter].Condition), 1, (255,255,0))

            #Blit the HP/Condition labels
            screen.blit(textPlayerHP, (200,600))
            screen.blit(textPlayerCondition, (200,630))
            screen.blit(textOpponentHP, (650, 35))
            screen.blit(textOpponentCondition, (650,65))

            ImageOpponent = pygame.image.load("Images\\" + init.SelectedCharacters[init.TempCurrentPlayerCounter].ImageFighter)
            screen.blit(ImageFighter, (0,450)) #Blit attacker in bottom down
            screen.blit(ImageOpponent, (800,0)) #Blit defender in top right

            screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + init.SelectedCharacters[init.CurrentPlayerCounter].ImageCard),(250,295)), (0,0))
        
            #If the first turn has not begun yet, display a placeholder for the dice. Else show what dice was thrown.
            if init.FighterCurrentPlayerCounter == 0:
                diePlaceholder = pygame.image.load("Images\\DIE-1.png")
                screen.blit(diePlaceholder, (((screen.get_width() /2)-95), (screen.get_height()/2)-95))
            else:
                screen.blit(dice[init.FighterDieInt[init.FighterCurrentPlayerCounter - 1]], (((screen.get_width() /2)-95), (screen.get_height()/2)-95))

            fightDie = pygame.Rect(((screen.get_width() /2)-95), (screen.get_height()/2)-95, 190, 190)
            if fightDie.collidepoint(pygame.mouse.get_pos()) and init.FighterCurrentPlayerCounter < 2: #If there are still turns left and
                if ev.type == pygame.MOUSEBUTTONDOWN:
                        init.FighterDieInt.append(random.randint(1,6))
                        diceSound.play()
                        pygame.time.delay(150)
                        init.FighterCurrentPlayerCounter += 1
            if init.FighterDieInt != [] and fightIsOver == False:
                #When the die is thrown, show which attacks are available.
                attackOptions = init.SelectedCharacters[bottomLeftFighter].Card.value[init.FighterDieInt[0]]
                textPlayerAttack = []
                textOpponentAttack = []
                if len(init.FighterDieInt) == 2:
                    #For the boxer in the top right corner
                    attackOpponentOptions = init.SelectedCharacters[init.TempCurrentPlayerCounter].Card.value[init.FighterDieInt[1]]
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
                bottomLeftFighter = init.SelectedCharacters[bottomLeftFighter]
                topRightFighter = init.SelectedCharacters[init.TempCurrentPlayerCounter]
                if bottomLeftFighter.Condition >= abs(bottomLeftCornerCondition): #Attacker has enough condition to perform the attack
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
                        bottomLeftCornerDamage = 0
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

            if(init.TempCurrentPlayerCounter == 3):
                init.TempCurrentPlayerCounter = 0

            if init.CurrentPlayerCounter == len(init.SelectedCharacters) - 1:
                init.CurrentPlayerCounter == 0

            #Player 0 and Player 1 exists, if it is 2 (which means both players have had their turns already) then reset it back to 0 for the next fight
            if init.FighterCurrentPlayerCounter == 2:
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_SPACE:
                        setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                        init.FighterCurrentPlayerCounter = 0
                        init.FighterDieInt = []
                        init.GameStatus = 'Game'
                        fightIsOver = True
        else:
            init.GameStatus = 'Game'
    elif init.GameStatus == 'superfight':
        if(init.SelectedCharacters[init.CurrentPlayerCounter].IsAlive == True): #Players alive?
            dieRect = None
            fightIsOver = False
            screen.fill((0,0,0))
            if init.TempCurrentPlayerCounter == 4:
                init.TempCurrentPlayerCounter = 3
            else:
                init.TempCurrentPlayerCounter = init.CurrentPlayerCounter - 1
            bottomLeftFighter = init.TempCurrentPlayerCounter
            ImageFighter = pygame.image.load("Images\\" + init.SelectedCharacters[init.TempCurrentPlayerCounter].ImageFighter)
        
            landedTile = init.SelectedCharacters[init.TempCurrentPlayerCounter].Tile

            curplaypos = init.SelectedCharacters[init.TempCurrentPlayerCounter].Tile #init.CurrentPlayerCounter got updated to the next player, but we want the previous player.
            screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + init.SelectedCharacters[init.TempCurrentPlayerCounter].ImageCard),(250,295)), (screen.get_width() - 250, screen.get_height() - 295)) #Current player's card etc.
        
            #Find index number in boardtiles
            init.tempTempCurrentPlayerCounter = init.TempCurrentPlayerCounter
            for x in boardtiles.items():
                if x[1] == curplaypos:
                    if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                        init.TempCurrentPlayerCounter = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                        if not init.TempCurrentPlayerCounter < len(init.SelectedCharacters):
                            #The new init.Tempinit.CurrentPlayerCounter is higher than what exists
                            init.TempCurrentPlayerCounter = init.tempTempCurrentPlayerCounter
                    else:
                        init.TempCurrentPlayerCounter = 0 #Going to fight player 0 (first player, that means its going to fight you.

            #HP and Condition labels for the player and the owner of the corner
            textPlayerHP = Option.fontSize(25, None).render("HP: " + str(init.SelectedCharacters[bottomLeftFighter].Health), 1, (255,255,0))
            textPlayerCondition = Option.fontSize(25, None).render("Condition: " + str(init.SelectedCharacters[bottomLeftFighter].Condition), 1, (255,255,0))
            textOpponentHP = Option.fontSize(25, None).render("HP: " + str(init.SelectedCharacters[init.TempCurrentPlayerCounter].Health), 1, (255,255,0))
            textOpponentCondition = Option.fontSize(25, None).render("Condition: " + str(init.SelectedCharacters[init.TempCurrentPlayerCounter].Condition), 1, (255,255,0))

            screen.blit(textPlayerHP, (200,600))
            screen.blit(textPlayerCondition, (200,630))

            if(init.Counter == 0):
                superfighter = random.choice(list(SuperFighters))
                randomFighterDamage = random.randint(1,6)-1
            init.Counter += 1
            randomSuperFighter = Option.fontSize(25, None).render(superfighter.name+" deals "+str(superfighter.value[randomFighterDamage])+" damage!", 1, (255,255,0))
            defendText = Option.fontSize(25, None).render("Roll to defend!", 1, (255,255,0))
            screen.blit(randomSuperFighter, (450, 35))
            screen.blit(defendText, (450, 60))


            screen.blit(ImageFighter, (0,450)) #Blit player at superfight in bottom left
           
            if init.FighterCurrentPlayerCounter == 0:
                diePlaceholder = pygame.image.load("Images\\DIE-1.png")
                screen.blit(diePlaceholder, (((screen.get_width() /2)-95), (screen.get_height()/2)-95))
            else:
                screen.blit(dice[init.SuperFighterDieInt[init.FighterCurrentPlayerCounter - 1]], (((screen.get_width() /2)-95), (screen.get_height()/2)-95))

            fightDie = pygame.Rect(((screen.get_width() /2)-95), (screen.get_height()/2)-95, 190, 190)
            if fightDie.collidepoint(pygame.mouse.get_pos()) and init.FighterCurrentPlayerCounter < 1: #If there are still turns left and
                if ev.type == pygame.MOUSEBUTTONDOWN:
                        init.SuperFighterDieInt.append(random.randint(1,6))
                        pygame.time.delay(150)
                        init.FighterCurrentPlayerCounter += 1
            if init.SuperFighterDieInt != [] and fightIsOver == False:
                #When the die is thrown, show which attacks are available.
                attackOptions = init.SelectedCharacters[bottomLeftFighter].Card.value[init.SuperFighterDieInt[0]]
                textPlayerAttack = []
                textOpponentAttack = []
                if len(init.SuperFighterDieInt) == 2: #This is very irrelevant in superfight. Dirty fix right here.
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
                bottomLeftFighter = init.SelectedCharacters[bottomLeftFighter]
                if bottomLeftFighter.Condition >= abs(bottomLeftCornerCondition): #Attacker has enough condition to perform the attack
                    if bottomLeftCornerDamage > superfighter.value[randomFighterDamage]: #The attackers damage is better than the superfighter
                        bottomLeftFighter.Condition += bottomLeftCornerCondition
                        init.FighterCurrentPlayerCounter = 0
                        init.SuperFighterDieInt = []
                        init.GameStatus = 'Game'
                        init.Counter = 0
                        #Nothing has to happen here. Superfighters don't take damage.
                    elif superfighter.value[randomFighterDamage] > bottomLeftCornerDamage:
                        bottomLeftFighter.Condition += bottomLeftCornerCondition #New condition for the attacker
                        bottomLeftFighter.Health -= (superfighter.value[randomFighterDamage]-bottomLeftCornerDamage)
                        init.FighterCurrentPlayerCounter = 0
                        init.SuperFighterDieInt = []
                        init.GameStatus = 'Game'
                        init.Counter = 0
                    elif superfighter.value[randomFighterDamage] == bottomLeftCornerDamage:
                        bottomLeftFighter.Condition += bottomLeftCornerCondition #New condition for the attacker
                        init.FighterCurrentPlayerCounter = 0
                        int.SuperFighterDieInt = []
                        init.GameStatus = 'Game'
                        init.Counter = 0
                else:
                    print("Cannot attack, you have not enough condition left!")
                    init.FighterCurrentPlayerCounter = 0
                    init.SuperFighterDieInt = []
                    init.GameStatus = 'Game'
                    init.Counter = 0

            if(init.TempCurrentPlayerCounter == 3):
                init.TempCurrentPlayerCounter = 0

            if init.CurrentPlayerCounter == len(init.SelectedCharacters) - 1:
                init.CurrentPlayerCounter == 0

            #Player 0 and Player 1 exists, if it is 2 (which means both players have had their turns already) then reset it back to 0 for the next fight
            if init.FighterCurrentPlayerCounter == 1:
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_SPACE:
                        setDefaultSoundSystem(init.EnableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                        init.FighterCurrentPlayerCounter = 0
                        init.SuperFighterDieInt = []
                        init.GameStatus = 'Game'
                        init.Counter = 0
                        fightIsOver = True
        else:
            init.GameStatus = 'Game'

    elif init.GameStatus == 'load':
        init.SelectedCharacters,init.CurrentPlayerCounter,init.EnableSound = pickle.load(open('save.txt', 'rb'))
        init.FirstDieIsThrown = True
        init.GameStatus = 'Game'
    pygame.display.flip()
pygame.quit()
sys.exit()