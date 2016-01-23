import pygame
class Player:
    def __init__(self,name,health,condition,card, imagecard = "placeholder_253_300.png", imageface = "placeholder_253_300.png"):
        self.Name = name
        self.Health = health
        self.Condition = condition
        self.Card = card
        self.ImageCard = imagecard
        self.ImageFace = imageface
    
    def CalculateHealth(damage):
        return self.Health - damage
    
    def CalculateCondition(conditionLose):
        return self.Condition - conditionLose

    def loadDefaultValues(self):
        self.Health = 100
        self.Condition = 15