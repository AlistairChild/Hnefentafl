from pawn import Pawn
import pygame
from globals import *

class Attacker(Pawn):

    color = (220, 20, 20)

    def __init__(self, board, position):
        super().__init__(board ,position, PIECE_RADIUS)