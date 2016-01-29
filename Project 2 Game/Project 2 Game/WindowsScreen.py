import pygame,sys

class WindowsScreen(pygame.sprite.Sprite):
    def __init__(self,screen , text ,backgroundImg ,brush, fontSize = 40):
        super(WindowsScreen, self).__init__()
        self.surf = pygame.Surface(screen.get_size())
        
        #Loading BackgroundImage
        self.surf.blit(pygame.transform.scale(pygame.image.load(backgroundImg),screen.get_size()),(0,0))
        self.rect = self.surf.get_rect()
        
        #Loading Messages 
        self.Text = text
        self.Brush = pygame.font.Font(brush, fontSize)
        self.Brush = self.Brush.render(text, 1, (255,255,0))
        
        #size handmatig aanpassen
        self.surf.blit(self.Brush, (screen.get_width() / 4, 150))