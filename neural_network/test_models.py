import numpy as np
import matplotlib.pyplot as plt
from .agent import Worker as WorkerAgent
from .ai import model as MlModel
from snake_game import SnakeGame
from snake_game import settings
import os


def adapt_input_to_model(input_data, expected_size):

    current_size = input_data.shape[1] if input_data.ndim > 1 else len(input_data)
    
    if current_size == expected_size:
        return input_data
    elif current_size < expected_size:

        if input_data.ndim == 1:
            return np.pad(input_data, (0, expected_size - current_size), mode='constant')
        else:
            padding = ((0, 0), (0, expected_size - current_size))
            return np.pad(input_data, padding, mode='constant')
    else:

        if input_data.ndim == 1:
            return input_data[:expected_size]
        else:
            return input_data[:, :expected_size]


def test_models(model_numbers, num_games=1000, render=False, delay_ms=500):

    game = SnakeGame(Render=render, delay_ms=delay_ms)
    Game_settings = (settings.SCREEN_WIDTH, settings.CELL_PIXEL, settings.SCREEN_HEIGHT)
    Worker = WorkerAgent(*Game_settings)
    

    results = {}
    
    print(f"\n{'='*70}")
    print(f"Testing Models: {model_numbers}")
    print(f"Games per model: {num_games}")
    print(f"{'='*70}\n")
    
    for model_num in model_numbers:

        if model_num == 'F':
            model_path = "models/model_final.npz"
            display_name = "FINAL"
        else:
            model_path = f"models/model_best_{model_num}.npz"
            display_name = str(model_num)
        

        if not os.path.exists(model_path):
            print(f"Model not found: {model_path}")
            continue
        
        print(f"\nTesting Model: {display_name}")
        print(f" Loading from: {model_path}")
        

        model_data = np.load(model_path)
        input_size = model_data['W1'].shape[0]
        hidden1_size = model_data['W1'].shape[1]
        hidden2_size = model_data['W2'].shape[1]
        
        print(f" Model Architecture: {input_size} -> {hidden1_size} -> {hidden2_size} -> 3")
        

        AI = MlModel(input_size=input_size, hidden1=hidden1_size, hidden2=hidden2_size, output_size=3)
        AI.load_model(model_path)

        scores = []
        moves_list = []
        rewards_list = []
        

        for game_idx in range(num_games):
            game.Reset()
            game_reward = 0
            game_moves = 0
            game_score = 0
            
            while True:
     
                Food_cord = (game.Food_x, game.Food_y)
                snake_cordinates = game.snake_cordinates
                head_direction = game.head_direction
                
             
                input_data = Worker.Run(Food_cord, snake_cordinates, head_direction)
       
                input_data = adapt_input_to_model(input_data, input_size)
                output = AI.forward_propagation(input_data)
                action_idx = np.argmax(output)
                
        
                state_action = [0, 0, 0]
                state_action[action_idx] = 1
                
         
                Food_cord_next, snake_cordinates_next, head_direction_next, game_over, score, reward = game.run_game(state_action)
                
                game_reward += reward
                game_moves += 1
                game_score = score
                
                if game_over:
                    break
            
            scores.append(game_score)
            moves_list.append(game_moves)
            rewards_list.append(game_reward)
            

            if (game_idx + 1) % 200 == 0:
                avg_score = np.mean(scores[-200:])
                avg_moves = np.mean(moves_list[-200:])
                avg_reward = np.mean(rewards_list[-200:])
                max_score = np.max(scores[-200:])
                
                print(f"   Games: {game_idx + 1}/{num_games} | "
                      f"Avg Score: {avg_score:.1f} | "
                      f"Max Score: {max_score:.0f} | "
                      f"Avg Moves: {avg_moves:.1f} | "
                      f"Avg Reward: {avg_reward:.2f}")
        
        # Store results
        results[model_num] = {
            'scores': scores,
            'moves': moves_list,
            'rewards': rewards_list,
            'avg_score': np.mean(scores),
            'max_score': np.max(scores),
            'avg_moves': np.mean(moves_list),
            'avg_reward': np.mean(rewards_list),
            'std_score': np.std(scores)
        }
        
        # Final summary
        print(f"      Summary for Model {display_name}:")
        print(f"      Average Score: {results[model_num]['avg_score']:.2f} ± {results[model_num]['std_score']:.2f}")
        print(f"      Max Score: {results[model_num]['max_score']:.0f}")
        print(f"      Average Moves: {results[model_num]['avg_moves']:.2f}")
        print(f"      Average Reward: {results[model_num]['avg_reward']:.2f}")
    

    if len(results) > 0:
        _plot_results(results, model_numbers)
    
    return results


