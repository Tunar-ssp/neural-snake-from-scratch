import pygame
from .settings import SCREEN_HEIGHT,SCREEN_WIDTH,CELL_PIXEL


class Plane:
    def __init__(self,screen,color=(255,255,255)):
        self.screen= screen
        self.color = color
    


    def draw_grid(self):

        
        for i in range(CELL_PIXEL,SCREEN_HEIGHT,CELL_PIXEL):
            pygame.draw.line(self.screen,self.color,(i,0),(i,SCREEN_WIDTH))
        for i in range(CELL_PIXEL,SCREEN_WIDTH,CELL_PIXEL):
            pygame.draw.line(self.screen,self.color,(0,i),(SCREEN_HEIGHT,i))