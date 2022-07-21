from pawn import * 
from guides import Guides
from attacker import Attacker
from defender import Defender
from king import King
import pygame
from globals import*
import math
from grid import *
from boards import *

class Board:
    '''holds the grid and pieces'''
    def __init__(self, game, path, screen):

        self.screen = screen
        self.cells = BOARDS[path]
        self.game = game

        self.num_rows = len(self.cells)
        self.num_cols = len(self.cells[0]) 
        self.grid = grid(self.screen, self.num_cols,  self.num_rows )

        self.characters = [[0 for i in range(len(self.cells))] for i in range(len(self.cells[0]))]


    def generate_pieces(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                if self.cells[i][j] == 0:
                    self.characters[i][j] = None
                elif self.cells[i][j] == 1:
                    self.game.all_sprites_list.add(Attacker(self, (i,j)))
                elif self.cells[i][j] == 2:
                    self.game.all_sprites_list.add(Defender(self, (i,j)))
                elif self.cells[i][j] == 3:  
                    self.game.all_sprites_list.add(King(self, (i,j)))
                else:
                    print("Please assign piece number %s an object" %self.cells[i][j])


    def get_cell_object(self, position) ->Pawn:
        '''get item in cell or None'''
        for sprite in self.game.all_sprites_list:
            if sprite.position.x == position.x and sprite.position.y == position.y:
                return sprite
        return None

    def pawn_neighbours(self, pawn):
        pos = pawn.position
        n_positions = (Position((pos.x, pos.y + 1)), Position((pos.x, pos.y - 1)), Position((pos.x+1, pos.y)), Position((pos.x-1, pos.y)))
        return [pawn.inspect_cell(npos) for npos in n_positions]

