import pygame
import math
from globals import *
from view import Button
from view import size
from layout import calculate_button_height
from layout import calculate_button_layout


class MainMenuView:
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        self.screen = game.screen
        self.options = ["Play Game (%s)"%game.board, "Change game mode"]
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.buttons = []


    def draw(self):
        #fill screen with black
        self.background.fill((0, 0, 0))
        #populate menu
        for i in calculate_button_layout(self.options):
            self.buttons.append(Button(self, i[0], i[1], i[2], self.on_click))

        self.screen.blit(self.background, (0, 0))


    def evaluate(self):
        if self.buttons:
            for button in self.buttons:
                button.evaluate()

    def on_click(self, data):
        if data == self.options[0]:
            self.parent.change_game_state()
        elif data == self.options[1]:
            self.parent.change_menu(GameTypeView(self.parent, self.game))

class GameTypeView:
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        self.screen = game.screen
        self.options = list(BOARD_TYPES.keys())
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.buttons = []

    def draw(self):
        #fill screen with black
        self.background.fill((0, 0, 0))

        #populate menu
        for i in calculate_button_layout(self.options):
            self.buttons.append(Button(self, i[0], i[1], i[2], self.on_click))

        self.screen.blit(self.background, (0, 0))


    def evaluate(self):
        if self.buttons:
            for button in self.buttons:
                button.evaluate()

    def on_click(self, data):
        self.game.change_board(data)
        self.parent.change_menu(MainMenuView(self.parent, self.game))

        

class Menuview:
    def __init__(self, game):
        font = pygame.font.SysFont('freesanbold.ttf', 50)

        #preset to hnefentafl
        self.game_selected = "Hnefatafl"
    
        self.screen = game.screen
        self.game = game
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))


        self.show_main_menu()

    def show_main_menu(self):
        #options to display on main menu.
        self.main_menu = ["Play Game (%s)"%self.game_selected, "Change game mode"]
        #fill screen with black
        self.background.fill((0, 0, 0))
        #clear the existing menu
        self.game.gamestate.clear_menu()
        #populate menu
        for i in calculate_button_layout(self.main_menu):
            Button(self, i[0], i[1], i[2], self.on_click)

        self.screen.blit(self.background, (0, 0))

    def draw(self):
        '''
        self.active_menu.draw()
        
        
        '''

        
    def on_click(self, gameType):


        if gameType == "Change game mode":
            self.game_options()

        elif gameType == game_types[0]:
            self.game_selected = game_types[0]
            self.show_main_menu()
        elif gameType == game_types[1]:
            self.game_selected = game_types[1] 
            self.show_main_menu()
        elif gameType == game_types[2]:
            self.game_selected = game_types[2]
            self.show_main_menu()
        elif gameType == game_types[3]:
            self.game_selected = game_types[3]
            self.show_main_menu()
        elif gameType == game_types[4]:
            self.game_selected = game_types[4]
            self.show_main_menu()

            
             
    
    def game_options(self):
        #fill screen with black
        self.background.fill((0, 0, 0))
        #clear the existing menu
        self.game.gamestate.clear_menu()
        #populate menu
        for i in calculate_button_layout(game_types):
            Button(self, i[0], i[1], i[2], self.on_click)

        self.screen.blit(self.background, (0, 0))




