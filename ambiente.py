import ast
import subprocess
import sys

class Environment:
    def __init__(self, threshold_score=50, expected_output=None):
        self.threshold_score = threshold_score  # Minimum score to consider the code satisfactory
        self.expected_output = expected_output  # Expected output for code correctness check

    def calculate_reward(self, score, agent_type="coder"):
        """
        Calculates the reward for the coder or reviewer based on the score.
        :param score: Total score given by the Reviewer.
        :param agent_type: Type of agent ("coder" or "reviewer").
        :return: Reward (positive for high scores, negative for low scores).
        """
        try:
            if agent_type == "coder":
                if score >= self.threshold_score:
                    return 1.0  # Maximum reward for satisfactory code
                else:
                    return -1.0 + (score / self.threshold_score)  # Proportional penalty
        except Exception as e:
            print(f"Error calculating reward: {e}")
            return -1.0  # Default to maximum penalty on error

    def execute_code(self, code):
        """
        Executes the code to check for runtime errors.
        :param code: Code to be executed.
        :return: Tuple (success: bool, output: str).
        """
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=30 # kind of big, but it worked better with a big timer
            )
            if result.returncode == 0:
                return True, "Code executed successfully."
            else:
                return False, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Error: Code execution timed out."
        except Exception as e:
            print(f"Error during execution: {e}")
            return False, f"Error during execution: {e}"

    def check_correctness(self, code_output):
        """
        Compares the code's output with the expected output to determine correctness.
        :param code_output: The output produced by executing the code.
        :return: Boolean indicating if the output matches the expected result.
        """
        return code_output == self.expected_output

    def analyze_code_quality(self, code):
        """
        Analyzes code quality using a simple static analysis.
        :param code: Code to be analyzed.
        :return: A score representing code quality.
        """
        issues = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    issues.append(f"Function '{node.name}' found.")
                elif isinstance(node, ast.Assign):
                    issues.append("Global variable assignment found.")
            if not issues:
                return 10  # Perfect score for no issues
            return max(0, 10 - len(issues))  # Deduct points based on issues found
        except SyntaxError:
            return 0  # Lowest quality score if there's a syntax error

    def calculate_complexity(self, code):
        """
        Calculates the complexity of the code based on certain heuristics.
        :param code: Code to be analyzed.
        :return: Complexity score (lower is simpler).
        """
        try:
            lines_of_code = len(code.splitlines())
            tree = ast.parse(code)
            function_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            return lines_of_code + function_count * 2  # Basic complexity formula
        except Exception as e:
            print(f"Error calculating complexity: {e}")
            return float('inf')  # Infinite complexity on error

    def reward_coder(self, code, reviewer_score):
        """
        Rewards the coder based on code quality, correctness, and complexity.
        The score from the reviewer is used to adjust the reward for the coder.
        :param code: The code generated by the coder.
        :param reviewer_score: The score assigned by the reviewer.
        :return: Reward score for the coder.
        """
        # Execute and check correctness
        success, output = self.execute_code(code)
        correctness_reward = 1.0 if success and self.check_correctness(output) else -1.

        # Calculate complexity (penalize high complexity)
        complexity_score = self.calculate_complexity(code)
        complexity_penalty = -0.5 if complexity_score > 20 else 0.0

        # Use the reviewer's score to adjust the reward:
        if reviewer_score == -1:  # Error from the reviewer, not coder's fault!
            reviewer_penalty = 0
        elif reviewer_score < 25:  # Bad code, large penalty
            reviewer_penalty = -5.0
        elif 25 <= reviewer_score <= 40:  # Average code, smaller penalty
            reviewer_penalty = -3.0
        elif 40 <= reviewer_score <= 60:  # Average code, smaller penalty
            reviewer_penalty = -1.0
        elif 60 <= reviewer_score <= 80:  # Average code, smaller penalty
            reviewer_penalty = 1.0
        else:  # Good code, reward
            reviewer_penalty = 3.0

        # Combine all rewards/penalties
        return correctness_reward + complexity_penalty + reviewer_penalty


    def reward_reviewer(self, previous_score, current_score):
        """
        Rewards the reviewer based on improvements in the analytic report's score.
        :param previous_score: The score from the last review.
        :param current_score: The score from the current review.
        :return: Reward score for the reviewer.
        """
        if current_score == -1:
            return -2  # Reviewer didn't follow the rules
        
        improvement = current_score - previous_score
        
        if improvement > 8:
            return 1.0
        if improvement > 15:
            return 2.0
        if improvement > 30:
            return 3.0
        return -0.5  # Penalize if no improvement was made


