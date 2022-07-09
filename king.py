from globals import *
from defender import Defender
import pygame

class King(Defender):
    
    color = (20, 20, 255)

    def __init__(self, board, position):
        super().__init__(board, position, PIECE_RADIUS*1.5)
