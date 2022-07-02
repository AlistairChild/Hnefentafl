import math
from globals import *

class grid:
    def __init__(self, screen, row_number, col_number):
        '''
        passing the number of rows and cols create a grid to fit screen
        '''

        #divide the screen width/height by the number of cols/rows get the cell/row width/height
        self.cellWidth = math.floor(screen.get_size()[0] / col_number)
        self.cellHeight = math.floor(screen.get_size()[1] / row_number)

        #board grid dimensions may not be devisor of screen width therefore shift by half offset
        self.offsetx = (SCREEN_WIDTH - (row_number * self.cellWidth))/2
        self.offsety = (SCREEN_HEIGHT - (col_number * self.cellHeight))/2

        # Create The self.background
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        #draw grid onto the self.background
        for x in range(col_number):
            for y in range(row_number):
                coords = (x*self.cellWidth+self.offsetx, y*self.cellHeight+self.offsety )
                
                
                rect = pygame.Rect(coords, (self.cellWidth ,self.cellHeight))
                pygame.draw.rect(self.background, (255,255,255), rect, 1)

        # Display The self.background
        screen.blit(self.background, (0, 0))
        

    def get_screen_coordinates(self, input_coords):
        '''
        passing grid coordinates as a parameter get the center of the grid in screen 
        coordinates
        '''
        return (int((input_coords[0]*self.cellWidth) + self.cellWidth/2 + self.offsetx), int((input_coords[1]*self.cellHeight)+self.cellHeight/2+self.offsety))

    def get_grid_coordinates(self, input_coords):
        '''
        passing screen coordinates as a parameter, this return the grid coordinates 
        '''
        return (math.floor(input_coords[0]/self.cellWidth ), math.floor(input_coords[1]/ self.cellHeight))
