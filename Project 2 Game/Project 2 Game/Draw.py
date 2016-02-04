import pygame

class Draw:
    def drawImage(screen, imgName, imgSize, imgPosition):
        screen.blit(pygame.transform.scale(pygame.image.load("Images/" + imgName), (imgSize[0], imgSize[1],)), (imgPosition[0],imgPosition[1]))