from snake_game import Game
from neural_network import WorkerAgent,MlModel
from snake_game import settings
import numpy as np
Game_settings = (settings.SCREEN_WIDTH,settings.CELL_PIXEL,settings.SCREEN_HEIGHT)




def main():
    game=Game()
    
    CreateData=WorkerAgent(*Game_settings)
    TrainModel=MlModel(input_size=17, hidden1=256, hidden2=64, output_size=3)
    
    learning_rate=0.01
    gamma=0.9


    moves=0
    number_of_moves=[]

    score_per_round=[]
    
    
    total_reward_per_round=[]
    total_reward_per_round_temp=[]
    
    while True:
        Training_data=CreateData.Run(Food_cord,snake_cordinates,head_direction,score)
        prediction_current=TrainModel.forward_propagation(Training_data)
        action_idx = np.argmax(prediction_current)
        state_action = [0, 0, 0]
        state_action[action_idx] = 1
        
        Food_cord,snake_cordinates,head_direction,game_over,score,reward=game.run_game(state_action)
        game.render()

        training_data_next = CreateData.Run(Food_cord, snake_cordinates, head_direction, score)
        prediction_next = TrainModel.forward_propagation(training_data_next)

        target_f = prediction_current.copy()
        
        Q_new = reward
        if not game_over:
            Q_new=TrainModel.calculate_Q_target(reward,prediction_next,gamma)
            
             
        
        target_f[0][action_idx] = Q_new


        loss_gradient = prediction_current - target_f
        
        TrainModel.gradient_descent(loss_gradient)
        TrainModel.backward_propagation(learning_rate)

        
        if game_over:
            pass


        


        


        
        total_reward_per_round_temp.append(reward)
        moves+=1
        if game_over==True:
            score_per_round.append(score)
            total_reward_per_round.append(total_reward_per_round_temp)
            total_reward_per_round_temp=[]
            number_of_moves.append(moves)
            moves=0
        




        

        
    
        
        

    

if __name__=="__main__":
    main()