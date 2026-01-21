import matplotlib.pyplot as plt
import numpy as np
import csv


plt.ion() 

class LivePlotter:
    def __init__(self):
        self.fig, self.axs = plt.subplots(2, 3, figsize=(18, 10))
        self.axs = self.axs.flatten()
        
        self.line_score, = self.axs[0].plot([], [], label='Score', color='blue')
        self.line_moves, = self.axs[1].plot([], [], color='green')
        self.line_loss, = self.axs[2].plot([], [], color='red')
        self.line_epsilon, = self.axs[3].plot([], [], color='orange')
        self.line_total_reward, = self.axs[4].plot([], [], color='purple')
        self.line_q_values, = self.axs[5].plot([], [], color='brown')
        
        self.axs[0].set_title("Score per Game")
        self.axs[1].set_title("Moves per Game")
        self.axs[2].set_title("Learning Loss")
        self.axs[3].set_title("Epsilon (Exploration Rate)")
        self.axs[4].set_title("Total Reward per Episode")
        self.axs[5].set_title("Average Q-Values")
        
        for ax in self.axs:
            ax.set_xlabel("Episode")

    def update(self, scores, moves, losses, epsilon_values, total_rewards, q_values):
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
        
        if len(epsilon_values) > 0:
            self.line_epsilon.set_data(range(len(epsilon_values)), epsilon_values)
            self.axs[3].relim()
            self.axs[3].autoscale_view()
        
        if len(total_rewards) > 0:
            self.line_total_reward.set_data(range(len(total_rewards)), total_rewards)
            self.axs[4].relim()
            self.axs[4].autoscale_view()
        
        if len(q_values) > 0:
            self.line_q_values.set_data(range(len(q_values)), q_values)
            self.axs[5].relim()
            self.axs[5].autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def save_stats_to_csv(game_count, number_of_moves, score_per_round, total_reward_per_round):
    rows = zip(range(1, game_count + 1), number_of_moves, score_per_round, total_reward_per_round)
    with open('stats.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['game', 'moves', 'score', 'total_reward'])
        writer.writerows(rows)