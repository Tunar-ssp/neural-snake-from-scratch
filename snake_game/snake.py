import pygame
from .settings import CELL_PIXEL 

#neural network controlled snake



class Snake:
    def __init__(self,screen,cordinates,head_direction):
        self.screen=screen
        self.cordinates=cordinates
        self.head_direction=head_direction
    def Reset(self,cordinates,head_direction):
        self.cordinates=cordinates.copy()
        self.head_direction=head_direction.copy()

    def Move_snake(self,state):
        #up right down left
        

        x,y=self.cordinates[-1]
        
   
  

        if state == [1,0,0]:head_direction=head_direction[1:]+head_direction[1]
        elif state ==[0,0,1]:head_direction=head_direction[-1]+head_direction[:-1]
        else: pass

        if head_direction==[1,0,0,0]:y-=1
        elif head_direction==[0,1,0,0]:x+=1
        elif head_direction==[0,0,1,0]:y+=1
        elif head_direction==[0,0,0,1]:x-=1
        else:print('Direction Error')

        self.cordinates.append((x,y))
        return head_direction,self.cordinates
    




    def Check_eaten(self,Food_x,Food_y):
        
        x,y=self.cordinates[-1]
        if x== Food_x and y ==Food_y:
            return True
        else:
            self.cordinates.pop(0)
            return False



        
    def Draw_snake(self):
        for x,y in self.cordinates:
            pygame.draw.rect(self.screen, (255, 0, 0),(x*CELL_PIXEL,y*CELL_PIXEL, CELL_PIXEL, CELL_PIXEL))
      
        

        
    