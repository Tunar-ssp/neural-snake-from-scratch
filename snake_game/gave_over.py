from .settings import CELL_PIXEL,SCREEN_HEIGHT,SCREEN_WIDTH
import pygame




class GameOverCheck:
    def __init__(self,screen):
        self.screen=screen
        self.max_x=SCREEN_WIDTH//CELL_PIXEL
        self.max_y=SCREEN_HEIGHT//CELL_PIXEL
    def check_snake_collision(self,cordinates):
        x_head,y_head=cordinates[-1]

        for x_body,y_body in cordinates[:len(cordinates)-1]:
            if x_head ==x_body  and y_body == y_head:
                return True
        return False
            
        


    def check_border_collision(self,cordinates):
        x_head,y_head=cordinates[-1]
        if x_head<0 or y_head<0 or x_head>self.max_x-1 or y_head>self.max_y-1:
            return True
        return False
        