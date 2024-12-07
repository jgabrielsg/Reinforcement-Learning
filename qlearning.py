import numpy as np
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
