import pygame
import math
from globals import *



class Pawn(pygame.sprite.Sprite):

    # Must override in sub-classes
    color = None

    def __init__(self, board ,position, radius):
        super().__init__()

        self.board = board
        self.position = Position(position)
        self.radius = radius
        self.grid = self.board.grid

        self.image = pygame.Surface([2*self.radius , 2*self.radius])
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, color = self.color, center = (self.radius , self.radius ), radius= self.radius)
  
        self.rect = self.image.get_rect()
        x, y = self.grid.get_screen_coordinates(self.position)
        self.rect.x, self.rect.y = x - self.radius, y - self.radius

    def move(self, location):
        x, y =  self.grid.get_screen_coordinates(location)
        self.rect.x, self.rect.y = x - self.radius, y - self.radius
        self.position = Position((location.x, location.y))

    
    def calculate_possible_moves(self, is_king = False):
        '''Return list of grid coordinates'''
        moves = []

        # Up
        pos = self.position
        while pos.y > 0:
            pos = Position((pos.x, pos.y - 1))
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)

        # Down
        pos = self.position
        while pos.y < self.board.num_cols - 1:
            pos = Position((pos.x, pos.y + 1))
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)

        # Left
        pos = self.position
        while pos.x > 0:
            pos = Position((pos.x - 1, pos.y))
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)

        # Right
        pos = self.position
        while pos.x < self.board.num_rows - 1:
            pos = Position((pos.x + 1, pos.y))
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)
        
        #Only the king is allowed in the special squares
        if not is_king:
            moves = [move for move in moves if (move.x,move.y) not in self.grid.special_squares ]

        return moves



    def inspect_cell(self, position):
        return self.board.get_cell_object(position)
        