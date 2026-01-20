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

    def Move_snake(self, state):
        x, y = self.cordinates[-1]
        #up right down left
        # Rotate direction
        idx = self.head_direction.index(1)

        if state == [0, 0, 1]:   
            idx = (idx + 1) % 4
        elif state == [1, 0, 0]: 
            idx = (idx - 1) % 4
        # [1, 0, 0] is straight  so idx stays the same

     
        self.head_direction = [0, 0, 0, 0]
        self.head_direction[idx] = 1

        
        if idx == 0: y -= 1    # Up
        elif idx == 1: x += 1  # Right
        elif idx == 2: y += 1  # Down
        elif idx == 3: x -= 1  # Left

        self.cordinates.append([x, y])

        self.cordinates.append([x, y])
        return self.head_direction, self.cordinates
        




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
      
        

        
    