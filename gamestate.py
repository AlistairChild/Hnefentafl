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
    '''decides the gamerules and the board to build the game'''
    def __init__(self, application):
        self.application = application
        
        self.rules = "Copenhagen"
        
        self.board = self.application.GAME_VARIATIONS[self.rules].allowed_boards[0]

        self.current_menu = MainMenuView(self, application)
        self.changed = True
        self.draw()
        
    def change_menu(self, menu):
        self.current_menu = menu
        self.changed = True


    def change_board(self, board):
        self.board = board

    def change_rules(self, rules):
        self.rules = rules

    def on_event(self, click_pos):
        self.current_menu.evaluate()
        
    def draw(self):
        
        self.current_menu.draw()

    def create_game(self):
        func = self.application.GAME_VARIATIONS[self.rules]
        self.application.build_game(func, self.board)
        #self.application.change_state(self.rules(board))


class Game(State):
    def __init__(self, application, board):
        self.application = application
        self.screen = application.screen
        self.board = board

        self.board = Board(self, BOARD_TYPES[self.board], self.screen)

        #starts with attackers turn
        self.is_attackers_turn = True

        #this will be moved to playing class
        self.all_sprites_list = pygame.sprite.Group()
        self.possible_moves_group = pygame.sprite.Group()

        self.win_message = None

        self.board.generate_pieces()

        self.possible_moves = []

    def turn_finished(self):
        if self.is_attackers_turn:
            self.is_attackers_turn = False
        else:
            self.is_attackers_turn = True
            
    def check_for_winner(self, pawn):
        #expect to be overriden depending on the gamerules
        raise NotImplementedError

    def check_capture(self, pawn):
        #expect to be overriden depending on the gamerules
        raise NotImplementedError

    def on_event(self, click_pos):
        self.possible_moves_group.empty()
        grid_coords = self.board.grid.get_grid_coordinates(click_pos)
        
        pawn = self.board.get_cell_object(grid_coords)

        if pawn and isinstance(pawn, Attacker) == self.is_attackers_turn:
            if isinstance(pawn, King):
                self.possible_moves = pawn.calculate_possible_moves(True)
            else:
                self.possible_moves = pawn.calculate_possible_moves()
            for coord in self.possible_moves:
                self.possible_moves_group.add(Guides(self.board, (coord.x, coord.y)))
                self.active_pawn = pawn


        for coord in self.possible_moves:
            if coord.x == grid_coords.x and coord.y == grid_coords.y:
                self.active_pawn.move(grid_coords)
                self.check_for_winner(self.active_pawn)
                self.check_capture(self.active_pawn)
                self.turn_finished()
                self.possible_moves = []
            
        if not pawn:
            self.possible_moves_group.empty()

    def draw(self):

        #draw background
        self.screen.blit(self.board.grid.background, (0, 0))
        #draw all sprites
        self.all_sprites_list.draw(self.screen)
        #draw possible moves
        self.possible_moves_group.draw(self.screen)

    def defender_wins(self):
        self.win_message = "Defenders Win"
        self.application.show_credits()
        
    def attacker_wins(self):
        self.win_message = "Attackers win"
        self.application.show_credits()

    def is_enemy(self, pawn1, pawn2):
        if pawn1 and pawn2:
            if isinstance(pawn1, Attacker) != isinstance(pawn2, Attacker):
                return True
        return False


    def is_special_square(self, position):
        for square in self.board.grid.special_squares:
            if position == square:
                return True
        return False

