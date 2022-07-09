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
            

    def print_winner(self):
        print("winner")

    def defender_wins(self):
        self.change_game_state(Finished(self), "Defenders Win")
        
    def attacker_wins(self):
        self.change_game_state(Finished(self), "Attackers win")
        
    
    def check_for_winner(self, pawn):

        #check if king made it to corner square
        if isinstance(pawn, King):
            x = pawn.position.x
            y = pawn.position.y

            #check if king is in the corners
            if x == 0 and y == 0 or x == 0 and y == self.game_board.num_rows - 1:
                self.defender_wins()
            if x == self.game_board.num_cols - 1 and y == self.game_board.num_rows - 1 or y == 0 and x == self.game_board.num_cols - 1:
                self.defender_wins()



        for pawn in self.game_board.pawn_neighbours(pawn):
            if isinstance(pawn, King):
                if self.is_king_taken(pawn):
                    self.attacker_wins()
            

        #check if king neighboures moved pawn
        #check if king is surrounded

    def is_king_taken(self, king):
        #check neighbours
        required_neighbours = 4

        #check if king surrounds by edge
        if king.position.y == 0 or king.position.x == 0 or king.position.x == self.game_board.num_cols or king.position.y == self.game_board.num_rows:
            required_neighbours -= 1

        #is square above central
        if king.position.y - 1 == (self.game_board.num_rows-1)/2 and king.position.x == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1
        #square below central
        if king.position.y +1 == (self.game_board.num_rows-1)/2 and king.position.x == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1
        #square right central
        if king.position.y == (self.game_board.num_rows-1)/2 and king.position.x +1  == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1
        #square left central
        if king.position.y == (self.game_board.num_rows-1)/2 and king.position.x -1  == (self.game_board.num_cols-1)/2:
            required_neighbours -= 1

        print(len(self.game_board.pawn_neighbours(king)))
        for coord in self.game_board.pawn_neighbours(king):
            if coord != None:
                required_neighbours -= 1
        return required_neighbours == 0
        

        
    def check_capture(self, pawn):
        '''
        check both sides of the pawn in interest for a capture:
         a capture takes place when a peice from one team has 2 peices either side of it either top/bottom or right left

         - - -          - X -           - * -     - - - - - 
         * X *   or     - * -   or      - X -     X * X X * 
         - - -          - X -           - * -     - - - - - 
        
         ''' 
        
        taken_pawns = self.pawn_takes(pawn)
        for pawn in taken_pawns:
            #delete pawn
            if isinstance(pawn, King):
                self.print_winner()
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

        if isinstance(pawn, King):
            return is_enemy_above and is_enemy_below and is_enemy_right and is_enemy_left
        else:
            return (is_enemy_above and is_enemy_below) or (is_enemy_right and is_enemy_left)

    def is_enemy(self, pawn1, pawn2):
        if pawn1 and pawn2:
            if isinstance(pawn1, Attacker) != isinstance(pawn2, Attacker):
                return True
        return False