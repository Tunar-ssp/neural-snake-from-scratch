import pygame
from .settings import *
from .plane import Plane
from .snake import Snake
from .food  import Food
from .gave_over import GameOverCheck
import random
class Game:
    def __init__(self):
        pygame.init()
        
        self.screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock=pygame.time.Clock()
        
        self.plane=Plane(self.screen)
        self.food=Food(self.screen)
        self.game_over=GameOverCheck(self.screen)


        #
        self.snake_cordinates=[[SCREEN_WIDTH //(2*CELL_PIXEL)   ,SCREEN_HEIGHT//(2*CELL_PIXEL)]]
        
        self.random_direction=random.randint(0,3)
        self.head_direction= [1 if i==self.random_direction else 0  for i in range(4) ]
        #

        self.snake=Snake(self.screen,self.snake_cordinates,self.head_direction)
        
        self.Reset()
    def Reset(self):
        self.snake_cordinates=[[SCREEN_WIDTH //(2*CELL_PIXEL)   ,SCREEN_HEIGHT//(2*CELL_PIXEL)]]
        
        self.random_direction=random.randint(0,3)
        self.head_direction= [1 if i==self.random_direction else 0  for i in range(4) ]

        self.Food_x,self.Food_y=self.food.Generate_food(self.snake_cordinates)
        

        self.score=0
        #for preventing ai from doing 'nothing'
        self.frame_iteration=0
        self.snake.Reset(self.cordinates,self.head_direction)


        
        
    def run_game(self,state):
        current_time=pygame.time.get_ticks()
        eaten=False

            
    

                
        #for testing i will use this after in fast mode 
        if current_time-last_move >= MOVE_INTERVAL:

            cordinates=self.snake.Move_snake(state)
            eaten=self.snake.Check_eaten(Food_x,Food_y)
            if eaten==True:
                score+=1
                Food_x,Food_y=self.food.Generate_food(cordinates)
            last_move=current_time

        self.frame_iteration+=1
        if self.game_over.check_border_collision(cordinates)==True or\
            self.game_over.check_snake_collision(cordinates)==True or\
            self.frame_iteration >= 40* (score+1):
            game_over=True
            self.Reset()
            # return False
        

        return (self.Food_x,self.Food_y),self.snake_cordinates,self.head_direction,game_over,score

        




    def render(self):
        self.screen.fill((0, 0,0))
        pygame.display.set_caption('Snake Game')
        # self.plane.draw_grid()
        self.snake.Draw_snake()
        self.food.Draw_food()