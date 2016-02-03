from Dice import rollDice

class Bot:
    def __init__(self, curplayer, gamestatus):
        self.curplayer = curplayer
        self.gamestatus = gamestatus

    def playTurn(gamestatus):
        if gamestatus == 'Game':
            dieThrow = rollDice(1,6)
            return dieThrow
            #print('DEBUG - PlayTurn')
        if gamestatus == 'fight':
            pass
