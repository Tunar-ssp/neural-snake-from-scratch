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

        # [Up, UpRight, Right, DownRight, Down, DownLeft, Left, UpLeft]
        directions = [
            [0, -1], [1, -1], [1, 0], [1, 1], 
            [0, 1], [-1, 1], [-1, 0], [-1, -1]
        ]

        vision_inputs = []
        for d in directions:
            res = self.cast_ray(head, d, snake_cordinates, Food_cord)
            vision_inputs.extend(res) 


        point_l = [head[0] - 1, head[1]]
        point_r = [head[0] + 1, head[1]]
        point_u = [head[0], head[1] - 1]
        point_d = [head[0], head[1] + 1]

        basic_inputs = [
            # Immediate Danger (Front, Left, Right) relative to head
            # Front: direction the snake is moving
            (dir_u and self.is_collision(point_u, snake_cordinates)) or 
            (dir_r and self.is_collision(point_r, snake_cordinates)) or 
            (dir_d and self.is_collision(point_d, snake_cordinates)) or 
            (dir_l and self.is_collision(point_l, snake_cordinates)),

            # Left: 90° counterclockwise from current direction
            (dir_u and self.is_collision(point_l, snake_cordinates)) or 
            (dir_r and self.is_collision(point_u, snake_cordinates)) or 
            (dir_d and self.is_collision(point_r, snake_cordinates)) or 
            (dir_l and self.is_collision(point_d, snake_cordinates)),

            # Right: 90° clockwise from current direction
            (dir_u and self.is_collision(point_r, snake_cordinates)) or 
            (dir_r and self.is_collision(point_d, snake_cordinates)) or 
            (dir_d and self.is_collision(point_l, snake_cordinates)) or 
            (dir_l and self.is_collision(point_u, snake_cordinates)),

            # Move Direction One-Hot
            dir_l, dir_r, dir_u, dir_d,

            # Food Quadrant Booleans
            Food_cord[0] < head[0],  # Left
            Food_cord[0] > head[0],  # Right
            Food_cord[1] < head[1],  # Up
            Food_cord[1] > head[1]   # Down
        ]

        food_dx = (Food_cord[0] - head[0]) / self.max_x
        food_dy = (Food_cord[1] - head[1]) / self.max_y
        food_dist_norm = np.sqrt(food_dx**2 + food_dy**2)

        vec_front, vec_left, vec_right = [0,0], [0,0], [0,0]
        
        if dir_u:
            vec_front, vec_left, vec_right = [0, -1], [-1, 0], [1, 0]
        elif dir_r:
            vec_front, vec_left, vec_right = [1, 0], [0, -1], [0, 1]
        elif dir_d:
            vec_front, vec_left, vec_right = [0, 1], [1, 0], [-1, 0]
        elif dir_l:
            vec_front, vec_left, vec_right = [-1, 0], [0, 1], [0, -1]
            
        body_dist_f = self.cast_body_only_ray(head, vec_front, snake_cordinates)
        body_dist_l = self.cast_body_only_ray(head, vec_left, snake_cordinates)
        body_dist_r = self.cast_body_only_ray(head, vec_right, snake_cordinates)


        total_cells = self.max_x * self.max_y
        free_cells = total_cells - len(snake_cordinates)
        free_space_ratio = free_cells / total_cells


        # Heuristic: If we are far enough from tail, we are likely not trapped in a tight loop
        tail = snake_cordinates[0]
        can_reach_tail = 1 if (abs(head[0] - tail[0]) + abs(head[1] - tail[1])) > 1 else 0

        advanced_inputs = [
            food_dx, 
            food_dy, 
            food_dist_norm,
            body_dist_f, 
            body_dist_l, 
            body_dist_r,
            free_space_ratio, 
            can_reach_tail
        ]

        # Combine: 16 + 11 + 8 = 35 Inputs
        final_state = vision_inputs + basic_inputs + advanced_inputs
        
        return np.array(final_state, dtype=float).astype(np.float32)

    def cast_ray(self, head, direction, snake_body, food):
        x, y = head
        dx, dy = direction
        
        distance = 0
        found_food = 0
        distance_to_danger = 0
        
        while True:
            x += dx
            y += dy
            distance += 1
            
            # Check Wall
            if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
                distance_to_danger = 1.0 / distance 
                break
            
            #  Check Body
            if [x, y] in snake_body[:-1]:
                distance_to_danger = 1.0 / distance
                break
            
            # Check Food
            if x == food[0] and y == food[1]:
                found_food = 1
        
        return [distance_to_danger, found_food]

    def cast_body_only_ray(self, head, direction, snake_body):

        x, y = head
        dx, dy = direction
        distance = 0
        
        while True:
            x += dx
            y += dy
            distance += 1
            
            if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
                return 0
           
            if [x, y] in snake_body[:-1]:
                return 1.0 / distance
                
        return 0

    def is_collision(self, point, snake_cordinates):
        x, y = point
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            return True
        if point in snake_cordinates[:-1]:
            return True
        return False