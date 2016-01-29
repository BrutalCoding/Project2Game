import pygame
import random
class fightScreen(object):
    """Description: As soon when a pawn lands on a corner from an enemy, he/she will need to fight against each other."""
    def __init__(self,fighterCurrentPlayerCounter,screen,currentPlayerCounter,
                 tempCurrentPlayerCounter,selectedCharacters,boardtiles,gameIsRunning,dice):
        self.fighterCurrentPlayerCounter = fighterCurrentPlayerCounter
        self.screen = screen
        self.currentPlayerCounter = currentPlayerCounter
        self.tempCurrentPlayerCounter = tempCurrentPlayerCounter
        self.selectedCharacters = selectedCharacters
        self.boardtiles = boardtiles
        self.gameIsRunning = gameIsRunning
        self.dice = dice

    def startFight(self):
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                    gameIsRunning = False
        if self.fighterCurrentPlayerCounter == 2:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    setDefaultSoundSystem(enableSound,"Sounds\Intro_1_Soft_Pump.mp3", 300, 0.3)
                    fighterCurrentPlayerCounter = 0
                    gameStatus = 'Game'
        dieRect = None
        if self.tempCurrentPlayerCounter == 4:
            self.tempCurrentPlayerCounter = 3
        else:
            self.tempCurrentPlayerCounter = self.currentPlayerCounter - 1
        ImageFighter = pygame.image.load("Images\\" + self.selectedCharacters[self.tempCurrentPlayerCounter].ImageFighter)
        
        landedTile = self.selectedCharacters[self.tempCurrentPlayerCounter].Tile

        curplaypos = self.selectedCharacters[self.tempCurrentPlayerCounter].Tile #currentPlayerCounter got updated to the next player, but we want the prself.evious player.
        self.screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + self.selectedCharacters[self.tempCurrentPlayerCounter].ImageCard),(250,295)), (self.screen.get_width() - 250, self.screen.get_height() - 295))
        #Find index number in boardtiles
        for x in self.boardtiles.items():
            if x[1] == curplaypos:
                if not x[0] in (0,39,1): #If its not the top left corner (Blue corner)
                    self.tempCurrentPlayerCounter = int(round(x[0] / 10)) #Going to fight player 1, 2 or 3 and not player 0.
                else:
                    self.tempCurrentPlayerCounter = 0 #Going to fight player 0 (first player, that means its going to fight you.

        if curplaypos in (self.boardtiles[0], self.boardtiles[1], self.boardtiles[9], self.boardtiles[10], self.boardtiles[11], self.boardtiles[19], self.boardtiles[20], self.boardtiles[21], self.boardtiles[29], self.boardtiles[30], self.boardtiles[31], self.boardtiles[39]):
            if (self.tempCurrentPlayerCounter) == 0 and curplaypos == self.boardtiles[0] or curplaypos == self.boardtiles[39] or curplaypos == self.boardtiles[1]:
                print('Player #', (self.tempCurrentPlayerCounter - 1),' cant go fight himself - Hello',self.tempCurrentPlayerCounter)
                pass #Don't fight
            elif (self.tempCurrentPlayerCounter) != 0 and curplaypos in (self.boardtiles[(self.tempCurrentPlayerCounter) * 10], self.boardtiles[((self.tempCurrentPlayerCounter) * 10) - 1], self.boardtiles[((self.tempCurrentPlayerCounter) * 10) + 1]):
                print('Player #', self.tempCurrentPlayerCounter,' cant go fight himself - Goodbye',self.tempCurrentPlayerCounter)
                pass
            else: #Fight code
                print('Player #', (self.tempCurrentPlayerCounter -1),' is going to fight player',self.tempCurrentPlayerCounter)

        ImageOpponent = pygame.image.load("Images\\" + self.selectedCharacters[self.tempCurrentPlayerCounter].ImageFighter)
        self.screen.blit(ImageFighter, (0,450)) #Blit attacker in bottom down
        self.screen.blit(ImageOpponent, (800,0)) #Blit defender in top right

        self.screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\" + self.selectedCharacters[self.currentPlayerCounter].ImageCard),(250,295)), (0,0))
        
        #If the first turn has not begun yet, display a placeholder for the dice. Else show what dice was thrown.
        if self.fighterCurrentPlayerCounter == 0:
            diePlaceholder = pygame.image.load("Images\\head__iron_rekt.png")
            self.screen.blit(diePlaceholder, (((self.screen.get_width() /2)-95), (self.screen.get_height()/2)-95))
        else:
            self.screen.blit(self.dice[fighterDieInt], (((self.screen.get_width() /2)-95), (self.screen.get_height()/2)-95))
        fightDie = pygame.Rect(((self.screen.get_width() /2)-95), (self.screen.get_height()/2)-95, 190, 190)
        if fightDie.collidepoint(pygame.mouse.get_pos()) and self.fighterCurrentPlayerCounter < 2: #If there are still turns left and
            if ev.type == pygame.MOUSEBUTTONDOWN:
                    fighterDieInt = random.randint(1,6)
                    pygame.time.delay(150)
                    self.fighterCurrentPlayerCounter += 1

        if(self.tempCurrentPlayerCounter == 3):
            self.tempCurrentPlayerCounter = 0

        if self.currentPlayerCounter == len(self.selectedCharacters) - 1:
            self.currentPlayerCounter == 0