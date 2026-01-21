from snake_game import SnakeGame
from neural_network import MlModel

from snake_game import settings

Game_settings = (settings.SCREEN_WIDTH,settings.CELL_PIXEL,settings.SCREEN_HEIGHT)




def main():
    game=SnakeGame()
    # TrainModel=MlModel(*Game_settings)
    for state in ([1,0,0],[0,0,1],[0,1,0],[1,0,0],[1,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]):
        print(1)
        print(state)
        Food__cord,snake_cordinates,head_direction,game_over,score,reward=game.run_game(state)
        print(
        f"Food__cord      = {Food__cord}\n"
        f"Snake_cordinates= {snake_cordinates}\n"
        f"Head_direction  = {head_direction}\n"
        f"Game_over       = {game_over}\n"
        f"Score           = {score}\n"
        f"Reward          = {reward}"
        )
        
        game.render()
        

    

if __name__=="__main__":
    main()