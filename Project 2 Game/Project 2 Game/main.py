import sys
import pygame
import options

Option = options.Option
pygame.init()

screen = pygame.display.set_mode((480, 320))
font = pygame.font.Font(None, 40)


options = [Option("NEW GAME", (140, 105), font, screen), Option("LOAD GAME", (135, 155), font, screen),
           Option("OPTIONS", (145, 205), font, screen)]
while True:
    pygame.event.pump()
    screen.fill((0, 0, 0))
    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
        else:
            option.hovered = False
        option.draw()
    pygame.display.update()






#screensize = width, height = 1000, 600
#startmenusize = width, height = 200, 500
#circle = pygame.transform.scale(pygame.image.load('Images/circle.jpg'), (30,30))
#board = pygame.transform.scale(pygame.image.load('Images/board.png'), (600,600))

#startmenu = pygame.display.set_mode()
#screen = pygame.display.set_mode(screensize)
##screen.fill(black)

#def main():
#    while True:#Main game loop
#       screen.blit(board, (0, 0))
#       screen.blit(circle, (10,10))
#       pygame.display.update()
#main()