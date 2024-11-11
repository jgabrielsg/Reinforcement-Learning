import numpy as np
import random

class QLearning:
    def __init__(self, actions, state_space_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.99):
        self.actions = actions  # Lista de ações possíveis
        self.q_table = np.zeros((state_space_size, len(actions)))  # Tabela Q inicializada com zeros
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def choose_action(self, state):
        # Epsilon-greedy para escolher a ação: explorar ou explorar
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(range(len(self.actions)))  # Escolher uma ação aleatória
        else:
            return np.argmax(self.q_table[state])  # Escolher a ação com o maior valor Q

    def update_q_value(self, state, action, reward, next_state):
        # Atualização da tabela Q
        best_future_q = np.max(self.q_table[next_state])
        current_q = self.q_table[state, action]
        # Fórmula Q-Learning
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * best_future_q - current_q)
        self.q_table[state, action] = new_q

        # Decaimento da taxa de exploração
        self.exploration_rate *= self.exploration_decay
