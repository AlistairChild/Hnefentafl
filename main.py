import pygame, sys
from globals import *
from game import * 

from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('Hello World!')


game = Game(screen)

while True: # main game loop

    game.draw()

    for event in pygame.event.get():

        if event.type == QUIT:

            pygame.quit()

            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                game.mouse_handle(pygame.mouse.get_pos())

    pygame.display.update()
    pygame.display.flip()


