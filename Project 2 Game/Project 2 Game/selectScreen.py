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
    def makeBotLabels(generateID, maxAmountOfBots, screen, Option):
        labelAmountPlayers = []
        playerNumber = 1 #Starting with min 1 and max 4 players
        amountPlayersLabelVector = {"x": 225,"y": 50}
        generateID += 1 #Increment the latest generated id by one so it stays unique
        labelBotName = "Player"
        for x in range(1,maxAmountOfBots):
            if not playerNumber == 1:
                labelBotName = "Players"
            labelAmountPlayers.append(Option(str(playerNumber) + ' ' + labelBotName, (amountPlayersLabelVector['x'], amountPlayersLabelVector['y']), Option.fontSize(25, None), screen, generateID))
            generateID += 1
            playerNumber += 1
            amountPlayersLabelVector['x'] += 150
        return (labelAmountPlayers, generateID)

    #Make the player labels
    def makePlayerLabels(players, Option, screen):
        playerLabels = []
        playerLabelVector = {"x": 20,"y": 400}#x,y coordinates on the screen for the label to be displayed
        generateID = 0 #Generate an ID for each player
        for x in players:
            playerLabels.append(Option(x.Name, (playerLabelVector["x"], playerLabelVector["y"]), Option.fontSize(25, None), screen, generateID))
            generateID += 1
            playerLabelVector["x"] += 200
        return (playerLabels, generateID)
        
    #Draw character image on screen based on if the character is selected and assign player or CPU to character.
    def displayPlayers(screen, playerImageFighterDict, PlayerImageFighterSelectedDict, characterList, selectedCharacters, font):
        labelsPlayerSelected = []
        for character in characterList:
            if character.selected:
                if character.text == selectedCharacters[0].Name:
                    label = font.render("Player 1", 1, (255,0,0))
                    labelsPlayerSelected.append((label, (character.pos[0] + 40, (character.pos[1] - 215))))
                else:
                    label = font.render("EXTRA", 1, (255,0,0))
                    labelsPlayerSelected.append((label, (character.pos[0] + 40, (character.pos[1] - 215))))
                   
                screen.blit(PlayerImageFighterSelectedDict[character.text], (character.pos[0], (character.pos[1] - 200)))
            else:
                screen.blit(playerImageFighterDict[character.text], (character.pos[0], (character.pos[1] - 200)))
                
        for label in labelsPlayerSelected:
            screen.blit(label[0], label[1])