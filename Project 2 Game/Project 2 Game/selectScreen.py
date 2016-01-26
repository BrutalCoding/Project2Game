import pygame
import options

class selectScreen:
    def selectCharacter(id, players):
        if int(id) > 4:#Set which character player 1 is.
            if id == 5:
                return players[0]
            elif id == 6:
                return players[1]
            elif id == 7:
                return players[2]
            elif id == 8:
                return players[3]

    def setAmountPlayers(id):
        if int(id) <= 4:#Set amount players that will play the game
            return int(id)    

    def drawOptions(l):
        for option in l:#Draw all options on the screen
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()