import pygame
import options

class selectScreen:
    #Reset the selected and amount of characters to zero again in able to reselect later.
    def resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar):
        if selectedCharacters is not None:
            selectedCharacters.clear()
        if selectedAmountBots is not None:
            selectedAmountBots = None
        if latestSelectedChar is not None:
            latestSelectedChar = None
        return (selectedCharacters, selectedAmountBots, latestSelectedChar)
    
    #Draw all the labels on the screen
    def drawOptions(l):
        for option in l:#Draw all options on the screen
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
    
    #Make the bot labels
    def makeBotLabels(generateID, maxAmountOfBots, font, screen, Option):
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
        return (labelAmountPlayers, generateID)

    #Make the player labels
    def makePlayerLabels(players, Option, font, screen):
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
        return (playerLabels, generateID)
        
   