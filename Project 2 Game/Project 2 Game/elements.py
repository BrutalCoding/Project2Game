import pygame
def diceload(file):
    return pygame.transform.smoothscale(pygame.image.load(file), (150,150))

def pawnload(file):
    return pygame.transform.smoothscale(pygame.image.load(file), (30,50))

