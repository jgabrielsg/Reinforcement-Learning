from agentes import Coder, Reviewer, MonitoringAndFeedbackAgent
from ambiente import Environment
from qlearning import QLearning
import random

def main():
    # Define a comprehensive problem description for testing
    problem_description = """
        We have a Sales.csv with 4 columns: Date, with the date (format 2024-09-25) of the sale;
        Price, how much money (format 20.99USD) the client paid for the sale;
        Store, in which store was made that sale, the IDs go from 1 to 5
        State, the state the sale was made. We work in 2 states, Paraná and Acre
        There's some data missing, with null values and outliers. Find the outliers (like a sale costing more than 
        100000USD) and the missing data and get rid of them. After that, your job is to create 2 visualizations: 
        - Sales per state
        - Sales per month of the year.
    """

    max_iterations = 100

    try:
        # Instantiate the agents and environment
        coder = Coder(problem_description=problem_description)
        reviewer = Reviewer(problem_description=problem_description)
        environment = Environment(threshold_score=100, max_iterations=max_iterations)
        monitor = MonitoringAndFeedbackAgent()
    except Exception as e:
        print(f"Error initializing agents or environment: {e}")
        return


    coder_prompts = [   
        """You are an experienced Python coder tasked with solving a data science problem efficiently. Your objective is to (with the file Sales.csv):
            1. Handle any missing or inconsistent data by applying appropriate imputation or removal methods.
            2. Ensure that any outliers (e.g., sales exceeding 100000USD) are properly identified and dealt with.
            3. Create two visualizations using libraries like `matplotlib` or `seaborn`: 
                - Sales per state.
                - Sales per month.
            4. Write clean and well-documented code. Use comments and docstrings to explain your approach and logic.
        Focus on writing robust, maintainable code that fulfills the problem description with clarity and efficiency. Ensure that edge cases, such as missing values and outliers, are handled properly, and the visualizations are meaningful and accurate.""",

        "You are a skilled Python developer and data scientist. Your primary task is to write Python code that effectively addresses "
        "data science problems based on a given problem description. Follow these guidelines carefully:\n\n"
            "1. Precision: Generate code that directly addresses the problem requirements without unnecessary elements.\n"
            "2. Documentation: Include concise comments in the code to explain key steps, so it's easy to understand and maintain.\n"
            "3. Error Handling: Anticipate common issues (e.g., missing data, incorrect formats) and handle them gracefully within the code.\n"
            "4. Efficiency: Use efficient methods, libraries, or algorithms wherever possible to optimize performance.\n\n"
        "Your code should be clean, well-organized, and focus on the task requirements provided in the problem description.",
        
        """You are a Python developer. You will make some code, that code needs to be:
        1. Remember all the basics, and give the code already finished.
        2. Handle unexpected input gracefully, always expect for the worse.
        3. Return results in the expected format.""",
        
        """You are a minimalist coder. Your mission is to write the shortest and simplest Python 
        script that accomplishes the given task without sacrificing clarity or functionality.""",

    ]
    
    reviewer_prompts = [    
        """You are a highly experienced Python code reviewer with a focus on data science tasks. Your role is to review the code generated by the Coder and provide clear, constructive feedback. Your review should cover:
            1. **Error Handling**: Evaluate how the code handles potential issues like missing data, invalid formats, or outliers. Ensure it is robust and fails gracefully.
            2. **Code Efficiency**: Suggest any improvements for optimizing performance, such as better handling of large datasets or faster methods for data cleaning and visualization.
            3. **Clarity and Readability**: Assess the code for clarity, modularity, and readability. Recommend improvements to naming conventions, structure, or documentation.
            4. **Best Practices**: Ensure that the code adheres to Python best practices, including proper use of libraries, concise code, and appropriate error handling.
        Avoid suggesting any new code. Your feedback should focus on the existing code and how it can be improved, highlighting areas that might not meet the problem’s requirements or where performance could be enhanced.""",

        "You are a Senior Python developer and data scientist with expertise in reviewing code for quality, efficiency, and best practices. "
        "Your primary role is to review code generated by other developers and provide detailed feedback on how to improve it. Follow these instructions carefully:\n\n"
            "1. Identify Errors: Analyze the code for errors or bugs, especially those that might arise from the code’s current logic, and explain how to handle them effectively.\n"
            "2. Suggest Optimizations: Look for ways to improve the code’s efficiency. This includes suggesting alternative methods, removing redundancies, and identifying potential performance bottlenecks.\n"
            "3. Enhance Readability: Recommend adjustments that improve code readability and maintainability, such as restructuring code blocks, adding comments, or following consistent naming conventions.\n"
            "4. Focus on Best Practices: Suggest ways to follow Python best practices, such as appropriate error handling, modular design, and clarity in code structure.\n\n"
        "Do not include any new code in your response, don't send ANY CODE in general, NOTHING. Focus only on providing constructive feedback based on the code’s" 
        "current state and the potential errors it could generate, as well as clear, actionable recommendations for improvement."
        ,

        """Your task is to review the provided Python code with the primary goal of verifying whether it fulfills the given problem’s requirements.

            1. Highlight any missing features, incomplete logic, or deviations from the problem requirements.
            2. Confirm whether it produces the expected results in all scenarios, including edge cases.
            3. Critize the Coder harshly, showing all his mistakes as if he's inferior to you.
        Your feedback should focus on aligning the code’s functionality with the problem’s goals, identifying oversights, and suggesting corrections or enhancements to improve alignment.""",
        
        """You are a minimalist reviewer. Your mission is to review the following code in the shortest and simplest way 
        that accomplishes the given task without sacrificing clarity or functionality.""",

    ]
    
    # Define actions and Q-Learning parameters
    coder_actions = coder_prompts
    reviewer_actions = reviewer_prompts
    
    # Initialize Q-Learning for both agents
    state_space_size = 4 # bad, average and good previous code
    c_qlearning = QLearning(coder_actions, state_space_size)
    r_qlearning = QLearning(reviewer_actions, state_space_size)

    save_iterations = [1, 2, 3] + list(range(10, 101, 10)) # Para salvar as iterações

    feedback = "" # Initially is an empty string
    generated_code = "" # Initially is an empty string

    last_reviewer_index = -1 # We just reward the reviewer one iteration later
    previous_score = 0
    state = 0  # Initial state
    for iteration in range(max_iterations):
        print(f"\n=== Iteration {iteration + 1} ===")

        # Step 1: Coder selects an action using Q-learning and generates code
        coder_action_index = c_qlearning.choose_action(state)
        coder_action = coder_actions[coder_action_index]
        
        print(f"Coder's action: {coder_action}")
        print(f"\n=== Coder is working... ===")
        
        generated_code = coder.generate_code(coder_action, feedback, generated_code) # Gets the last code as well

        # Step 2: Reviewer selects an action using Q-learning and reviews the code
        reviewer_action_index = r_qlearning.choose_action(state)
        reviewer_action = reviewer_actions[reviewer_action_index]
        
        print("Generated code by Coder:\n", generated_code, "\n")
        
        print(f"Reviewer's action: {reviewer_action}")
        print(f"\n=== Reviewer is working... ===")

        feedback, score = reviewer.review_code(generated_code, reviewer_action)

        # Monitor performance during coder's action
        monitor.provide_feedback(generated_code, score)  # Monitor the coder's performance

        # Monitor performance during coder's action
        monitor.monitor_execution_time(generated_code)  # Monitor the coder's performance
        memory_usage, cpu_usage = monitor.monitor_resource_usage()  # Monitor resource usage

        # Imprimir tempo de execução, uso de memória e CPU
        print(f"Execution Time: {monitor.end_time - monitor.start_time:.2f} seconds")
        print(f"Memory Usage: {memory_usage:.2f} MB")
        print(f"CPU Usage: {cpu_usage:.2f}%")

        # Monitor performance during reviewer's action
        monitor.provide_feedback(feedback, score)  # Monitor the reviewer's performance
        
        print("Reviewer's feedback:\n", feedback)
        print("Score assigned by Reviewer:", score, "\n")

        # Step 3: Calculate rewards
        coder_reward = environment.reward_coder(generated_code, score, iteration)
        if last_reviewer_index != -1:
            reviewer_reward = environment.reward_reviewer(previous_score, score)
        previous_score = score  # Update the previous score for the next iteration
        
        print("Coder's reward:", coder_reward)
        if last_reviewer_index != -1:
            print("Reviewer's reward:", reviewer_reward, "\n")
        
        # Changing the state
        if score == -1: # If the code is not even working
            next_state = 0
        elif score < 50: # Bad code
            next_state = 1
        elif 50 <= score <= 90: # Average code
            next_state = 2
        else:
            next_state = 3 # Good code
            
        c_qlearning.update_q_value(state, coder_action_index, coder_reward, next_state)
        if last_reviewer_index != -1:
            r_qlearning.update_q_value(state, last_reviewer_index, reviewer_reward, next_state) # We just reward the reviewer one iteration later
        
        print("\n=== Q-values for Coder ===")
        print(c_qlearning.q_table)
        
        print("\n=== Q-values for Reviewer ===")
        print(r_qlearning.q_table)
        
        # next state
        state = next_state
        last_reviewer_index = reviewer_action_index

        if iteration + 1 in save_iterations:
            iteration_output = f"Iteration {iteration + 1}\n"
            iteration_output += f"Coder's action: {coder_action}\n"
            iteration_output += f"Generated code by Coder:\n{generated_code}\n"
            iteration_output += f"Reviewer's action: {reviewer_action}\n"
            iteration_output += f"Reviewer's feedback:\n{feedback}\n"
            iteration_output += f"Score assigned by Reviewer: {score}\n"

            # Save to a text file
            file_name = f"iterations/iteration_{iteration + 1}.txt"
            with open(file_name, 'w') as file:
                file.write(iteration_output)

    print("\n=== Iterative agent flow test completed ===")

if __name__ == "__main__":
    main()
