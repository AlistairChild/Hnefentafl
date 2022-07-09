from pawn import *
import pygame

class Guides(Pawn):
    color = (200, 200, 200)
    def __init__(self, board, position):
        super().__init__(board, position, PIECE_RADIUS/2)

        