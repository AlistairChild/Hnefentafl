from attacker import Attacker
from king import King
from guides import Guides
import pygame


class State:
    def __init__(self):
        pass
    def on_event(self):
        pass

class Menu(State):
    def __init__(self, game):
        self.game = game
    def on_event(self, click_pos):
        self.game.change_game_state(Playing(self.game))

class Playing(State):
    def __init__(self, game):
        self.game = game
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
                self.game.possible_moves_group.add(Guides(self.game.game_board, (coord.x,coord.y)))
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

class Finished(State):
    def __init__(self, game):
        self.game = game
    def on_event(self, click_pos):
        self.game.change_game_state(Playing(self.game))