class Copenhagen_rules(Game):
    allowed_boards = ["Hnefentafl"]
    def __init__(self, application, board):
        super().__init__(application, board)
        
    def check_for_winner(self, pawn):
        '''
        winner occurs either when the king escapes to a corner square, or, 
        the king is surrounded by the attacking team.
        '''
        #check if king made it to corner square
        if isinstance(pawn, King):
            x = pawn.position.x
            y = pawn.position.y

            #check if king is in the corners
            if x == 0 and y == 0 or x == 0 and y == self.board.num_rows - 1:
                self.defender_wins()
            if x == self.board.num_cols - 1 and y == self.board.num_rows - 1 or y == 0 and x == self.board.num_cols - 1:
                self.defender_wins()

        #check if king neighboures moved pawn
        for pawn in self.board.pawn_neighbours(pawn):
            if isinstance(pawn, King):
                if self.is_king_taken(pawn):
                    self.attacker_wins()

    def check_capture(self, pawn):
        '''
        only the moving piece can capture during their go
        A pawn is taken when sandwiched between two enemys on opposed sides or 1 enemy and 1 special square
         ''' 
        
        taken_pawns = self.pawn_takes(pawn)
        for pawn in taken_pawns:
            pawn.kill()

    def pawn_takes(self, pawn):
        neighbours = self.board.pawn_neighbours(pawn)

        taken_pawns = []
        for pawn in neighbours:
            if pawn and self.pawn_is_taken(pawn):
                taken_pawns.append(pawn)
        return taken_pawns

    def pawn_is_taken(self, pawn):
        '''check capture condition king has a different condition'''
        pos = pawn.position

        is_enemy_above = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x, pos.y + 1)))) 
        is_enemy_below = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x, pos.y - 1))))
        is_enemy_right = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x+1, pos.y ))))
        is_enemy_left = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x-1, pos.y ))))

        #if no enemy check if special square;
        if not is_enemy_above:
            is_enemy_above = self.is_special_square((pos.x, pos.y+1))
        if not is_enemy_below:
            is_enemy_below = self.is_special_square((pos.x , pos.y - 1))
        if not is_enemy_right:
            is_enemy_right = self.is_special_square((pos.x + 1, pos.y))
        if not is_enemy_left:
            is_enemy_left = self.is_special_square((pos.x - 1, pos.y))

        if isinstance(pawn, King):
            return is_enemy_above and is_enemy_below and is_enemy_right and is_enemy_left
        else:
            return (is_enemy_above and is_enemy_below) or (is_enemy_right and is_enemy_left)

    def check_sandwich_take(self, pawn):
        '''
        A row of two or more taflmen along the board edge may be captured together, 
        by bracketing the whole group at both ends, 
        as long as every member of the row has an enemy taflman directly in front of him.
        
        '''



    def is_king_taken(self, king):
        '''
        the King is taken when surrounded by enemy pieces on all avaliable sides.
        if the king is on side of board it only needs to be surrounded by 3 pieces
        if the king is neighboring the center square the king only needs be surrounded by 3 pieces

        returns boolian
        '''
        #check neighbours
        required_neighbours = 4

        #check if king surrounds by edge
        if king.position.y == 0 or king.position.x == 0 or king.position.x == self.board.num_cols or king.position.y == self.board.num_rows:
            required_neighbours -= 1

        #is square above the central square 
        if king.position.y - 1 == (self.board.num_rows-1)/2 and king.position.x == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square below the central square 
        if king.position.y +1 == (self.board.num_rows-1)/2 and king.position.x == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square right the central square 
        if king.position.y == (self.board.num_rows-1)/2 and king.position.x +1  == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square left the central square 
        if king.position.y == (self.board.num_rows-1)/2 and king.position.x -1  == (self.board.num_cols-1)/2:
            required_neighbours -= 1

        for pawn in self.board.pawn_neighbours(king):
            if pawn != None and self.is_enemy(king, pawn):
                required_neighbours -= 1

        return required_neighbours == 0
        



