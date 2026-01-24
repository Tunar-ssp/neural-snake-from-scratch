import pygame
from .settings import *
from .plane import Plane
from .snake import Snake
from .food  import Food
from .gave_over import GameOverCheck
import random


class Game:
    def __init__(self, Render, delay_ms=500):
        self.should_render = Render
        self.delay_ms = delay_ms
        # default rewards (will be overridden by main.py)
        self.REWARDS = {
            'game_over': -10,
            'food_eaten': 10,
            'trapped': -5,
            'closer_to_food': 0.3,
            'away_from_food': -0.3
        }

        if Render:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.clock = pygame.time.Clock()
            self.plane = Plane(self.screen)
            self.food = Food(self.screen, Render=Render)
            
        else:
            self.screen = None
            self.food = Food(Render=Render)
        self.Check_GameOver = GameOverCheck()
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
            self.snake = Snake(self.screen, self.snake_cordinates, self.head_direction, self.should_render)
        x_head, y_head = self.snake_cordinates[-1]
        self.last_food_distance = (self.Food_x - x_head)**2 + (self.Food_y - y_head)**2
        self.reward = 0

    def run_game(self, state):
        self.eaten = False
        self.game_over = False
        self.limit = int(((max_x * max_y)) * (self.score **1.05 + 1))
        
        
        self.head_direction, self.snake_cordinates = self.snake.Move_snake(state)
        
        if self.Check_GameOver.check_border_collision(self.snake_cordinates) or \
           self.Check_GameOver.check_snake_collision(self.snake_cordinates) or \
           self.frame_iteration >=  self.limit :
            self.game_over = True
            self.calculate_reward()
            if self.should_render:
                self.render()
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
        if self.should_render:
            self.render()
        return (self.Food_x, self.Food_y), self.snake_cordinates, self.head_direction, False, self.score, self.reward

    def calculate_reward(self):
        if self.game_over:
            self.reward = self.REWARDS['game_over']
            return
        if self.eaten:
            self.reward = self.REWARDS['food_eaten']
            return


        if self.is_trapped():
            self.reward = self.REWARDS['trapped']
            return
        
        x_head, y_head = self.snake_cordinates[-1]
        dist = (self.Food_x - x_head)**2 + (self.Food_y - y_head)**2
        if dist < self.last_food_distance:
            self.reward = self.REWARDS['closer_to_food']
        else:
            self.reward = self.REWARDS['away_from_food']
        self.last_food_distance = dist
    
    def is_trapped(self):

        head = self.snake_cordinates[-1]
        body_set = set(tuple(c) for c in self.snake_cordinates[:-1])
        max_x = SCREEN_WIDTH // CELL_PIXEL
        max_y = SCREEN_HEIGHT // CELL_PIXEL
        
        
        directions = [
            (head[0], head[1] - 1),  # Up
            (head[0] + 1, head[1]),  # Right
            (head[0], head[1] + 1),  # Down
            (head[0] - 1, head[1])   # Left
        ]
        
        blocked_count = 0
        for x, y in directions:
            # Check if out of bounds
            if x < 0 or x >= max_x or y < 0 or y >= max_y:
                blocked_count += 1
            # Check if hits own body
            elif (x, y) in body_set:
                blocked_count += 1
        
        # Trapped if all 4 directions are blocked
        return blocked_count == 4

    def render(self):
        self.screen.fill((0, 0, 0))
        self.plane.draw_grid()
        self.snake.Draw_snake()
        self.food.Draw_food()
        pygame.display.flip()
        fps = 1000 / self.delay_ms
        self.clock.tick(fps)