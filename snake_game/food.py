import random
import pygame
from .settings import CELL_PIXEL,SCREEN_WIDTH,SCREEN_HEIGHT




class Food:
    def __init__(self,screen,color=(0,255,0),radius=2.5,width=0):
        self.screen=screen
        self.Food_x=None
        self.Food_y=None
        self.color=color
        self.radius=CELL_PIXEL//radius
        self.width=width
    def Generate_food(self,cordinates):
        x_cord,y_cord=[],[]
        for x,y in cordinates:
            x_cord.append(x)
            y_cord.append(y)
        while True:
            self.Food_x=random.randint(0,SCREEN_WIDTH//CELL_PIXEL-1)
            if self.Food_x not in x_cord:break
        while True:
            self.Food_y=random.randint(0,SCREEN_HEIGHT//CELL_PIXEL-1)
            if self.Food_y not in y_cord:break
        return self.Food_x,self.Food_y
    
    
    def Draw_food(self):
        pygame.draw.circle(self.screen,
                           self.color,
                           ((self.Food_x+0.5) *CELL_PIXEL,(self.Food_y+0.5)*CELL_PIXEL),
                           self.radius,
                           self.width
        )
        
        


    
    