from snake_game import SnakeGame
from neural_network import MlModel

from snake_game import settings

Game_settings = (settings.SCREEN_WIDTH,settings.CELL_PIXEL,settings.SCREEN_HEIGHT)




def main():
    game=SnakeGame()
    # TrainModel=MlModel(*Game_settings)
    for state in ([1,0,0],[0,0,1],[0,1,0],[1,0,0],[1,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]):
        print(1)
        print(state)
        game.run_game(state)
        game.render()
        

    

if __name__=="__main__":
    main()