class Fetlar_rules(Game):
    allowed_boards = ["Hnefentafl"]
    def __init__(self, application, board):
        super().__init__(application, board)

    def check_for_winner(self, pawn):
        '''
        winner occurs either when the king escapes to a corner square, or, 
        the king is surrounded by the attacking team.
        '''
        #check if king made it to corner square
        if isinstance(pawn, King):
            x = pawn.position.x
            y = pawn.position.y

            #check if king is in the corners
            if x == 0 and y == 0 or x == 0 and y == self.board.num_rows - 1:
                self.defender_wins()
            if x == self.board.num_cols - 1 and y == self.board.num_rows - 1 or y == 0 and x == self.board.num_cols - 1:
                self.defender_wins()

        #check if king neighboures moved pawn
        for pawn in self.board.pawn_neighbours(pawn):
            if isinstance(pawn, King):
                if self.is_king_taken(pawn):
                    self.attacker_wins()

    def check_capture(self, pawn):
        '''
        only the moving piece can capture during their go
        A pawn is taken when sandwiched between two enemys on opposed sides or 1 enemy and 1 special square
         ''' 
        
        taken_pawns = self.pawn_takes(pawn)
        for pawn in taken_pawns:
            pawn.kill()

    def pawn_takes(self, pawn):
        neighbours = self.board.pawn_neighbours(pawn)

        taken_pawns = []
        for pawn in neighbours:
            if pawn and self.pawn_is_taken(pawn):
                taken_pawns.append(pawn)
        return taken_pawns

    def pawn_is_taken(self, pawn):
        '''check capture condition king has a different condition'''
        pos = pawn.position

        is_enemy_above = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x, pos.y + 1)))) 
        is_enemy_below = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x, pos.y - 1))))
        is_enemy_right = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x+1, pos.y ))))
        is_enemy_left = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x-1, pos.y ))))

        #if no enemy check if special square;
        if not is_enemy_above:
            is_enemy_above = self.is_special_square((pos.x, pos.y+1))
        if not is_enemy_below:
            is_enemy_below = self.is_special_square((pos.x , pos.y - 1))
        if not is_enemy_right:
            is_enemy_right = self.is_special_square((pos.x + 1, pos.y))
        if not is_enemy_left:
            is_enemy_left = self.is_special_square((pos.x - 1, pos.y))

        if isinstance(pawn, King):
            return is_enemy_above and is_enemy_below and is_enemy_right and is_enemy_left
        else:
            return (is_enemy_above and is_enemy_below) or (is_enemy_right and is_enemy_left)



    def is_king_taken(self, king):
        '''
        the King is taken when surrounded by enemy pieces on all avaliable sides.
        if the king is on side of board it only needs to be surrounded by 3 pieces
        if the king is neighboring the center square the king only needs be surrounded by 3 pieces

        returns boolian
        '''
        #check neighbours
        required_neighbours = 4

        #check if king surrounds by edge
        if king.position.y == 0 or king.position.x == 0 or king.position.x == self.board.num_cols or king.position.y == self.board.num_rows:
            required_neighbours -= 1

        #is square above the central square 
        if king.position.y - 1 == (self.board.num_rows-1)/2 and king.position.x == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square below the central square 
        if king.position.y +1 == (self.board.num_rows-1)/2 and king.position.x == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square right the central square 
        if king.position.y == (self.board.num_rows-1)/2 and king.position.x +1  == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square left the central square 
        if king.position.y == (self.board.num_rows-1)/2 and king.position.x -1  == (self.board.num_cols-1)/2:
            required_neighbours -= 1

        for pawn in self.board.pawn_neighbours(king):
            if pawn != None and self.is_enemy(king, pawn):
                required_neighbours -= 1

        return required_neighbours == 0
        
    def defender_wins(self):
        self.win_message = "Defenders Win"
        self.change_game_state(Finished(self))
        
    def attacker_wins(self):
        self.win_message = "Attackers win"
        self.change_game_state(Finished(self))

