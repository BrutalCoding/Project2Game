import pygame
class Player:
    def __init__(self,name,health,condition,card,tile, imagecard="placeholder_253_300.png", imageface="placeholder_253_300.png", imagefighter = "placeholder_253_300.png"):
        self.Name = name
        self.Health = health
        self.Condition = condition
        self.Card = card
        self.Tile = tile
        self.ImageCard = imagecard
        self.ImageFace = imageface
        self.ImageFighter = imagefighter
    
    def CalculateHealth(damage):
        return self.Health - damage
    
    def CalculateCondition(conditionLose):
        return self.Condition - conditionLose

    def loadDefaultValues(self):
        self.Health = 100
        self.Condition = 15