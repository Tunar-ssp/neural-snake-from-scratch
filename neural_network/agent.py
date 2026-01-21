import numpy as np

class Worker:
    def __init__(self, SCREEN_WIDTH, CELL_PIXEL, SCREEN_HEIGHT):
        self.max_x = SCREEN_WIDTH // CELL_PIXEL
        self.max_y = SCREEN_HEIGHT // CELL_PIXEL

    def Run(self, Food_cord, snake_cordinates, head_direction):
        self.Food_cord = Food_cord
        self.snake_cordinates = snake_cordinates
        self.head_direction = head_direction

        self.food_direction()
        self.long_range_danger()
        self.immediate_danger()
        self.find_nearest_danger_distance()

        # Combine all features into one flat array for the neural network
        training_data = np.array(
            self.head_direction +            # 4 values
            self.food_direction_list +       # 4 values
            self.long_range_danger_list +    # 4 values
            self.immediate_danger_list +     # 4 values
            [self.nearest_danger_distance]   # 1 value (must be in a list to concatenate)
        ).astype(np.float32)

        return training_data

    def food_direction(self):
        # HEAD IS AT [-1]
        x_head, y_head = self.snake_cordinates[-1]
        x_food, y_food = self.Food_cord
        
        self.food_direction_list = [
            int(y_food < y_head),  # food is Up
            int(x_food > x_head),  # food is Right
            int(y_food > y_head),  # food is Down
            int(x_food < x_head),  # food is Left
        ]

    def long_range_danger(self):
        # HEAD IS AT [-1]
        x_head, y_head = self.snake_cordinates[-1]
        self.long_range_danger_list = [0, 0, 0, 0]
        
        # Check if body parts are in the same row/column as the head
        # We slice  to avoid checking the head against itself
        for x, y in self.snake_cordinates[:-1]:
            if x == x_head and y < y_head:   self.long_range_danger_list[0] = 1 # Danger Up
            elif y == y_head and x > x_head: self.long_range_danger_list[1] = 1 # Danger Right
            elif x == x_head and y > y_head: self.long_range_danger_list[2] = 1 # Danger Down
            elif y == y_head and x < x_head: self.long_range_danger_list[3] = 1 # Danger Left

    def immediate_danger(self):
        
        x_head, y_head = self.snake_cordinates[-1]
        self.immediate_danger_list = [0, 0, 0, 0]

        # Wall Checks
        if y_head - 1 < 0: self.immediate_danger_list[0] = 1
        if x_head + 1 >= self.max_x: self.immediate_danger_list[1] = 1
        if y_head + 1 >= self.max_y: self.immediate_danger_list[2] = 1
        if x_head - 1 < 0: self.immediate_danger_list[3] = 1

        #Body Checks (Immediate neighbor)
        for x, y in self.snake_cordinates[:-1]:
            if x == x_head and y == y_head - 1: self.immediate_danger_list[0] = 1
            if x == x_head + 1 and y == y_head: self.immediate_danger_list[1] = 1
            if x == x_head and y == y_head + 1: self.immediate_danger_list[2] = 1
            if x == x_head - 1 and y == y_head: self.immediate_danger_list[3] = 1

    def find_nearest_danger_distance(self):
      
        x_head, y_head = self.snake_cordinates[-1]
        
        # Distance to the 4 walls
        dists = [
            y_head,                # distance to top
            self.max_x - x_head - 1, # distance to right
            self.max_y - y_head - 1, # distance to bottom
            x_head                 # distance to left
        ]
        
        # Normalize: find the closest wall and scale 0.0 to 1.0
        min_dist = min(dists)
        self.nearest_danger_distance = np.float32(min_dist) / max(self.max_x, self.max_y)