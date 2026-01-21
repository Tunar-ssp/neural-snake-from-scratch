from .settings import CELL_PIXEL, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

class GameOverCheck:
    def __init__(self):
        self.max_x = SCREEN_WIDTH // CELL_PIXEL
        self.max_y = SCREEN_HEIGHT // CELL_PIXEL

    def check_snake_collision(self, cordinates):
        if len(cordinates) < 2: return False
        head = cordinates[-1]
        return head in cordinates[:-1]

    def check_border_collision(self, cordinates):
        x, y = cordinates[-1]
        return x < 0 or y < 0 or x >= self.max_x or y >= self.max_y
    




    