import pygame

class size:
    def __init__(self, width, height):
        self.x = width
        self.y = height

class Margin:
    def __init__(self, left, right, top, bottom):
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom

class Button:
    def __init__(self, parent, top_left_pos, size, text, callback_function = None):
        self.pos = top_left_pos
        self.size = size
        self.callback_function = callback_function
        self.text = text
        self.parent = parent
        self.font = pygame.font.SysFont('freesanbold.ttf', 50)
        
        self.draw()

    def draw(self):
        self.buttonSurface = pygame.Surface((self.size.x, self.size.y))
        self.buttonRect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.buttonSurf = self.font.render(self.text, True, (255, 255, 255))
        self.buttonSurface.fill((0,0,255))
        self.buttonSurface.blit(self.buttonSurf , [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])

        self.parent.background.blit(self.buttonSurface,self.buttonRect)

    def evaluate(self):
        click_pos = pygame.mouse.get_pos()
        if self.is_button_clicked(click_pos):
            if self.callback_function:
                self.callback_function(self.text)
        
    def is_button_clicked(self, click_pos):
        if click_pos[0] >=self.pos.x and click_pos[0] <= self.pos.x + self.size.x and click_pos[1] >= self.pos.y and click_pos[1]<= self.pos.y+self.size.y:
            return True

