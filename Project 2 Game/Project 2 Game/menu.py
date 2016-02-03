import pygame
import options

class GameMenu():
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, font_size= 30, font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color  
       
        self.items = []
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
            
            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            total_height = len(items) * height
            posy = (self.scr_height / 2) - (total_height / 2) + (index * height)
         
            self.items.append([item, label, (width, height), (posx, posy)])
        
    def run(self):
        mainloop = True
        while mainloop:
            for name, label, (width, height), (posx, posy) in self.items:
                    self.screen.blit(label, (posx, posy))

        for option in menu:#Draw all options on the screen
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()

            pygame.display.flip()