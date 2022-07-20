import pygame 
from view import size
from globals import *

def calculate_button_layout(button_names):
    '''returns a list of [top_right, size, label]'''
    n = len(button_names)
    button_height = calculate_button_height(n)
    gap = button_height / 4
    button_layout = []

    for i in range(n):
        top_right_y = button_height + i * button_height + i * gap
        height = button_height
        width = SCREEN_WIDTH * 0.6
        top_right_x = math.floor(SCREEN_WIDTH/2 - width/2)
        button_layout.append((Position((top_right_x, top_right_y)), size(width,height), button_names[i]))

    return button_layout

def calculate_button_height(n):
    '''
    the screen should have enough space to have n+2 buttons and n-1 gaps.
    
    '''
    return SCREEN_HEIGHT/ ((5*n)/4 + (7/4))