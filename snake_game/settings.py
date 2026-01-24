
CELL_PIXEL=120
max_x=15
max_y=15

SCREEN_WIDTH=CELL_PIXEL*max_x
SCREEN_HEIGHT=CELL_PIXEL *max_y



FPS=60
MOVE_INTERVAL=400#ms
BG_COLOR=(255,0,0)
REWARDS = {
    'game_over': -10,      # snake hits wall or itself
    'food_eaten': 20,      # snake eats food
    'trapped': -5,         # all 4 directions are blocked
    'closer_to_food': 0.1, # moving closer to food
    'away_from_food': -0.2 # moving away from food
}