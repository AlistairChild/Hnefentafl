from pawn import Pawn
import pygame
from globals import *

class Attacker(Pawn):

    color = (255, 0, 0)

    def __init__(self, board, position):
        super().__init__(board ,position, PIECE_RADIUS)