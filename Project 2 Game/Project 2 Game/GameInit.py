import pygame
class GameInit(object):
    def __init__(self, gameStatus = 'main', selectedCharacters = [], selectedAmountBots = None, currentPlayerCounter = 0, 
                 tempCurrentPlayerCounter = 0, defaultPawnLocations = [], defaultTileLocations = [], maxAmountOfBots = 4,                                                                                                                                                   #Minimal 1 and maximum depends on how many characters are in the game, see 'players' variable. E.g. 4 = 3 bots, 1 player.
                 scoreBoardHeight = 0, randomDiceNumber = 1, firstDieIsThrown = False, mainMenuSize = [800, 600],
                 mainBackground = pygame.image.load("Images\FighterMenu.png"), background = pygame.image.load("Images\Background.png"),
                 selectBackground = pygame.image.load("Images\EmptyBackground.png"), scoreBoardBackground = pygame.image.load("Images\ScoreBoard.png"),
                 botChosen = False, charChosen = False, tileSelected = False, enableSound = True, ruleOpened = False, fighterDieInt = [],
                fighterCurrentPlayerCounter = 0, fightAttackIsChosen = False, playersAlive = 0, counter = 0, gameIsRunning = True):

        self.GameStatus = gameStatus
        self.SelectedCharacters = selectedCharacters #List of selected characters from the "new game" screen
        self.SelectedAmountBots = selectedAmountBots #How many bots he/she wants to play
        self.CurrentPlayerCounter = currentPlayerCounter #Default player
        self.TempCurrentPlayerCounter = tempCurrentPlayerCounter #Only used in the gamestatus 'fight'
        self.DefaultPawnLocations = defaultPawnLocations #The top left corner but all with a little bit of offset so the pawns are not on top of each other
        self.DefaultTileLocations = defaultTileLocations #All tiles that are possible to move on to (with a pawn)
        self.MaxAmountOfBots = maxAmountOfBots  #MAX 4 OR GIUSEPPE WILL HAVE YOUR TESTICLES          4 is actually 3. Bots means players, really.                                                                                                                                                     #Minimal 1 and maximum depends on how many characters are in the game, see 'players' variable. E.g. 4 = 3 bots, 1 player.
        self.ScoreBoardHeight = scoreBoardHeight #Define the scoreboard height, that's where the lives and conditions of each player gets displayed
        self.RandomDiceNumber = randomDiceNumber
        self.FirstDieIsThrown = firstDieIsThrown
        self.MainMenuSize = mainMenuSize
        self.MainBackground = mainBackground
        self.Background = background
        self.SelectBackground = selectBackground
        self.ScoreBoardBackground = scoreBoardBackground
        self.BotChosen = botChosen
        self.CharChosen = charChosen
        self.TileSelected = tileSelected
        self.EnableSound = enableSound
        self.RuleOpened = ruleOpened
        self.FighterDieInt = fighterDieInt
        self.FighterCurrentPlayerCounter = fighterCurrentPlayerCounter #When a player lands on a corner, this variable will be assigned to the current fighter.
        self.FightAttackIsChosen = fightAttackIsChosen #In the fightscreen, where the player has the option to select an attack
        self.PlayersAlive = playersAlive
        self.Counter = counter
        self.GameIsRunning = gameIsRunning


        