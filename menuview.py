import pygame
import math

class Menuview:
    def __init__(self, screen):
        font = pygame.font.SysFont('freesanbold.ttf', 50)

        self.screen = screen

        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))


        # Render the texts that you want to display
        text = font.render('Play Game', True, (0, 255, 0))
        # crete a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        
        # setting center for the first text
        textRect.center = (math.floor(screen.get_size()[0]/2), math.floor(screen.get_size()[1]/2))
        
        

        self.background.blit(text, textRect)


        screen.blit(self.background, (0, 0))
