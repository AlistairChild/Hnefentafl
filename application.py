from menu import Menu
from finished import Finished

class Application:
    '''
    manages the current application state forwarding events to their handlers.

    '''
    def __init__(self, screen):
        self.menu = Menu(self)
        self.screen = screen
        self.credits = Finished(self)
        #the starting state is the menu state
        self.state = self.menu

    def handle_mouse_click(self, pos):'
        self.state.on_event(click_pos)

    def build_game(self, game: Game, board):
        '''build a game with the rules and board as selected in the menu'''
        # TODO: check board is compatible with game
        game_instance = game(board)
        game_instance.build_ruleset()
        game.build_board()

        self.state = game

    def show_menu():
        self.state = self.menu

    def show_credits():
        self.state = self.credits

    def update(self):
        self.state.draw()