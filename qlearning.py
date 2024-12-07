import numpy as np
import csv
import random

class QLearning:
    def __init__(self, actions, state_space_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.99):
        self.actions = actions  # List of possible actions
        
        # I changed to it starts with 5 so we encourage the coder to explore more at the start
        self.q_table = np.full((state_space_size, len(actions)), 5) # Q-table initialized with fives
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def choose_action(self, state):
        # Epsilon-greedy to choose action: explore or exploit
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(range(len(self.actions)))  # Choose a random action
        else:
            return np.argmax(self.q_table[state])  # Choose the action with the highest Q value

    def update_q_value(self, state, action, reward, next_state):
        # Update the Q-table
        best_future_q = np.max(self.q_table[next_state])
        current_q = self.q_table[state, action]
        # Q-learning formula
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * best_future_q - current_q)
        self.q_table[state, action] = new_q

        # Exploration rate decay
        self.exploration_rate *= self.exploration_decay

    def save_q_table(self, iteration, is_reviewer=False):
        # Usa um nome diferente para o arquivo dependendo de quem está salvando
        file_name = "reviewer_q_tables.csv" if is_reviewer else "coder_q_tables.csv"
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)

            if iteration == 0:  # No primeiro, escreve o cabeçalho
                header = ['Iteration'] + [f'Action {i+1}' for i in range(self.q_table.shape[1])]
                writer.writerow(header)

            for row in self.q_table:
                writer.writerow([iteration] + list(row))