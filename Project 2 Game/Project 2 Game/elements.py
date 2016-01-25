import pygame
def diceload(file):
    return pygame.transform.scale(pygame.image.load(file), (150,150))

#def pawnload(file):
#    return pygame.transform.scale(pygame.image.load(file), (30,51))

def pawnload(file):
    return pygame.transform.scale(pygame.image.load(file), (30,30))

