import pygame
import math
from globals import *
from view import Button
from view import size
from layout import calculate_button_height
from layout import calculate_button_layout
from boards import BOARDS

class MainMenuView:
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        self.screen = game.screen
        self.options = ["Play/n(%s, %s)"%(self.parent.rules, self.parent.board), "Change rules", "Change Board"]
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.buttons = []

        for i in calculate_button_layout(self.options):
            self.buttons.append(Button(self, i[0], i[1], i[2], self.on_click))

        self.screen.blit(self.background, (0, 0))

    def draw(self):
        #fill screen with black
        self.background.fill((0, 0, 0))
        #populate menu
        for button in self.buttons:
            button.draw()
        self.screen.blit(self.background, (0, 0))

    def evaluate(self):
        if self.buttons:
            for button in self.buttons:
                button.evaluate()

    def on_click(self, data):
        if data == self.options[0]:

            self.parent.create_game()
        elif data == self.options[1]:
            self.parent.change_menu(GameRulesMenu(self.parent, self.game))
        elif data == self.options[2]:
            self.parent.change_menu(BoardMenu(self.parent, self.game))

class GameRulesMenu:
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        self.screen = game.screen
        self.options = list(game.GAME_VARIATIONS.keys())
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.buttons = []

        for i in calculate_button_layout(self.options):
            self.buttons.append(Button(self, i[0], i[1], i[2], self.on_click))

    def draw(self):
        #fill screen with black
        self.background.fill((0, 0, 0))
        
        #populate menu
        for button in self.buttons:
            button.draw()

        self.screen.blit(self.background, (0, 0))


    def evaluate(self):
        if self.buttons:
            for button in self.buttons:
                button.evaluate()

    def on_click(self, data):
        
        self.parent.change_rules(data)
        self.parent.change_menu(MainMenuView(self.parent, self.game))

       
class BoardMenu:
    def __init__(self, parent, application):
        self.application = application
        self.parent = parent
        self.screen = application.screen
        self.options = list(self.application.GAME_VARIATIONS[self.parent.rules].allowed_boards)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.buttons = []

        for i in calculate_button_layout(self.options):
            self.buttons.append(Button(self, i[0], i[1], i[2], self.on_click))

    def draw(self):
        #fill screen with black
        self.background.fill((0, 0, 0))

        #populate menu
        for button in self.buttons:
            button.draw()

        self.screen.blit(self.background, (0, 0))


    def evaluate(self):
        if self.buttons:
            for button in self.buttons:
                button.evaluate()

    def on_click(self, data):
        self.parent.change_board(data)
        self.parent.change_menu(MainMenuView(self.parent, self.application))

        


