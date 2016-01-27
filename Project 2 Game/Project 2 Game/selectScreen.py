import sys
import pygame
import options
import random

pygame.init()
Font = pygame.font.Font(None, 40)
events = pygame.event.get()
amountPlayers = 0
yourChar = None

def drawOptions(l):
        for option in l:#Draw all options on the screen
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()   

def setAmountPlayers(id):
    if int(id) <= 4:#Set amount players that will play the game
        amountPlayers = int(id)

def selectCharacter(id):
    if int(id) > 4 and int(id) < 10:#Set which character player 1 is.
        if id == 5:
            yourChar = players[0]
        elif id == 6:
            yourChar = players[1]
        elif id == 7:
            yourChar = players[2]
        elif id == 8:
            yourChar = players[3]
        chosen.append(yourChar)


class selectScreen:
    def __init__(self):
        self.Amount
        
    
    def Run(self):
        entities = self
        screen = pygame.display.set_mode((1000, 600))
        label = Font.render("Choose amount players", 1, (255,255,0))
        screen.blit(label, (350, 10))
        label = Font.render("Choose your character", 1, (255,255,0))
        screen.blit(label, (350, 150))
        
        for x in entities:
                drawOptions(x)
                for ev in events:
                    if ev.type == pygame.MOUSEBUTTONUP:
                        for option in x:
                            if option.rect.collidepoint(pygame.mouse.get_pos()):
                                if option.id == 10:
                                    gameStatus = 'Game'
                                else:
                                    setAmountPlayers(option.id)
                                    selectCharacter(option.id)
                    elif ev.type == pygame.KEYUP:
                        if ev.key == pygame.K_ESCAPE:
                            gameStatus = 'main'