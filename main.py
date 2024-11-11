"""
Neste módulo implemente o fluxo básico do treinamento por RL dos agentes.
"""

from agentes import Coder, Reviewer
from ambiente import Environment
from qlearning import QLearning
import random

def main():
    # Define a comprehensive problem description for testing
    problem_description = """
    You have a Sales.csv with 4 columns: Date, with the date (format 2024-09-25) of the sale;
    Price, how much money (format 20.99USD) the client paid for the sale;
    Store, in which store was made that sale, the IDs go from 1 to 5
    State, the state the sale was made. We work in 2 states, Paraná and Acre
    There's some data missing, with null values and outliers. Find the outliers (like a sale costing more than 
    100000USD) and the missing data and get rid of them. After that, create 2 visualizations: Sales per state
    and Sales per month of the year.
    """

    try:
        # Instantiate the agents and environment
        coder = Coder(problem_description=problem_description)
        reviewer = Reviewer(problem_description=problem_description)
        environment = Environment(threshold_score=100)
    except Exception as e:
        print(f"Error initializing agents or environment: {e}")
        return

    # Define actions and Q-Learning parameters
    coder_actions = ['improve_readability', 'optimize_efficiency', 'handle_errors']
    reviewer_actions = ['suggest_refactoring', 'identify_bugs', 'recommend_comments']
    
    # Define a simple state space size (arbitrary for simplicity)
    state_space_size = 10
    
    # Initialize Q-Learning for both agents
    coder_qlearning = QLearning(coder_actions, state_space_size)
    reviewer_qlearning = QLearning(reviewer_actions, state_space_size)
    
    feedback = "" # Initially is an empty string
    generated_code = "" # Initially is an empty string

    # Start the iterative process
    previous_score = 0
    state = 0  # Initial state (simplified)
    for iteration in range(5):
        print(f"\n=== Iteration {iteration + 1} ===")

        # Step 1: Coder selects an action using Q-learning and generates code
        coder_action_index = coder_qlearning.choose_action(state)
        coder_action = coder_actions[coder_action_index]
        
        print(f"Coder's action: {coder_action}")
        print(f"\n=== Coder is working... ===")
        
        coder_action_prompt = generate_coder_prompt(coder_action)
        generated_code = coder.generate_code(coder_action_prompt, feedback, generated_code) # Gets the last code as well
        
        print("Generated code by Coder:\n", generated_code, "\n")

        # Step 2: Reviewer selects an action using Q-learning and reviews the code
        reviewer_action_index = reviewer_qlearning.choose_action(state)
        reviewer_action = reviewer_actions[reviewer_action_index]
        
        print(f"Reviewer's action: {reviewer_action}")
        print(f"\n=== Reviewer is working... ===")
        
        reviewer_action_prompt = generate_reviewer_prompt(reviewer_action)
        feedback, score = reviewer.review_code(generated_code, reviewer_action_prompt)
        
        print("Reviewer's feedback:\n", feedback)
        print("Score assigned by Reviewer:", score, "\n")

        # Step 3: Calculate rewards
        coder_reward = environment.reward_coder(generated_code, score)
        reviewer_reward = environment.reward_reviewer(previous_score, score)
        previous_score = score  # Update the previous score for the next iteration
        
        # Print rewards
        print("Coder's reward:", coder_reward)
        print("Reviewer's reward:", reviewer_reward, "\n")
        
        # Update Q-values for Coder and Reviewer
        next_state = random.randint(0, state_space_size - 1)  # For simplicity, using random state transition
        coder_qlearning.update_q_value(state, coder_action_index, coder_reward, next_state)
        reviewer_qlearning.update_q_value(state, reviewer_action_index, reviewer_reward, next_state)
        
        # Move to the next state
        state = next_state

    print("\n=== Iterative agent flow test completed ===")

def generate_coder_prompt(action):
    """Generates a prompt for the Coder based on the chosen action."""
    if action == "improve_readability":
        return f"Focus on making the code readable and adding comments where necessary. "
    elif action == "optimize_efficiency":
        return f"Focus on optimizing the code for performance. "
    elif action == "handle_errors":
        return f"Focus on adding error handling to make the code more robust. "
    return ". "

def generate_reviewer_prompt(action):
    """Generates a prompt for the Reviewer based on the chosen action."""
    if action == "suggest_refactoring":
        return f"Please review the following code with a focus on suggesting refactoring improvements. "
    elif action == "identify_bugs":
        return f"Please review the following code with a focus on identifying and explaining any bugs. "
    elif action == "recommend_comments":
        return f"Please review the following code with a focus on recommending where comments could improve clarity. "
    return ". "

if __name__ == "__main__":
    main()