from load_board import *
import pygame
from globals import*
from menuview import Menuview
from gamestate import *
from finishedview import FinishedView

class Game:
    def __init__(self, screen):
        self.screen = screen
        #generate sprite groups
        self.all_sprites_list = pygame.sprite.Group()
        self.possible_moves_group = pygame.sprite.Group()

        #starts with attackers turn
        self.is_attckers_turn = True

        self.gamestate = Menu(self)
        self.menuview = Menuview(screen)


    def draw(self):

        if isinstance(self.gamestate, Playing):
            self.screen.blit(self.game_board.grid.background, (0, 0))
            self.all_sprites_list.draw(self.screen)
            self.possible_moves_group.draw(self.screen)


    def change_game_state(self, state, text = None):
        #change the gamestate
        self.gamestate = state

        if isinstance(self.gamestate, Menu):
            #generate menu
            self.menuview = Menuview(self.screen)


        if isinstance(self.gamestate, Playing):
            #generate sprite groups
            self.all_sprites_list = pygame.sprite.Group()
            self.possible_moves_group = pygame.sprite.Group()

            #starts with attackers turn
            self.is_attckers_turn = True

            #create board and pieces
            self.game_board = board(self, '/home/alistair/Desktop/vscode_projects/Hnefentafl/board.txt', self.screen)

            self.game_board.generate_pieces()

            self.possible_moves = []

        if isinstance(self.gamestate, Finished):
            self.finishedview = FinishedView(self.screen, text)
            
    def mouse_handle(self, click_pos):
        '''handle the mouse event in accordance with the current game state'''
        if isinstance(self.gamestate, Menu):
            self.gamestate.on_event(click_pos)

        elif isinstance(self.gamestate, Playing):
            self.gamestate.on_event(click_pos)

        elif isinstance(self.gamestate, Finished):
            self.gamestate.on_event(click_pos)

    def turn_finished(self):
        if self.is_attckers_turn:
            self.is_attckers_turn = False
        else:
            self.is_attckers_turn = True
            
    def defender_wins(self):
        self.change_game_state(Finished(self), "Defenders Win")
        
    def attacker_wins(self):
        self.change_game_state(Finished(self), "Attackers win")
        
    
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
            if x == 0 and y == 0 or x == 0 and y == self.game_board.num_rows - 1:
                self.defender_wins()
            if x == self.game_board.num_cols - 1 and y == self.game_board.num_rows - 1 or y == 0 and x == self.game_board.num_cols - 1:
                self.defender_wins()

        #check if king neighboures moved pawn
        for pawn in self.game_board.pawn_neighbours(pawn):
            if isinstance(pawn, King):
                if self.is_king_taken(pawn):
                    self.attacker_wins()
            


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
        if king.position.y == 0 or king.position.x == 0 or king.position.x == self.game_board.num_cols or king.position.y == self.game_board.num_rows:
            required_neighbours -= 1

        #is square above the central square 
        if king.position.y - 1 == (self.game_board.num_rows-1)/2 and king.position.x == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1
        #is square below the central square 
        if king.position.y +1 == (self.game_board.num_rows-1)/2 and king.position.x == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1
        #is square right the central square 
        if king.position.y == (self.game_board.num_rows-1)/2 and king.position.x +1  == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1
        #is square left the central square 
        if king.position.y == (self.game_board.num_rows-1)/2 and king.position.x -1  == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1

        for pawn in self.game_board.pawn_neighbours(king):
            if pawn != None and self.is_enemy(king, pawn):
                required_neighbours -= 1

        return required_neighbours == 0
        

        
    def check_capture(self, pawn):
        '''
        only the moving piece can capture during their go
        A pawn is taken when sandwiched between two enemys on opposed sides or 1 enemy and 1 special square
         ''' 
        
        taken_pawns = self.pawn_takes(pawn)
        for pawn in taken_pawns:
            pawn.kill()

    def pawn_takes(self, pawn):
        neighbours = self.game_board.pawn_neighbours(pawn)

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

    def is_enemy(self, pawn1, pawn2):
        if pawn1 and pawn2:
            if isinstance(pawn1, Attacker) != isinstance(pawn2, Attacker):
                return True
        return False


    def is_special_square(self, position):
        for square in self.game_board.grid.special_squares:
            if position == square:
                return True
        return False
