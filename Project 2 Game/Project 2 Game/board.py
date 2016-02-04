import pygame
from options import *
from Draw import *
from GameInit import *
import random
class Board:
    def tiles():#Algorithm to decide where tiles are
        tiles = {}
        posx = 20
        posy = 15
        for i in range(40):
            #Top left to upper right tile
            if i <= 10:
                posy = 15
                if i > 1 and i < 10 and i != 5 and i != 6:
                    posx += 45
                elif i == 0:
                    #Top left corner
                    #pygame.rect(0,0,50,50)
                    posx = 20
                elif i == 1:
                    #From top left corner to the first small tile right of it
                    posx += 65
                elif i == 5 or i == 6:
                    #Midtop fighter block
                    posx += 65
                elif i == 10:
                    #Top right corner
                    posx = 550

            #Top right to bottom right tile
            elif i > 10 and i <= 20:
                posx = 550
                if i > 11 and i < 20 and i != 15 and i != 16:
                    posy += 45
                elif i == 11:
                    #From top right corner to the first small tile beneath it
                    posy += 65
                elif i == 15 or i == 16:
                    #Midtop fighter block
                    posy += 65
                elif i == 20:
                    #Bottom right corner
                    posy = 540

            #Bottom right to bottom left tile
            elif i > 20 and i <= 30:
                posy = 540
                if i > 21 and i < 30 and i != 25 and i != 26:
                    posx -= 45
                elif i == 21:
                    #Bottom right corner
                    posx -= 65
                elif i == 25 or i == 26:
                    #Midtop fighter block
                    posx -= 65
                elif i == 30:
                    #Top right corner
                    posx = 20

            #Bottom left to upper left tile
            elif i > 30 and i <= 39: #Left lane
                posx = 20
                if i > 31 and i < 40 and i != 35 and i != 36:
                    posy -= 45
                elif i == 31:
                    #From top right corner to the first small tile beneath it
                    posy -= 65
                elif i == 35 or i == 36:
                    #Midtop fighter block
                    posy -= 65
                elif i == 40:
                    #Bottom right corner
                    posy = 15
            tiles[i] = posx, posy
        return tiles

    def drawScoreBoard(screen, selectedCharacters, yourChar, currentPlayerCounter, playersAlive, playerImageFaceDict):
        #Draw scoreboard
        scoreBoardLabels = []
        name = None
        vectorX = 0
        for x in selectedCharacters:
            Draw.drawImage(screen, "ScoreBoard.png", (250,100), (vectorX,600))
            #screen.blit(pygame.transform.scale(scoreBoardBackground,(250,100)), (vectorX,600))
            vectorX += 250
            if x == yourChar:
                name = "Player 1: " + str(x.Name)
            else:
                name = "Player: " + str(x.Name)
            if x == selectedCharacters[currentPlayerCounter] and playersAlive != 1:
                labelColor = (217, 30, 24) #'Thunderbird' red
                screen.blit(Option.fontSize(35, None).render("Current player:", 1,(255,255,255)), (680, 225))
                screen.blit(playerImageFaceDict[x.Name],(870,210))
            else:
                labelColor = (0,0,0) #Black
            scoreBoardLabels.append((Option.fontSize(18, "lcd").render(name, 1, labelColor), Option.fontSize(20, None).render("Lifepoints: " + str(x.Health), 1, labelColor), Option.fontSize(20, None).render("Condition: " + str(x.Condition), 1, labelColor)))
        return scoreBoardLabels

    def renderPlayers(screen, scoreBoardLabels):
            #Render the players on the score board
            labelPixelLenght = 10 #First label location on the score board
            for label in scoreBoardLabels:
                labelPixelHeight = 613
                for x in label:
                    screen.blit(x, (labelPixelLenght, labelPixelHeight))
                    labelPixelHeight += 25
                labelPixelLenght += 250    

    def displayCharacterScoreCard(clickPosition, selectedCharacters):
        cardName = None
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
            tileSelected = False
        return (tileSelected, cardName)

    #Loop through selected characters and place related pawns
