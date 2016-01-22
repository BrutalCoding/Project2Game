'''
Created on 19 jan. 2016

@author: Bunyamin Sakar

'''

class Player:
    def __init__(self,health,condition,card):
        self.Health = health
        self.Condition = condition
        self.Card = card
    
    def CalculateHealth(damage):
        return self.Health - damage
    
    def CalculateCondition(conditionLose):
        return self.Condition - conditionLose
    