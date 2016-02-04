import pygame
from options import *
from Draw import *

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