import pygame, sys
from globals import *
from game import * 

from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('Hello World!')


game = Game(screen)

while True: # main game loop
    screen.blit(game.game_board.grid.background, (0, 0))
    game.game_board.all_sprites_list.draw(screen)
    game.game_board.possible_moves_group.draw(screen)

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


