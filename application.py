from gamestate import Menu, Finished, Game, Copenhagen_rules, Fetlar_rules, Berserk_rules


class Application:
    '''
    manages the current application state forwarding events to their handlers.

    '''
    #TODO: change this 
    GAME_VARIATIONS = {
    "Copenhagen": Copenhagen_rules,
    "Fetlar Rules": Fetlar_rules,
    "Berserk": Berserk_rules
    }

    def __init__(self, screen):
        self.screen = screen
        self.menu = None
        self.credits = None

        #show menu on application entry
        self.show_menu()

    def handle_mouse_click(self, click_pos):
        '''pass event to the current state'''
        self.state.on_event(click_pos)

    def build_game(self, game: Game, board):
        '''build a game with the rules and board as selected in the menu'''
        # TODO: check board is compatible with game
        self.game= game(self, board)
   
        self.state = self.game

    def show_menu(self):
        '''create menu if not already else/ and set current state to menu'''
        if not self.menu:
            self.menu = Menu(self)
        self.state = self.menu

    def show_credits(self):
        '''create credits if not already else/ and set current state to credits'''
        if not self.credits and self.game:
            self.credits = Finished(self)
        self.state = self.credits

    def update(self):
        '''forward call to the current state'''
        self.state.draw()