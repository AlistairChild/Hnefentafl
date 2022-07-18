import pygame
import math

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900

PIECE_RADIUS = 20

BOARD_TYPES = {
    'Alea Evangelii' : '/home/alistair/Desktop/vscode_projects/Hnefentafl/alea_evangelle_board.txt',
    'Ard Rí' : '/home/alistair/Desktop/vscode_projects/Hnefentafl/ard_ri_board.txt',
    'Brandubh' : '/home/alistair/Desktop/vscode_projects/Hnefentafl/brandubh_board.txt',
    'Hnefentafl' : '/home/alistair/Desktop/vscode_projects/Hnefentafl/board.txt',
    'Tablut' : '/home/alistair/Desktop/vscode_projects/Hnefentafl/tablut_board.txt',
    'Tawlbwrdd' : '/home/alistair/Desktop/vscode_projects/Hnefentafl/tawlbwrdd_board.txt',
}

class Position:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]










