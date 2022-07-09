import pygame
import math

class FinishedView:
    def __init__(self, screen, text):
        font = pygame.font.SysFont('freesanbold.ttf', 50)

        self.screen = screen

        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))


        # Render the texts that you want to display
        text = font.render(text, True, (0, 255, 0))
        text1 = font.render("Click to restart", True, (0, 255, 0))
        # crete a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        textRect1 = text1.get_rect()
        
        # setting center for the first text
        textRect.center = (math.floor(screen.get_size()[0]/2), math.floor(screen.get_size()[1]/2))
        textRect1.center = (math.floor(screen.get_size()[0]/2), math.floor(screen.get_size()[1]/2) + math.floor(screen.get_size()[1]/16) )
        
        

        self.background.blit(text, textRect)
        self.background.blit(text1, textRect1)


        screen.blit(self.background, (0, 0))