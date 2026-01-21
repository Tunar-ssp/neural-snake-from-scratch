import random
from collections import deque
import numpy as np
from snake_game import SnakeGame
from neural_network import WorkerAgent, MlModel
from snake_game import settings
import plot_save

def main():
    game = SnakeGame(Render=False)
    plotter = plot_save.LivePlotter()
    
    Game_settings = (settings.SCREEN_WIDTH, settings.CELL_PIXEL, settings.SCREEN_HEIGHT)
    CreateData = WorkerAgent(*Game_settings)
    TrainModel = MlModel(input_size=35, hidden1=256, hidden2=128, output_size=3)
    
    learning_rate = 0.001  
    gamma = 0.9            
    epsilon = 1.0
    epsilon_min = 0.1    
    epsilon_decay = 0.995

    memory = deque(maxlen=100000) 
    BATCH_SIZE = 128
    moves = 0
    max_score = 0
    game_count = 0
    
    number_of_moves = []
    score_per_round = []
    total_reward_per_round = []
    total_reward_per_round_temp = []
    loss_per_game_temp = [] 
    avg_loss_history = []
    epsilon_history = []
    q_values_per_episode = []
    q_values_current_episode = []

    try:
        while True:
        
            Food_cord = (game.Food_x, game.Food_y)
            snake_cordinates = game.snake_cordinates
            head_direction = game.head_direction
            
            state_old = CreateData.Run(Food_cord, snake_cordinates, head_direction)
            
            prediction_current = TrainModel.forward_propagation(state_old)
            
            if random.random() <= epsilon:
                action_idx = random.randint(0, 2)  
            else:
                action_idx = np.argmax(prediction_current)
            
            state_action = [0, 0, 0]
            state_action[action_idx] = 1
            
            
            
            Food_cord_next, snake_cordinates_next, head_direction_next, game_over, score, reward = game.run_game(state_action)
            
        

            state_new = CreateData.Run(Food_cord_next, snake_cordinates_next, head_direction_next)
 
 
            memory.append((state_old, action_idx, reward, state_new, game_over))
      
    
            
            
            if len(memory) > BATCH_SIZE and (game_over or moves % 15 == 0):
                batch_loss = []
                for _ in range(10):  
                    mini_batch = random.sample(memory, BATCH_SIZE)
                    states = np.array([m[0] for m in mini_batch]).reshape(BATCH_SIZE, -1)
                    next_states = np.array([m[3] for m in mini_batch]).reshape(BATCH_SIZE, -1)
                    actions = np.array([m[1] for m in mini_batch])
                    rewards = np.array([m[2] for m in mini_batch])
                    dones = np.array([m[4] for m in mini_batch])
                    # Get predictions for next states to calculate targets
                    next_preds = TrainModel.forward_propagation(next_states)
           
                    # Fully Vectorized Bellman Equation
                    max_next_q = np.max(next_preds, axis=1)
                    target_q_values = rewards + (gamma * max_next_q * (1 - dones))

                    # NOW get predictions for current states and store activations for backprop
                    preds = TrainModel.forward_propagation(states)
                    targets = preds.copy()
            

                    targets[np.arange(BATCH_SIZE), actions] = target_q_values

                    # Compute gradient and backprop
                    loss_grad = preds - targets
                    loss_grad = np.clip(loss_grad, -1.0, 1.0)
              
                    TrainModel.gradient_descent(loss_grad)
                    TrainModel.backward_propagation(learning_rate)
          
                    batch_loss.append(np.mean(np.square(loss_grad)))

                loss_per_game_temp.append(np.mean(batch_loss))


            total_reward_per_round_temp.append(reward)
            q_values_current_episode.append(np.mean(prediction_current))
            moves += 1

            if game_over:
                if score > max_score:
                    max_score = score
                    TrainModel.save_model(f"models/model_best_{max_score}.npz")

                score_per_round.append(score)
                total_reward_per_round.append(sum(total_reward_per_round_temp))
                number_of_moves.append(moves)
                
                if len(loss_per_game_temp) > 0:
                    avg_loss_history.append(np.mean(loss_per_game_temp))
                else:
                    avg_loss_history.append(0)
                    
                epsilon_history.append(epsilon)
                
                if len(q_values_current_episode) > 0:
                    avg_q_val = np.mean(q_values_current_episode)
                    q_values_per_episode.append(avg_q_val)
                else:
                    q_values_per_episode.append(0)
                if game_count % 50 == 0:

                    plotter.update(score_per_round, number_of_moves, avg_loss_history, 
                                epsilon_history, total_reward_per_round, q_values_per_episode)

     
                total_reward_per_round_temp = []
                loss_per_game_temp = []
                q_values_current_episode = []
                moves = 0
                game_count += 1
                
                if epsilon > epsilon_min:
                    epsilon *= epsilon_decay
                print("------------------")
                print(f"Game: {game_count}, Score: {score}, Max Score: {max_score}, Epsilon: {epsilon:.4f}")

    except KeyboardInterrupt:
        print('-----------Training Stopped by Keyboard Interrupt -----------')
    finally:
        print("Saving final model and stats...")
        TrainModel.save_model("models/model_final.npz")
        plot_save.save_stats_to_csv(game_count, number_of_moves, score_per_round, total_reward_per_round)
        print("Done. Safe to close.")

if __name__ == "__main__":
    main()