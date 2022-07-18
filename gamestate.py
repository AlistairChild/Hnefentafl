from attacker import Attacker
from king import King
from guides import Guides
import pygame
from menuview import MainMenuView
from finishedview import FinishedView
from board import Board
from globals import *

class State:
    def __init__(self):
        pass
    def on_event(self):
        pass

class Menu(State):
    def __init__(self, game):
        self.game = game
        self.current_menu = MainMenuView(self, game)
        self.changed = True
        self.draw()
        
    def change_menu(self, menu):
        self.current_menu = menu
        self.changed = True

    def on_event(self, click_pos):
        self.current_menu.evaluate()
        
    def draw(self):
        if self.changed:
            self.current_menu.draw()
        self.changed = False

    def change_game_state(self):
        #next state is always Playing
        self.game.change_game_state(Playing(self.game))



class Playing(State):
    def __init__(self, game):
        self.game = game
        #generate sprite groups
        self.game.all_sprites_list.empty()
        self.game.possible_moves_group.empty()

        #starts with attackers turn
        self.game.is_attckers_turn = True

        #create board and pieces
        self.game.game_board = Board(self.game, BOARD_TYPES[self.game.board], self.game.screen)

        self.game.game_board.generate_pieces()

        self.game.possible_moves = []

    def on_event(self, click_pos):

        self.game.possible_moves_group.empty()
        grid_coords = self.game.game_board.grid.get_grid_coordinates(click_pos)
        
        pawn = self.game.game_board.get_cell_object(grid_coords)

        if pawn and isinstance(pawn, Attacker) == self.game.is_attckers_turn:
            if isinstance(pawn, King):
                self.game.possible_moves = pawn.calculate_possible_moves(True)
            else:
                self.game.possible_moves = pawn.calculate_possible_moves()
            for coord in self.game.possible_moves:
                self.game.possible_moves_group.add(Guides(self.game.game_board, (coord.x, coord.y)))
                self.game.active_pawn = pawn


        for coord in self.game.possible_moves:
            if coord.x == grid_coords.x and coord.y == grid_coords.y:
                self.game.active_pawn.move(grid_coords)
                self.game.check_for_winner(self.game.active_pawn)
                self.game.check_capture(self.game.active_pawn)
                self.game.turn_finished()
                self.game.possible_moves = []
            
        if not pawn:
            self.game.possible_moves_group.empty()

    def draw(self):
        #draw background
        self.game.screen.blit(self.game.game_board.grid.background, (0, 0))
        #draw all sprites
        self.game.all_sprites_list.draw(self.game.screen)
        #draw possible moves
        self.game.possible_moves_group.draw(self.game.screen)

class Finished(State):
    def __init__(self, game):
        self.game = game
        self.finishedview = FinishedView(self.game.screen, self.game.win_message)
    def on_event(self, click_pos):
        self.game.change_game_state(Menu(self.game))
    def draw(self):
        self.finishedview.draw()
        