class Berserk_rules(Game):
    allowed_boards = ["Hnefentafl"]
    def __init__(self, application, board):
        super().__init__(application, board)

    def check_for_winner(self, pawn):
        '''
        winner occurs either when the king escapes to a corner square, or, 
        the king is surrounded by the attacking team.
        '''
        #check if king made it to corner square
        if isinstance(pawn, King):
            x = pawn.position.x
            y = pawn.position.y

            #check if king is in the corners
            if x == 0 and y == 0 or x == 0 and y == self.board.num_rows - 1:
                self.defender_wins()
            if x == self.board.num_cols - 1 and y == self.board.num_rows - 1 or y == 0 and x == self.board.num_cols - 1:
                self.defender_wins()

        #check if king neighboures moved pawn
        for pawn in self.board.pawn_neighbours(pawn):
            if isinstance(pawn, King):
                if self.is_king_taken(pawn):
                    self.attacker_wins()

    def check_capture(self, pawn):
        '''
        only the moving piece can capture during their go
        A pawn is taken when sandwiched between two enemys on opposed sides or 1 enemy and 1 special square
         ''' 
        
        taken_pawns = self.pawn_takes(pawn)
        for pawn in taken_pawns:
            pawn.kill()

    def pawn_takes(self, pawn):
        neighbours = self.board.pawn_neighbours(pawn)

        taken_pawns = []
        for pawn in neighbours:
            if pawn and self.pawn_is_taken(pawn):
                taken_pawns.append(pawn)
        return taken_pawns

    def pawn_is_taken(self, pawn):
        '''check capture condition king has a different condition'''
        pos = pawn.position

        is_enemy_above = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x, pos.y + 1)))) 
        is_enemy_below = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x, pos.y - 1))))
        is_enemy_right = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x+1, pos.y ))))
        is_enemy_left = self.is_enemy(pawn, pawn.inspect_cell(Position((pos.x-1, pos.y ))))

        #if no enemy check if special square;
        if not is_enemy_above:
            is_enemy_above = self.is_special_square((pos.x, pos.y+1))
        if not is_enemy_below:
            is_enemy_below = self.is_special_square((pos.x , pos.y - 1))
        if not is_enemy_right:
            is_enemy_right = self.is_special_square((pos.x + 1, pos.y))
        if not is_enemy_left:
            is_enemy_left = self.is_special_square((pos.x - 1, pos.y))

        if isinstance(pawn, King):
            return is_enemy_above and is_enemy_below and is_enemy_right and is_enemy_left
        else:
            return (is_enemy_above and is_enemy_below) or (is_enemy_right and is_enemy_left)



    def is_king_taken(self, king):
        '''
        the King is taken when surrounded by enemy pieces on all avaliable sides.
        if the king is on side of board it only needs to be surrounded by 3 pieces
        if the king is neighboring the center square the king only needs be surrounded by 3 pieces

        returns boolian
        '''
        #check neighbours
        required_neighbours = 4

        #check if king surrounds by edge
        if king.position.y == 0 or king.position.x == 0 or king.position.x == self.board.num_cols or king.position.y == self.board.num_rows:
            required_neighbours -= 1

        #is square above the central square 
        if king.position.y - 1 == (self.board.num_rows-1)/2 and king.position.x == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square below the central square 
        if king.position.y +1 == (self.board.num_rows-1)/2 and king.position.x == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square right the central square 
        if king.position.y == (self.board.num_rows-1)/2 and king.position.x +1  == (self.board.num_cols-1)/2:
            required_neighbours -= 1
        #is square left the central square 
        if king.position.y == (self.board.num_rows-1)/2 and king.position.x -1  == (self.board.num_cols-1)/2:
            required_neighbours -= 1

        for pawn in self.board.pawn_neighbours(king):
            if pawn != None and self.is_enemy(king, pawn):
                required_neighbours -= 1

        return required_neighbours == 0


class Finished(State):
    def __init__(self, application):
        self.application = application
        self.game = application.game
        self.finishedview = FinishedView(self.game)

    def on_event(self, click_pos):
        self.application.show_menu()

    def draw(self):
        self.finishedview.draw()
        