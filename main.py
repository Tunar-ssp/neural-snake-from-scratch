from snake_game import Game
from neural_network import MlModel

from snake_game import settings

Game_settings = (settings.SCREEN_WIDTH,settings.CELL_PIXEL,settings.SCREEN_HEIGHT)




def main():
    game=Game()
    TrainModel=MlModel(*Game_settings)
    
    while True:
        
        Food_cord,snake_cordinates,head_direction,game_over,score=game.run_game(state)
        
      


        if game_over:
            continue
        state=TrainModel.Run(Food_cord,snake_cordinates,head_direction,score)
        

    

if __name__=="__main__":
    main()