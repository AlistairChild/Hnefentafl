from gamestate import Menu, Finished, Game, Copenhagen_rules, Fetlar_rules, Berserk_rules


class Application:
    '''
    manages the current application state forwarding events to their handlers.

    '''
    GAME_VARIATIONS = {
    "Copenhagen": Copenhagen_rules,
    "Fetlar Rules": Fetlar_rules,
    "Berserk": Berserk_rules
    }
    
    def __init__(self, screen):
        
        self.screen = screen
        self.menu = Menu(self)
        self.credits = None
    
        #the starting state is the menu state
        self.state = self.menu

    def handle_mouse_click(self, click_pos):
        self.state.on_event(click_pos)

    def build_game(self, game: Game, board):
        '''build a game with the rules and board as selected in the menu'''
        # TODO: check board is compatible with game
        self.game= game(self, board)
   
        self.state = self.game

    def show_menu(self):
        self.state = self.menu

    def show_credits(self):

        if not self.credits and self.game:
            self.credits = Finished(self)
        self.state = self.credits

    def update(self):
        self.state.draw()