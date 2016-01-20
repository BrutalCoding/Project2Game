def tiles():#Algorithm to decide where tiles are
    tiles = {}
    posx = 37
    posy = 37
    for i in range(40):#There's 40 tiles.
        if i == 0 or i == 5 or i == 10 or i == 15 or i == 20 or i == 25 or i == 30 or i == 35: #Exceptions (big tiles in corners and big tiles in middle of each lane.)
            tiles[i] = posx, posy
            i += 15
        elif i > 10:
            tiles[i] = posx, posy
            i += 1
        elif i > 20:
            tiles[i] = posx, posy
            i += 1
        elif i > 30:
            tiles[i] = posx, posy
            i += 1
        else: #This is the first lane.
            posx += 50
            tiles[i] = posx, posy
            pass
    return tiles
