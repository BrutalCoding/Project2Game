import pygame
from Rules import *

class Rules_Screen():
    def __init__(self, screen,screenVectorSize,selectBackground,ev):
        self.Screen = screen
        self.ScreenVectorSize = screenVectorSize
        self.SelectBackground = selectBackground
        self.Event = ev
        self.Rules = Rules
        self.Font = pygame.font.Font(None, 40)
  
    def FontSize(self, size, typeFont):
        if typeFont == "Brush": 
            font_path = "./Fonts/Brushstrike.ttf"
            return pygame.font.Font(font_path, size)
        elif typeFont == "Super":
            font_path = "./Fonts/Superstar.ttf"
            return pygame.font.Font(font_path, size)
        else:
            return pygame.font.Font(None, size)

    def Show(self):
        self.Screen.blit(pygame.transform.scale(self.SelectBackground,(self.ScreenVectorSize["x"],self.ScreenVectorSize["y"])), (0, 0))
        if self.Event.type == pygame.QUIT:
            gameIsRunning = False
        if self.Event.type == pygame.KEYUP:
            if self.Event.key == pygame.K_ESCAPE:
                gameStatus = 'main'
                self.ScreenVectorSize["x"] = mainMenuSize[0]
                self.ScreenVectorSize["y"] = mainMenuSize[1]
                self.ScreenVectorSize(self.ScreenVectorSize, self.Screen)
        labelHeight = self.Screen.get_rect().midtop[1]
        for rule in self.Rules.LoadAllRules():
            text = self.FontSize(25, None).render(rule, 1, (217, 30, 24))
            textpos = text.get_rect()
            labelHeight += 25
            self.Screen.blit(text, (self.Screen.get_rect().centerx / 4, labelHeight))
        text = self.Font.render("Press 'ESC' to get back to the main menu", 1, (255,255,0))
        textpos = text.get_rect()
        self.Screen.blit(text, (self.Screen.get_rect().centerx / 4, self.Screen.get_size()[1] - 50))


