from load_board import *

class Game:
    def __init__(self, screen):
        print("start the engine")

        self.game_board = board('/home/alistair/Desktop/vscode_projects/Hnefentafl/board.txt', screen)

        self.game_board.generate_pieces()

    def mouse_handle(self, click_pos):
        self.game_board.on_click(click_pos)
    

