from .ai import model
import numpy as np

class Worker:
    def __init__(self,SCREEN_WIDTH,CELL_PIXEL,SCREEN_HEIGHT):
        self.max_x=SCREEN_WIDTH//CELL_PIXEL
        self.max_y=SCREEN_HEIGHT//CELL_PIXEL
        self.Run_Model=model.Run()
        
        
    def Run(self,Food_cord,snake_cordinates,head_direction,score):
        self.Food_cord=Food_cord
        self.snake_cordinates=snake_cordinates
        self.head_direction=head_direction
        


        self.food_direction()
        self.long_range_danger()
        self.immediate_danger()
        self.find_nearest_danger_distance()

        training_data=np.array(self.food_direction_list+
                               self.long_range_danger_list+
                               self.immediate_danger_list+
                               self.nearest_danger_distance
        )
        reward=0
        state=self.Run_Model(training_data,reward)




        return state



    def food_direction(self):
        x_head,y_head=self.snake_cordinates[0]
        x_food,y_food=self.Food_cord
        self.food_direction_list=[]
        #up right down left
        #We check if food is up right down left  from head?
        self.food_direction_list = [
            int(y_food < y_head),  # up
            int(x_food > x_head),  # right
            int(y_food > y_head),  # down
            int(x_food < x_head),  # left
        ]

    def long_range_danger(self):
        x_head,y_head=self.snake_cordinates[-1]
        
        self.max_distance=self.max_x **2 +self.max_y**2
        
        
        self.long_range_danger_list=[0,0,0,0]
        #up right down left
        
        for x,y in self.snake_cordinates[1:]:
            if x==x_head and y<y_head: #up
                self.long_range_danger_list[0]=1
            elif y==y_head and x>x_head: # right
                self.long_range_danger_list[1]=1
            elif  x==x_head and y>y_head: # down
                self.long_range_danger_list[2]=1
            elif y==y_head and x<x_head:  # left
                self.long_range_danger_list[3]=1
            
            if x**2+y**2<self.max_distance:self.max_distance=x**2+y**2
    def immediate_danger(self):
        x_head,y_head=self.snake_cordinates[-1]
        self.immediate_danger_list=[0,0,0,0]
        if y_head - 1 < 0: self.immediate_danger_list[0] = 1
        if x_head + 1 >= self.max_x: self.immediate_danger_list[1] = 1
        if y_head + 1 >= self.max_y: self.immediate_danger_list[2] = 1
        if x_head - 1 < 0: self.immediate_danger_list[3] = 1

        for x,y in self.snake_cordinates[:-1]:
                
            if x == x_head and y == y_head - 1: self.immediate_danger_list[0] = 1
            if x == x_head + 1 and y == y_head: self.immediate_danger_list[1] = 1
            if x == x_head and y == y_head + 1: self.immediate_danger_list[2] = 1
            if x == x_head - 1 and y == y_head: self.immediate_danger_list[3] = 1
    def find_nearest_danger_distance(self):
        
        x_head,y_head=self.snake_cordinates[-1]
        if abs(x_head-self.max_x)**2>self.max_distance:
            self.nearest_danger_distance=abs(x_head-self.max_x)**2
        if abs(y_head-self.max_y)**2>self.max_distance:
            self.nearest_danger_distance=abs(y_head-self.max_y)**2
        else:
            self.nearest_danger_distance=self.max_distance
        self.nearest_danger_distance=np.float32(self.nearest_danger_distance)/ np.sqrt((self.max_x **2 +self.max_y**2))
    



        


