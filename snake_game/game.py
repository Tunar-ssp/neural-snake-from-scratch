import pygame
from .settings import *
from .plane import Plane
from .snake import Snake
from .food  import Food
from .gave_over import GameOverCheck
import random
import time

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock=pygame.time.Clock()
        
        self.plane=Plane(self.screen)
        self.food=Food(self.screen)
        self.Check_GameOver=GameOverCheck(self.screen)


        #setting starting pos. somewhere at the middle
        self.snake_cordinates=[[SCREEN_WIDTH //(2*CELL_PIXEL)   ,SCREEN_HEIGHT//(2*CELL_PIXEL)]]
        #creating random head direction for starting
        self.random_direction=random.randint(0,3)
        self.head_direction= [1 if i==self.random_direction else 0  for i in range(4) ]
        #

        self.snake=Snake(self.screen,self.snake_cordinates,self.head_direction)
        #used for rewarding procces
        x_head,y_head=self.snake_cordinates[-1]
        self.Reset()

        self.reward=0
        self.last_food_distance=(self.Food_x-x_head)**2+(self.Food_y-y_head)**2
        

        
    def Reset(self):
        self.snake_cordinates=[[SCREEN_WIDTH //(2*CELL_PIXEL)   ,SCREEN_HEIGHT//(2*CELL_PIXEL)]]
        
        self.random_direction=random.randint(0,3)
        self.head_direction= [1 if i==self.random_direction else 0  for i in range(4) ]

        self.Food_x,self.Food_y=self.food.Generate_food(self.snake_cordinates)
        
        
        self.score=0
        #for preventing ai from doing 'nothing'
        self.frame_iteration=0
        self.snake.Reset(self.snake_cordinates,self.head_direction)
        #used for rewarding procces
        x_head,y_head=self.snake_cordinates[-1]
        self.last_food_distance=(self.Food_x-x_head)**2+(self.Food_y-y_head)**2
        self.reward=0

        
        
    def run_game(self,state):
        print('test',self.snake_cordinates)
        self.eaten=False
        self.game_over=False

            
    

                
        #for testing i will use this after in fast mode 
        time.sleep(0.25)
        self.head_direction, self.snake_cordinates=self.snake.Move_snake(state)
        eaten=self.snake.Check_eaten(self.Food_x,self.Food_y)
        # print(f'Eaten:{eaten}')
        if self.eaten==True:
            score+=1
            self.Food_x,self.Food_y=self.food.Generate_food(self.snake_cordinates)
        else:
            self.snake_cordinates.pop(0)
        # print('test2',self.snake_cordinates)
        
       

        self.frame_iteration+=1
        print(self.snake_cordinates)
        if self.Check_GameOver.check_border_collision(self.snake_cordinates)==True or\
            self.Check_GameOver.check_snake_collision(self.snake_cordinates)==True or\
            self.frame_iteration >= 40* (self.score+1):
            self.game_over=True
            self.Reset()
            # return False
        self.calculate_reward()

        return (self.Food_x,self.Food_y),self.snake_cordinates,self.head_direction,self.game_over,self.score,self.reward

        
    def calculate_reward(self):
        if self.game_over==True:
            self.reward-=10
        if self.eaten==True:
            self.reward+=10
        else:
            x_head,y_head=self.snake_cordinates[-1]
            distance=(self.Food_x-x_head)**2+(self.Food_y-y_head)**2
            if self.last_food_distance>distance:
                self.reward+=0.1
            else:
                self.reward-=0.1
            self.last_food_distance=distance
        
        
        
        
        



    def render(self):
        self.screen.fill((0, 0,0))
        pygame.display.set_caption('Snake Game')
        self.plane.draw_grid()
        self.snake.Draw_snake()
        self.food.Draw_food()
        pygame.display.flip()