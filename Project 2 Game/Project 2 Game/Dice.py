import random
def rollDice(min, max):
    result = random.randint(min, max)
    print('Result = '+str(result))
    return result