def _plot_results(results, model_numbers):
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Model Testing Results', fontsize=16, fontweight='bold')
    

    colors = plt.cm.tab10(np.linspace(0, 1, len(model_numbers)))
    
    # (Box Plot)
    ax = axes[0, 0]
    scores_data = [results[m]['scores'] for m in model_numbers]
    bp = ax.boxplot(scores_data, labels=[f"Model {m}" for m in model_numbers], patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    ax.set_ylabel('Score')
    ax.set_title('Score Distribution')
    ax.grid(True, alpha=0.3)
    
    # (Bar Plot)
    ax = axes[0, 1]
    x_pos = np.arange(len(model_numbers))
    width = 0.25
    
    avg_scores = [results[m]['avg_score'] for m in model_numbers]
    avg_moves = [results[m]['avg_moves'] for m in model_numbers]
    avg_rewards = [results[m]['avg_reward'] for m in model_numbers]
    
    ax.bar(x_pos - width, avg_scores, width, label='Avg Score', alpha=0.8)
    ax.bar(x_pos, avg_moves, width, label='Avg Moves', alpha=0.8)
    ax.bar(x_pos + width, avg_rewards, width, label='Avg Reward', alpha=0.8)
    
    ax.set_ylabel('Value')
    ax.set_title('Average Metrics Comparison')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"Model {m}" for m in model_numbers])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    ax = axes[1, 0]
    for model_num, color in zip(model_numbers, colors):

        scores = np.array(results[model_num]['scores'])
        window = min(50, len(scores) // 10)
        if window > 1:
            smoothed = np.convolve(scores, np.ones(window)/window, mode='valid')
            ax.plot(smoothed, label=f"Model {model_num}", linewidth=2, color=color)
        else:
            ax.plot(scores, label=f"Model {model_num}", linewidth=2, color=color)
    
    ax.set_xlabel('Game Number')
    ax.set_ylabel('Score')
    ax.set_title('Score Progression (Smoothed)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    

    ax = axes[1, 1]
    max_scores = [results[m]['max_score'] for m in model_numbers]
    bars = ax.barh([f"Model {m}" for m in model_numbers], max_scores, color=colors)
    

    for i, (bar, val) in enumerate(zip(bars, max_scores)):
        ax.text(val + 0.5, i, f"{val:.0f}", va='center', fontweight='bold')
    
    ax.set_xlabel('Max Score Achieved')
    ax.set_title('Best Performance Per Model')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('test_results.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("Snake Game Model Testing")
    

    try:
        models_input = input("Enter model numbers to test ").strip()
        model_numbers = [int(m.strip()) for m in models_input.split(',')]
    except:
        print("Using default models: [1, 2, 3]")
        model_numbers = [1, 2, 3]
    
    try:
        num_games_input = input("Enter number of test games (default 1000): ").strip()
        num_games = int(num_games_input) if num_games_input else 1000
    except:
        num_games = 1000
    

    results = test_models(model_numbers, num_games=num_games, render=False)
    

    for model_num in model_numbers:
        if model_num in results:
            r = results[model_num]
            display_name = "FINAL" if model_num == 'F' else f"Model {model_num}"
            print(f"\n{display_name}:")
            print(f"  Average Score:  {r['avg_score']:.2f} ± {r['std_score']:.2f}")
            print(f"  Max Score:      {r['max_score']:.0f}")
            print(f"  Average Moves:  {r['avg_moves']:.2f}")
            print(f"  Average Reward: {r['avg_reward']:.2f}")
