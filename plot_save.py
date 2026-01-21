import matplotlib.pyplot as plt
import numpy as np
import csv


plt.ion() 

class LivePlotter:
    def __init__(self):
        self.fig, self.axs = plt.subplots(1, 3, figsize=(15, 5))
        self.line_score, = self.axs[0].plot([], [], label='Score')
        self.line_moves, = self.axs[1].plot([], [], color='green')
        self.line_loss, = self.axs[2].plot([], [], color='red')
        
        self.axs[0].set_title("Score per Game")
        self.axs[1].set_title("Moves")
        self.axs[2].set_title("Learning Loss")

    def update(self, scores, moves, losses):
        self.line_score.set_data(range(len(scores)), scores)
        self.axs[0].relim()
        self.axs[0].autoscale_view()

        self.line_moves.set_data(range(len(moves)), moves)
        self.axs[1].relim()
        self.axs[1].autoscale_view()

        if len(losses) > 0:
            self.line_loss.set_data(range(len(losses)), losses)
            self.axs[2].relim()
            self.axs[2].autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def save_stats_to_csv(game_count, number_of_moves, score_per_round, total_reward_per_round):
    rows = zip(range(1, game_count + 1), number_of_moves, score_per_round, total_reward_per_round)
    with open('stats.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['game', 'moves', 'score', 'total_reward'])
        writer.writerows(rows)