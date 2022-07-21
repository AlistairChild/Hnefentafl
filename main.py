import pygame, sys

from globals import *
from application import Application
from gamestate import Game
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tafl')
black_cursor = pygame.image.load('images/Black_cursor.png').convert_alpha()
red_cursor = pygame.image.load('images/red_cursor.png').convert_alpha()
green_cursor = pygame.image.load('images/green_cursor.png').convert_alpha()

black_cursor = pygame.transform.scale(black_cursor, (PIECE_RADIUS, PIECE_RADIUS))
green_cursor = pygame.transform.scale(green_cursor, (2*PIECE_RADIUS, 2*PIECE_RADIUS))
red_cursor = pygame.transform.scale(red_cursor, (2*PIECE_RADIUS, 2*PIECE_RADIUS))

pygame.mouse.set_visible(False)
cursor_img_rect = black_cursor.get_rect()

application = Application(screen)

while True: # main game loop
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                application.handle_mouse_click(pygame.mouse.get_pos())       
    
    application.update()
    
    cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
    # draw the cursor
    if isinstance(application.state, Game):
        if application.state.is_attackers_turn:
            screen.blit(red_cursor, cursor_img_rect) 
        else:
            screen.blit(green_cursor, cursor_img_rect) 
    else:
        screen.blit(black_cursor, cursor_img_rect) 
    pygame.display.flip()


