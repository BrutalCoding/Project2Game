import pygame
from Option import *

class Option_Screen():
    def __init__(self, screen,screenVectorSize,selectBackground,ev):
        self.Screen = screen
        self.ScreenVectorSize = screenVectorSize
        self.SelectBackground = selectBackground
        self.Event = ev
        self.Rules = Rules
        self.Font = pygame.font.Font(None, 40)

    def Show(self):
        screen.blit(pygame.transform.scale(selectBackground,(screenVectorSize["x"],screenVectorSize["y"])), (0, 0))
        label = fontSize(50, "Brush").render("Option menu", 1, (255, 0, 0))
        screen.blit(label, (260, 50))
        geluid = pygame.mixer.get_num_channels()
        if enableSound == True:
                buttonsOptionScreen[1].selected = True
        elif enableSound == False:
            buttonsOptionScreen[0].selected = True
        selectScreen.drawOptions(buttonsOptionScreen)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for option in buttonsOptionScreen:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    for button in buttonsOptionScreen:
                        button.selected = False
                    if option.id == 99:
                        enableSound = False
                        pygame.mixer.music.stop()
                        option.selected = True
                    elif option.id == 98:
                        enableSound = True
                        option.selected = True
                    elif option.id == mainMenuGameID:
                            selectedCharacters, selectedAmountBots, latestSelectedChar = resetSelections(selectedCharacters, selectedAmountBots, latestSelectedChar)
                            gameStatus = 'main'
                            setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 1000)
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                #mainmenusound#
                setDefaultSoundSystem(enableSound,"Sounds\Intro_Soft_Touch.mp3", 300)
                screenVectorSize["x"] = mainMenuSize[0]
                screenVectorSize["y"] = mainMenuSize[1]
                setScreenVectorSize(screenVectorSize, screen)
                selectedCharacters, selectedAmountBots = selectScreen.resetSelections(selectedCharacters, selectedAmountBots)
                selectedCharacters = [] #List of selected characters from the "new game" screen
                firstDieIsThrown = False
                yourChar = None
                latestSelectedChar = None
                player = Player