def boardLogic(SelectedCharacters, CurrentPlayerCounter, RandomDiceNumber, FirstDieIsThrown, GameStatus, TempCurrentPlayerCounter, PlayersAlive, ev, init, boardtiles, screen, pawnload, dice, dieRect, diceSound):
    #Board game main loop. Every movement is here.
    if ev.type == pygame.MOUSEBUTTONDOWN:
        if dieRect.collidepoint(pygame.mouse.get_pos()):
            if init.SelectedCharacters[init.CurrentPlayerCounter].Health > 0:
                init.RandomDiceNumber = random.randint(1,6)
                diceSound.play()
                #check steps and ad condition
                newSteps = init.SelectedCharacters[init.CurrentPlayerCounter].Steps + init.RandomDiceNumber
                if newSteps >= 40:
                    init.SelectedCharacters[init.CurrentPlayerCounter].Condition = 15
                    init.SelectedCharacters[init.CurrentPlayerCounter].Steps = 0
                    if newSteps > 40:
                        difference = newSteps - 40
                        init.SelectedCharacters[init.CurrentPlayerCounter].Steps += difference
                else:
                    init.SelectedCharacters[init.CurrentPlayerCounter].Steps += init.RandomDiceNumber

                currentTile = init.SelectedCharacters[init.CurrentPlayerCounter].Tile
                for x in boardtiles.items():
                    if x[1] == currentTile:
                        #To prevent that newTileNumber gets number 40 (Since it goes from 0 to 39)
                        if x[0] + init.RandomDiceNumber < 40:
                            newTileNumber = x[0] + init.RandomDiceNumber
                        else:
                            newTileNumber = 0
                        for pawn in init.SelectedCharacters:
                            if pawn.Name != init.SelectedCharacters[init.CurrentPlayerCounter].Name:
                                if boardtiles[newTileNumber] == pawn.Tile and pawn.Health > 0 and boardtiles[newTileNumber] != boardtiles[5] and boardtiles[newTileNumber] != boardtiles[15] and boardtiles[newTileNumber] != boardtiles[25] and boardtiles[newTileNumber] != boardtiles[35]:#If there are 2 pawns on the same tile and the tile is not a fight tile. 
                                    init.GameStatus = 'fight'
                        init.SelectedCharacters[init.CurrentPlayerCounter].Tile = boardtiles[newTileNumber]
                        if init.SelectedCharacters[init.CurrentPlayerCounter].Tile == boardtiles[5] or init.SelectedCharacters[init.CurrentPlayerCounter].Tile == boardtiles[15] or init.SelectedCharacters[init.CurrentPlayerCounter].Tile == boardtiles[25] or init.SelectedCharacters[init.CurrentPlayerCounter].Tile == boardtiles[35]:
                            init.GameStatus = "superfight"
                        curplaypos = init.SelectedCharacters[init.CurrentPlayerCounter].Tile #Current player's position on board
                        if curplaypos in (boardtiles[0], boardtiles[1], boardtiles[9], boardtiles[10], boardtiles[11], boardtiles[19], boardtiles[20], boardtiles[21], boardtiles[29], boardtiles[30], boardtiles[31], boardtiles[39]):
                            if init.CurrentPlayerCounter == 0 and (curplaypos == boardtiles[0] or curplaypos == boardtiles[39] or curplaypos == boardtiles[1]):
                                #Add HP to the owner
                                playerHP = init.SelectedCharacters[init.CurrentPlayerCounter].Health  
                                if playerHP + 10 <= 100:
                                    init.SelectedCharacters[init.CurrentPlayerCounter].Health += 10
                                elif playerHP + 10 > 100:
                                    init.SelectedCharacters[init.CurrentPlayerCounter].Health = 100
                            elif init.CurrentPlayerCounter != 0 and curplaypos in (boardtiles[init.CurrentPlayerCounter * 10], boardtiles[(init.CurrentPlayerCounter * 10) - 1], boardtiles[(init.CurrentPlayerCounter * 10) + 1]):
                                #Add HP to the owner
                                playerHP = init.SelectedCharacters[init.CurrentPlayerCounter].Health  
                                if playerHP + 10 <= 100:
                                    init.SelectedCharacters[init.CurrentPlayerCounter].Health += 10
                                elif playerHP + 10 > 100:
                                    init.SelectedCharacters[init.CurrentPlayerCounter].Health = 100
                            else: #Fight code
                                for x in boardtiles.items():
                                    if x[1] == curplaypos:
                                        if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                                            currentTileOwner = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                                        else:
                                            currentTileOwner = 0 #Going to fight player 0 (first player, that means its going to fight you.
                                if currentTileOwner < len(init.SelectedCharacters):
                                    if init.SelectedCharacters[currentTileOwner].Health > 0:
                                        setDefaultSoundSystem(init.EnableSound, "Sounds\Fight.mp3")
                                        init.GameStatus = 'fight'
                                    else:
                                        init.GameStatus = "Game"
                                else:
                                    init.SelectedCharacters[init.CurrentPlayerCounter].Health -= 10
                screen.blit(pawnload('Images/' + init.SelectedCharacters[init.CurrentPlayerCounter].ImageFace), currentTile)
                pygame.time.delay(150)
                #If the counter is at the last character, start at the first player again.
                init.FirstDieIsThrown = True
                if init.CurrentPlayerCounter == len(init.SelectedCharacters) - 1: 
                    init.CurrentPlayerCounter = 0
                else:
                    if init.SelectedCharacters[init.CurrentPlayerCounter + 1].Health > 0:
                        init.CurrentPlayerCounter += 1
                    elif init.SelectedCharacters[init.CurrentPlayerCounter]:
                        init.CurrentPlayerCounter += 2

                if init.TempCurrentPlayerCounter == len(init.SelectedCharacters) - 1: 
                    init.TempCurrentPlayerCounter = 0
                else:
                    init.TempCurrentPlayerCounter += 1
        return init.CurrentPlayerCounter, init.RandomDiceNumber, init.FirstDieIsThrown, init.GameStatus,init.TempCurrentPlayerCounter,init.SelectedCharacters[init.CurrentPlayerCounter].Health, init.PlayersAlive
    else:
        #Update player position
        cntCorner = 1
        cntPlayer = 1

        for p in init.SelectedCharacters:
            if not init.FirstDieIsThrown:
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
        screen.blit(dice[init.RandomDiceNumber], (725,50))
        init.PlayersAlive = 0
        cnt = 0
        for fighter in init.SelectedCharacters:
            if fighter.Health > 0:
                init.PlayersAlive += 1
            else:
                fighter.Health = 0 #Reset it to 0 instead of displaying a negative value.
                fighter.IsAlive = False
            if not fighter.Condition > 0:
                fighter.Condition = 0
            if cnt < len(init.SelectedCharacters):
                cnt += 1
        if init.PlayersAlive == 1:
            for x in init.SelectedCharacters:
                if x.IsAlive:
                    message = str(x.Name) + " just won the game!"
            ImageBGLink = "Images/EmptyBackground.png"
            brushLink = "Fonts/Brushstrike.ttf"
            screenMessage = WindowsScreen(screen,message,ImageBGLink,brushLink)
            screen.blit(screenMessage.surf, (0, 0))
    return init.CurrentPlayerCounter, init.RandomDiceNumber,init.FirstDieIsThrown,init.GameStatus, init.TempCurrentPlayerCounter,init.SelectedCharacters[init.CurrentPlayerCounter].Health, init.PlayersAlive