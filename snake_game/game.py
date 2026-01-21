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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.plane = Plane(self.screen)
        self.food = Food(self.screen)
        self.Check_GameOver = GameOverCheck(self.screen)
        self.Reset()

    def Reset(self):
        self.snake_cordinates = [[SCREEN_WIDTH // (2 * CELL_PIXEL), SCREEN_HEIGHT // (2 * CELL_PIXEL)]]
        self.random_direction = random.randint(0, 3)
        self.head_direction = [1 if i == self.random_direction else 0 for i in range(4)]
        self.Food_x, self.Food_y = self.food.Generate_food(self.snake_cordinates)
        self.score = 0
        self.frame_iteration = 0
        if hasattr(self, 'snake'):
            self.snake.Reset(self.snake_cordinates, self.head_direction)
        else:
            self.snake = Snake(self.screen, self.snake_cordinates, self.head_direction)
        x_head, y_head = self.snake_cordinates[-1]
        self.last_food_distance = (self.Food_x - x_head)**2 + (self.Food_y - y_head)**2
        self.reward = 0

    def run_game(self, state):
        self.eaten = False
        self.game_over = False
        time.sleep(0.05)
        
        self.head_direction, self.snake_cordinates = self.snake.Move_snake(state)
        
        if self.Check_GameOver.check_border_collision(self.snake_cordinates) or \
           self.Check_GameOver.check_snake_collision(self.snake_cordinates) or \
           self.frame_iteration >= 100 * (self.score + 1):
            self.game_over = True
            self.calculate_reward()
            res = (self.Food_x, self.Food_y), self.snake_cordinates, self.head_direction, True, self.score, self.reward
            self.Reset()
            return res

        self.eaten = self.snake.Check_eaten(self.Food_x, self.Food_y)
        if self.eaten:
            self.score += 1
            self.Food_x, self.Food_y = self.food.Generate_food(self.snake_cordinates)
            x_head, y_head = self.snake_cordinates[-1]
            self.last_food_distance = (self.Food_x - x_head)**2 + (self.Food_y - y_head)**2
        else:
            self.snake_cordinates.pop(0)

        self.frame_iteration += 1
        self.calculate_reward()
        return (self.Food_x, self.Food_y), self.snake_cordinates, self.head_direction, False, self.score, self.reward

    def calculate_reward(self):
        if self.game_over:
            self.reward = -10
            return
        if self.eaten:
            self.reward = 10
            return
        
        x_head, y_head = self.snake_cordinates[-1]
        dist = (self.Food_x - x_head)**2 + (self.Food_y - y_head)**2
        self.reward = 0.1 if dist < self.last_food_distance else -0.2
        self.last_food_distance = dist

    def render(self):
        self.screen.fill((0, 0, 0))
        self.plane.draw_grid()
        self.snake.Draw_snake()
        self.food.Draw_food()
        pygame.display.flip()