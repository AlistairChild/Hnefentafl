from pawn import * 
from guides import Guides
from attacker import Attacker
from defender import Defender
from king import King
import pygame
from globals import*
import math
from grid import *

class board:
    """pass a path to a text file with the board layout to initialise"""
    def __init__(self, path, screen):
        self.x, self.y = SCREEN_WIDTH, SCREEN_HEIGHT
        self.all_sprites_list = pygame.sprite.Group()
        self.possible_moves_group = pygame.sprite.Group()
        self.screen = screen
        self.file = open(path, 'r')
        self.cells = []
        self.active_pawn =None
        self.possible_moves = []
        
        rows = self.file.read().splitlines()
        self.image = pygame.Surface((PIECE_RADIUS, PIECE_RADIUS))
        for item in rows:
            self.cells.append(item.split(" "))
        
        self.cellWidth = math.floor(screen.get_size()[0] / len(self.cells[0]))
        self.cellHeight = math.floor(screen.get_size()[1] / len(self.cells))

        self.num_rows = len(self.cells)
        self.num_cols = len(self.cells[0]) 
        self.grid = grid(self.screen, self.num_cols,  self.num_rows )

        self.characters = [[0 for i in range(len(self.cells))] for i in range(len(self.cells[0]))]


    def generate_pieces(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                if self.cells[i][j] == "0":
                    self.characters[i][j] = None
                elif self.cells[i][j] == "1":
                    self.all_sprites_list.add(Attacker(self, (i,j)))
                elif self.cells[i][j] == "2":
                    self.all_sprites_list.add(Defender(self, (i,j)))
                else:  
                    self.all_sprites_list.add(King(self, (i,j)))

    
    def on_click(self, location):
        '''selects a characted showing possible moves'''

        self.possible_moves_group.empty()
        grid_coords = self.grid.get_grid_coordinates(location)

        pawn = self.get_cell_object(grid_coords)

        if pawn:
            self.possible_moves = pawn.calculate_possible_moves()
            for coord in self.possible_moves:
                self.possible_moves_group.add(Guides(self, coord))
                self.active_pawn = pawn

        if grid_coords in self.possible_moves:
            self.active_pawn.move(grid_coords)
            self.check_capture(self.active_pawn)
            self.possible_moves = []
            
        if not pawn:
            self.possible_moves_group.empty()
        

    
    def get_cell_object(self, location) ->Pawn:
        '''get item in cell or None'''
        for sprite in self.all_sprites_list:
            if sprite.position == location:
                return sprite
        return None


    def pawn_neighbours(self, pawn):

        pos = pawn.position
        n_positions = ((pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0]+1, pos[1]), (pos[0]-1, pos[1]))
        return [pawn.inspect_cell(npos) for npos in n_positions]

    def pawn_takes(self, pawn):

        neighbours = self.pawn_neighbours(pawn)

        taken_pawns = []
        for pawn in neighbours:
            if pawn and self.pawn_is_taken(pawn):
                taken_pawns.append(pawn)
        return taken_pawns

    def is_enemy(self, pawn1, pawn2):
        if pawn1 and pawn2:
            if isinstance(pawn1, Attacker) != isinstance(pawn2, Attacker):
                return True
        return False


    def pawn_is_taken(self, pawn):

        pos = pawn.position

        is_enemy_above = self.is_enemy(pawn, pawn.inspect_cell((pos[0], pos[1] + 1)))
        is_enemy_below = self.is_enemy(pawn, pawn.inspect_cell((pos[0], pos[1] - 1)))
        is_enemy_right = self.is_enemy(pawn, pawn.inspect_cell((pos[0]+1, pos[1] )))
        is_enemy_left = self.is_enemy(pawn, pawn.inspect_cell((pos[0]-1, pos[1] )))

        return (is_enemy_above and is_enemy_below) or (is_enemy_right and is_enemy_left)

    def check_capture(self, pawn):
        '''
        check both sides of the pawn in interest for a capture:
         a capture takes place when a peice from one team has 2 peices either side of it either top/bottom or right left

         - - -          - X -           - * -     - - - - - 
         * X *   or     - * -   or      - X -     X * X X * 
         - - -          - X -           - * -     - - - - - 
        
         ''' 
        #has pawn been taken
        if self.pawn_is_taken(pawn):
            #delete pawn
            pawn.kill()
        else:
            taken_pawns = self.pawn_takes(pawn)
            for pawn in taken_pawns:
                #delete pawn
                pawn.kill()

