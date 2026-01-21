from snake_game import SnakeGame
from neural_network import WorkerAgent,MlModel
from snake_game import settings
import numpy as np
import csv
import plot_save
Game_settings = (settings.SCREEN_WIDTH,settings.CELL_PIXEL,settings.SCREEN_HEIGHT)
import time
import random



def main():
    game=SnakeGame()
    plotter = plot_save.LivePlotter()
    
    CreateData=WorkerAgent(*Game_settings)
    TrainModel=MlModel(input_size=17, hidden1=256, hidden2=64, output_size=3)
    
    learning_rate=0.0005
    gamma=0.9


    epsilon=1.0 # 100% random moves at start
    epsilon_min=0.01
    epsilon_decay=0.995



    game_count=1
    moves=0
    max_score=0
    number_of_moves=[]

    score_per_round=[]

    Food_cord = (game.Food_x, game.Food_y)
    snake_cordinates = game.snake_cordinates
    head_direction = game.head_direction
    score = game.score
    
    
    total_reward_per_round=[]
    total_reward_per_round_temp=[]

    loss_per_game_temp = [] 
    avg_loss_history = []
    try:
        while True:
            Training_data=CreateData.Run(Food_cord,snake_cordinates,head_direction)
            print(f'Training data:{Training_data}')
            prediction_current = TrainModel.forward_propagation(Training_data)
            print(f'prediction_current:{prediction_current}')
            if random.random() <= epsilon:
                action_idx = random.randint(0, 2)  
            else:

                action_idx = np.argmax(prediction_current)
            
            
            
            # time.sleep(0.01)
            
            
            state_action = [0, 0, 0]
            state_action[action_idx] = 1
            
            Food_cord,snake_cordinates,head_direction,game_over,score,reward=game.run_game(state_action)
            
            print(
            f"Food__cord      = {Food_cord}\n"
            f"Snake_cordinates= {snake_cordinates}\n"
            f"Head_direction  = {head_direction}\n"
            f"Game_over       = {game_over}\n"
            f"Score           = {score}\n"
            f"Reward          = {reward}"
            )
                
            game.render()

            training_data_next = CreateData.Run(Food_cord, snake_cordinates, head_direction)
            prediction_next = TrainModel.forward_propagation(training_data_next)
            
            target_f = prediction_current.copy()
            
            Q_new = reward
            if not game_over:
                Q_new=TrainModel.calculate_Q_target(reward,prediction_next,gamma)





           
            
            target_f[0][action_idx] = Q_new
            loss_gradient = prediction_current - target_f

            current_mse = np.mean(np.square(loss_gradient))
            loss_per_game_temp.append(current_mse)
            total_reward_per_round_temp.append(reward)






            TrainModel.gradient_descent(loss_gradient)
            TrainModel.backward_propagation(learning_rate)

            






            moves+=1
            if game_over==True:
                if score > max_score:
                    max_score = score
                    TrainModel.save_model(f"model_best_{max_score}.npz")

                score_per_round.append(score)
                total_reward_per_round.append(sum(total_reward_per_round_temp))
                number_of_moves.append(moves)
                
                avg_loss_history.append(np.mean(loss_per_game_temp))
                plotter.update(score_per_round, number_of_moves, avg_loss_history)

                total_reward_per_round_temp=[]
                loss_per_game_temp = []
                moves=0
                game_count+=1
                if epsilon > epsilon_min:
                    epsilon *= epsilon_decay
            
            
                
                
            
            target_f[0][action_idx] = Q_new


    except KeyboardInterrupt:
        print('-----------Training Stopped by Keyboard Interrupt -----------')
    finally:
        print("Saving final model and stats...")
        TrainModel.save_model("models/model_final.npz")
        
        plot_save.save_stats_to_csv(game_count,number_of_moves,score_per_round, total_reward_per_round)
        print("Done. Safe to close.")



        


        


        

        




        

        
    
        
        

    

if __name__=="__main__":
    main()