'''
Created on 19 jan. 2016

@author: Bunyamin Sakar

'''

class Player:
    def __init__(self,name,health,condition,card, imagecard):
        self.Name = name
        self.Health = health
        self.Condition = condition
        self.Card = card
        self.ImageCard = imagecard
    
    def CalculateHealth(damage):
        return self.Health - damage
    
    def CalculateCondition(conditionLose):
        return self.Condition - conditionLose

    def loadDefaultValues(self):
        self.Health = 100
        self.Condition = 15
    