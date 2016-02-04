import pygame

pygame.font.init()

class Option:
    hovered = False
    selected = False
    def __init__(self, text, pos, font, screen, id):
        self.text = text
        self.pos = pos
        self.font = font
        self.screen = screen
        self.id = id
        self.set_rect()
        self.draw()
            
    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        menu_font = self.font
        self.rend = menu_font.render(self.text, True, self.get_color())
    
    def get_color(self):
        if self.hovered:
            return (255, 0, 0)
        elif self.selected:
            return (255, 255, 0)
        else:
            return (255, 255, 255)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

    def fontSize(size, typeFont):
        if typeFont == "Brush": 
            font_path = "./Fonts/Brushstrike.ttf"
        elif typeFont == "Super":
            font_path = "./Fonts/Superstar.ttf"
        elif typeFont == "lcd":
            font_path = "./Fonts/LCD-N.TTF"
        else:
            return pygame.font.Font(None, size)
        return pygame.font.Font(font_path, size)