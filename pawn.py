import pygame
import math
from globals import *

class Pawn(pygame.sprite.Sprite):

    # Must override in sub-classes
    color = None

    def __init__(self, board ,position, radius):
        super().__init__()

        self.board = board
        self.position = position
        # self.color = color
        self.radius = radius
        self.destroyed = False
        self.grid = self.board.grid
        #print(team)

        self.image = pygame.Surface([2*self.radius , 2*self.radius ])

        pygame.draw.circle(self.image, color = self.color, center = (self.radius , self.radius ), radius= self.radius)
  
        self.rect = self.image.get_rect()
       
        
        self.rect.x, self.rect.y = self.grid.get_screen_coordinates(self.position)
        self.rect.x, self.rect.y = self.rect.x - self.radius, self.rect.y-self.radius

    def move(self, location):
        self.rect.x, self.rect.y  =  self.grid.get_screen_coordinates(location)
        self.rect.x, self.rect.y = self.rect.x - self.radius, self.rect.y-self.radius
        self.position = location

    def update(self):
        print("hi")
    
    def calculate_possible_moves(self):
        '''Return list of grid coordinates'''
        moves = []

        # Up
        pos = self.position
        while pos[1] > 0:
            pos = (pos[0], pos[1] - 1)
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)

        # Down
        pos = self.position
        while pos[1] < self.board.num_cols - 1:
            pos = (pos[0], pos[1] + 1)
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)

        # Left
        pos = self.position
        while pos[0] > 0:
            pos = (pos[0] - 1, pos[1])
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)

        # Right
        pos = self.position
        while pos[0] < self.board.num_rows - 1:
            pos = (pos[0] + 1, pos[1])
            if self.inspect_cell(pos):
                break # hit an obstacle
            else:
                moves.append(pos)

        return moves

    def inspect_cell(self, location):
        return self.board.get_cell_object(location)
        