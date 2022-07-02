from globals import *
from pawn import Pawn
import pygame

class Defender(Pawn):

    color = (0, 255, 0)

    def __init__(self, board ,position, radius = PIECE_RADIUS):
        super().__init__(board ,position, radius)


        