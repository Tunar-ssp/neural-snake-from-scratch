import numpy as np
import os
from neural_network import test_models


def get_available_models():


    models_dir = "models"
    available_models = []
    
    if os.path.exists(models_dir):
        for filename in sorted(os.listdir(models_dir)):
            if filename.startswith("model_best_") and filename.endswith(".npz"):
                try:
                    model_num = int(filename.replace("model_best_", "").replace(".npz", ""))
                    available_models.append(model_num)
                except ValueError:
                    pass
    
    return sorted(available_models)


def display_models(available_models):

    print("AVAILABLE MODELS")

    
    models_dir = "models"
    has_final = os.path.exists(os.path.join(models_dir, "model_final.npz"))
    
    if not available_models and not has_final:
        print("No models found in 'models/' directory")
        return False
    

    if available_models:
        print("  Best Models:")
        for i in range(0, len(available_models), 10):
            models_chunk = available_models[i:i+10]
            print("  " + "  ".join(f"[{m:2d}]" for m in models_chunk))

    if has_final:
        print("  Final Model:")
        print("  [F] - model_final")
    
    print("="*70 + "\n")
    return True


def select_models():

    available_models = get_available_models()
    
    if not display_models(available_models):
        return None
    
    models_dir = "models"
    has_final = os.path.exists(os.path.join(models_dir, "model_final.npz"))
    
    while True:
        models_input = input("Select models (ex: 44,48,49,F): ").strip()
        
        if not models_input:
            print(" Please enter at least one model number or F for final")
            continue
        
        try:
            selected_models = []
            for item in models_input.split(','):
                item = item.strip().upper()
                
                if item == 'F':
                    if has_final:
                        selected_models.append('F')
                    else:
                        print(f"'final' not found")
                        break
                else:
                    try:
                        model_num = int(item)
                        if model_num not in available_models:
                            print(f" Model {model_num} not found")
                            print(f"   Available models: {available_models}")
                            break
                        selected_models.append(model_num)
                    except ValueError:
                        print(f"Invalid : {item}")
                        break
            else:

                return selected_models
        
        except Exception as e:
            print(f"errorr :{e}")


def main():

    model_numbers = select_models()
    if model_numbers is None:
        print("No models selected. Exiting.")
        return
    
    print(f"Selected models: {model_numbers}\n")
    

    while True:
        try:
            num_games_input = input("Enter number of test games (default 1000 ,  Enter to skip): ").strip()
            num_games = int(num_games_input) if num_games_input else 1000
            
            if num_games < 1:
                print("must be at least 1")
                continue
            
            break
        except ValueError:
            print("Please enter a number")
    while True:
        render_input = input("enable rendering? (y/n, default n): ").strip().lower()
        if render_input in ['y', 'yes']:
            render = True
            break
        elif render_input in ['n', 'no', '']:
            render = False
            break
        else:
            print("please enter 'y' or 'n'.")
    
    #default
    delay_ms = 75

    if render:
        while True:
            try:
                delay_input = input("Milliseconds between each move (default 75ms): ").strip()
                delay_ms = int(delay_input) if delay_input else 500
                
                if delay_ms < 10:
                    print("must be at least 10ms")
                    continue
                
                break
            except ValueError:
                print("Please enter a number")
    
    print()
    
    results = test_models(model_numbers, num_games=num_games, render=render, delay_ms=delay_ms)


if __name__ == "__main__":
    main()








