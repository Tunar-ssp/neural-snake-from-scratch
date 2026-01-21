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
    game=SnakeGame(Render=False)
    plotter = plot_save.LivePlotter()
    
    CreateData=WorkerAgent(*Game_settings)
    TrainModel=MlModel(input_size=27, hidden1=256, hidden2=64, output_size=3)
    
    learning_rate=0.00005
    gamma=0.9


    epsilon=1.0 # 100% random moves at start
    epsilon_min=0.01
    epsilon_decay=0.998



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
    
    epsilon_history = []
    q_values_per_episode = []
    q_values_current_episode = []
    try:
        while True:
            Training_data=CreateData.Run(Food_cord,snake_cordinates,head_direction)
            #print(f'Training data:{Training_data}')#
            prediction_current = TrainModel.forward_propagation(Training_data)
            #print(f'prediction_current:{prediction_current}')
            if random.random() <= epsilon:
                action_idx = random.randint(0, 2)  
            else:

                action_idx = np.argmax(prediction_current)
            
            
            
            # time.sleep(0.01)
            
            
            state_action = [0, 0, 0]
            state_action[action_idx] = 1
            
            Food_cord,snake_cordinates,head_direction,game_over,score,reward=game.run_game(state_action)
            
            # print(
            # f"Food__cord      = {Food_cord}\n"
            # f"Snake_cordinates= {snake_cordinates}\n"
            # f"Head_direction  = {head_direction}\n"
            # f"Game_over       = {game_over}\n"
            # f"Score           = {score}\n"
            # f"Reward          = {reward}\n"
            # f"Epsilon          = {epsilon}"
            
            # )
                
            # game.render()

            training_data_next = CreateData.Run(Food_cord, snake_cordinates, head_direction)
            prediction_next = TrainModel.forward_propagation(training_data_next)
            
            target_f = prediction_current.copy()
            
            Q_new = reward
            if not game_over:
                Q_new=TrainModel.calculate_Q_target(reward,prediction_next,gamma)





           
            
            target_f[0][action_idx] = Q_new
            loss_gradient = prediction_current - target_f
            loss_gradient = np.clip(loss_gradient, -1.0, 1.0)

            current_mse = np.mean(np.square(loss_gradient))
            loss_per_game_temp.append(current_mse)
            total_reward_per_round_temp.append(reward)
            q_values_current_episode.append(np.mean(prediction_current))







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
                epsilon_history.append(epsilon)
                
                # Calculate average Q-values for this episode
                if len(q_values_current_episode) > 0:
                    avg_q_val = np.mean(q_values_current_episode)
                    q_values_per_episode.append(avg_q_val)
                else:
                    q_values_per_episode.append(0)
                
                plotter.update(score_per_round, number_of_moves, avg_loss_history, 
                              epsilon_history, total_reward_per_round, q_values_per_episode)

                total_reward_per_round_temp=[]
                loss_per_game_temp = []
                q_values_current_episode = []
                moves=0
                game_count+=1
                if epsilon > epsilon_min:
                    epsilon *= epsilon_decay
            # if game_count >600:
            #     time.sleep(0.05)
            #     game.render()
            
                
                
            



    except KeyboardInterrupt:
        print('-----------Training Stopped by Keyboard Interrupt -----------')
    finally:
        print("Saving final model and stats...")
        TrainModel.save_model("models/model_final.npz")
        
        plot_save.save_stats_to_csv(game_count,number_of_moves,score_per_round, total_reward_per_round)
        print("Done. Safe to close.")



        


        


        

        




        

        
    
        
        

    

if __name__=="__main__":
    main()