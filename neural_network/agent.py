import numpy as np

class Worker:
    def __init__(self, SCREEN_WIDTH, CELL_PIXEL, SCREEN_HEIGHT):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT
        self.cell_size = CELL_PIXEL
        self.max_x = SCREEN_WIDTH // CELL_PIXEL
        self.max_y = SCREEN_HEIGHT // CELL_PIXEL

    def Run(self, Food_cord, snake_cordinates, head_direction):
        head = snake_cordinates[-1]
        
       
        # Current Head Direction as Booleans
        dir_u = head_direction[0] == 1
        dir_r = head_direction[1] == 1
        dir_d = head_direction[2] == 1
        dir_l = head_direction[3] == 1

        # Define the 8 directions to look (x, y)
        # [Up, UpRight, Right, DownRight, Down, DownLeft, Left, UpLeft]
        directions = [
            [0, -1], [1, -1], [1, 0], [1, 1], 
            [0, 1], [-1, 1], [-1, 0], [-1, -1]
        ]

       
        # We look in 8 directions. For each, we get:
        # A) Distance to Obstacle (Wall/Body) - Normalized (1 = Close, 0 = Far)
        # B) Is Food in this direct line of sight? (1 = Yes, 0 = No)
        
        vision_inputs = []
        
        for d in directions:
            # Raycast function
            res = self.cast_ray(head, d, snake_cordinates, Food_cord)
            vision_inputs.extend(res) # Adds 2 values per direction

      
        # Standard inputs to help fast reaction
        
        point_l = [head[0] - 1, head[1]]
        point_r = [head[0] + 1, head[1]]
        point_u = [head[0], head[1] - 1]
        point_d = [head[0], head[1] + 1]

        basic_inputs = [
            # Danger relative to head (3)
            (dir_r and self.is_collision(point_r, snake_cordinates)) or 
            (dir_l and self.is_collision(point_l, snake_cordinates)) or 
            (dir_u and self.is_collision(point_u, snake_cordinates)) or 
            (dir_d and self.is_collision(point_d, snake_cordinates)),

            (dir_u and self.is_collision(point_r, snake_cordinates)) or 
            (dir_d and self.is_collision(point_l, snake_cordinates)) or 
            (dir_l and self.is_collision(point_u, snake_cordinates)) or 
            (dir_r and self.is_collision(point_d, snake_cordinates)),

            (dir_d and self.is_collision(point_r, snake_cordinates)) or 
            (dir_u and self.is_collision(point_l, snake_cordinates)) or 
            (dir_r and self.is_collision(point_u, snake_cordinates)) or 
            (dir_l and self.is_collision(point_d, snake_cordinates)),

            # Move Direction (4)
            dir_l, dir_r, dir_u, dir_d,

            # General Food Direction (4)
            Food_cord[0] < head[0],  # Left
            Food_cord[0] > head[0],  # Right
            Food_cord[1] < head[1],  # Up
            Food_cord[1] > head[1]   # Down
        ]

        # Combine Vision (16) + Basic (11) = 27 Inputs
        final_state = vision_inputs + basic_inputs
        
        # Convert True/False to 1/0 and return float32 array
        return np.array(final_state, dtype=int).astype(np.float32)

    def cast_ray(self, head, direction, snake_body, food):
        x, y = head
        dx, dy = direction
        
        distance = 0
        found_food = 0
        distance_to_danger = 0
        
        # Loop until we hit a wall or body
        while True:
            x += dx
            y += dy
            distance += 1
            
            # 1. Check Wall
            if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
                distance_to_danger = 1.0 / distance # closer = hhigher number (1.0)
                break
            
            # 2. Check Body
            if [x, y] in snake_body[:-1]:
                distance_to_danger = 1.0 / distance
                break
            
            # 3. Check Food
            if x == food[0] and y == food[1]:
                found_food = 1
        
        return [distance_to_danger, found_food]

    def is_collision(self, point, snake_cordinates):
        x, y = point
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            return True
        if point in snake_cordinates[:-1]:
            return True
        return False