import math
from globals import *

def draw_special_square(canvas,top_left, cellWidth, cellHeight ,line_width):
        '''visual design for squares reserved only for king'''
        rect = pygame.Rect((top_left.x, top_left.y), (cellWidth ,cellHeight))
        pygame.draw.rect(canvas, (50,50,50), rect)
        pygame.draw.line(canvas,(100,100,100), (top_left.x, top_left.y), (top_left.x + cellWidth, top_left.y + cellHeight), width = line_width)
        pygame.draw.line(canvas,(100,100,100), (top_left.x + cellWidth, top_left.y), (top_left.x, top_left.y + cellHeight), width = line_width)

class grid:
    def __init__(self, screen, row_number, col_number):
        '''
        passing the number of rows and cols create a grid to fit screen
        '''
        self.special_squares = {(0,0),(0,row_number-1),(col_number -1,0),(col_number -1, row_number-1)}

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

        #create special squares     
        line_width = 4
        #top left  
        top_left = Position((self.offsetx, self.offsety))
        draw_special_square(self.background, top_left, self.cellWidth, self.cellHeight, line_width)
        #bottom right
        top_left = Position((self.cellWidth*(col_number -1) + self.offsetx, self.cellHeight*(row_number-1)+self.offsety))
        draw_special_square(self.background, top_left, self.cellWidth, self.cellHeight,line_width)
        #top right
        top_left = Position((self.cellWidth*(col_number -1) + self.offsetx, self.offsety))
        draw_special_square(self.background, top_left, self.cellWidth, self.cellHeight,line_width)
        #bottom left
        top_left = Position((self.offsetx, self.cellHeight*(row_number-1)+self.offsety))
        draw_special_square(self.background, top_left, self.cellWidth, self.cellHeight,line_width)
        #central
        top_left = Position((self.cellWidth*math.floor((col_number -1)/2) + self.offsetx, self.cellHeight*math.floor((row_number)/2)+self.offsety))
        draw_special_square(self.background, top_left, self.cellWidth, self.cellHeight,line_width)

        
        for x in range(col_number):
            for y in range(row_number):
                coords = (x*self.cellWidth+self.offsetx, y*self.cellHeight+self.offsety )
                
                
                rect = pygame.Rect(coords, (self.cellWidth ,self.cellHeight))
                pygame.draw.rect(self.background, (100,100,100), rect,1)

        #blit to screen
        screen.blit(self.background, (0, 0))
        

    def get_screen_coordinates(self, input_coords):
        '''
        passing grid coordinates as a parameter get the center of the grid in screen 
        coordinates
        '''
        return (int((input_coords.x*self.cellWidth) + self.cellWidth/2 + self.offsetx), int((input_coords.y*self.cellHeight)+self.cellHeight/2+self.offsety))

    def get_grid_coordinates(self, input_coords):
        '''
        passing screen coordinates as a parameter, this return the grid coordinates 
        '''
        return Position((math.floor(input_coords[0]/self.cellWidth ), math.floor(input_coords[1]/ self.cellHeight)))
