def tiles():#Algorithm to decide where tiles are
    tiles = {}
    posx = 20
    posy = 15
    for i in range(40):#There's 40 tiles.
        print(i)
        if i == 0: #Exceptions (big tiles in corners and big tiles in middle of each lane.)
            tiles[i] = posx, posy
            i += 1
        if i > 10 and i < 21:#Lane 2 v
            if i == 10:
                posy += 30
                tiles[i] = posx, posy
                i += 1
            elif i == 15:
                posy += 73
                tiles[i] = posx, posy
                i += 1
            elif i == 16:
                posy += 67
                tiles[i] = posx, posy
                i += 1
            elif i == 20:
                posy += 60
                tiles[i] = posx, posy
                i += 1
            else:
                posy += 45
                tiles[i] = posx, posy
                i += 1
        elif i > 20 and i < 31:#Lane 3 <
            if i == 21:
                posx -= 62
                tiles[i] = posx, posy
                i += 1
            elif i == 25:
                posx -= 73
                tiles[i] = posx, posy
                i += 1
            elif i == 26:
                posx -= 67
                tiles[i] = posx, posy
                i += 1
            elif i == 30:
                posx -= 60
                tiles[i] = posx, posy
                i += 1
            else:
                posx -= 45
                tiles[i] = posx, posy
                i += 1
        elif i > 30:#Lane 4 ^
            if i == 29:
                posy -= 30
                tiles[i] = posx, posy
                i += 1
            elif i == 35:
                posy -= 73
                tiles[i] = posx, posy
                i += 1
            elif i == 36:
                posy -= 67
                tiles[i] = posx, posy
                i += 1
            elif i == 40:
                posy -= 60
                tiles[i] = posx, posy
                i += 1
            else:
                posy -= 45
                tiles[i] = posx, posy
                i += 1
        elif i == 41:
            posx = 20
            posy = 15
        else: #This is the first lane(>). The ifs and elifs are exceptions, such as starting tiles and fighting tiles. This is the same for all lanes.
            if i == 1:
                posx += 30
                tiles[i] = posx, posy
                i += 1
            elif i == 5:
                posx += 73
                tiles[i] = posx, posy
                i += 1
            elif i == 6:
                posx += 67
                tiles[i] = posx, posy
                i += 1
            elif i == 10:
                posx += 60
                tiles[i] = posx, posy
                i += 1
            else:
                posx += 45
                tiles[i] = posx, posy
                i += 1
    return tiles
