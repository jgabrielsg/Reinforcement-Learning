import ollama
import ast
import re
import ruff
import subprocess
import sys
import os
import pathlib

class LLMAgent:
    def __init__(self, model="llama3.2:1b"):
        self.model = model
        self.memory = []  # Memory for conversation history

    def generate(self, prompt):
        """Sends a prompt to the model and receives a response."""
        messages = [{'role': 'user', 'content': prompt}]
        try:
            response = ollama.chat(model=self.model, messages=messages + self.memory)
            
            #print(response) # debugging
            
            return response['message']['content']

        except Exception as e:
            print(f"Error calling ollama.chat: {e}")
            return "Error generating code: exception in model call."


class Coder(LLMAgent):
    def __init__(self, model="llama3.2:1b", problem_description=""):
        super().__init__(model)
        self.problem_description = problem_description

    def generate_code(self, action, review="", previous_code=""):
        """
        Generates code based on the problem description.
        :return: Generated code as a string.
        """
        if review == "":
            prompt = f"{action} Consider the following problem: {self.problem_description}"
        else:
            prompt = (f"{action}. A skilled Python Developer gave you the following feedback to improve your code:\n"
                        f"{review}\n\nCurrent code to improve:\n{previous_code}\n"
                        "Send the entire code back everytime, with all functions needed for the program to run smoothly.")
        
        response = self.generate(prompt)
        
        # Extract only the code from the response
        return self.extract_code(response)
    

    def extract_code(self, content):
        """
        Extracts code from the response by looking for code blocks.
        This assumes code is enclosed in triple backticks ``` or other delimiters.
        """
        # Look for code blocks enclosed in triple backticks
        code_blocks = re.findall(r"```(?:python)?\n(.*?)```", content, re.DOTALL)
        
        if code_blocks:
            # Join multiple code blocks if any are found, or use the first one
            return "\n".join(code_blocks).strip()
        else:
            # If no code blocks are found, return the response as is
            return content.strip()



class Reviewer(LLMAgent):
    def __init__(self, model="llama3.2:1b", problem_description=""):
        super().__init__(model)
        self.problem_description = problem_description

    def review_code(self, code, action):
        """
        Reviews the code by performing static analysis, checking for bugs, and generating feedback.
        :param code: Code to be reviewed.
        :return: Feedback and total score.
        """
        # Execute static analysis using Ruff
        static_analysis_report = self._static_analysis_ruff(code)

        # Attempt to execute code to check for runtime errors
        success, execution_report = self._execute_code(code)

        # Generate detailed feedback
        prompt = (f"{action} Consider the following problem: {self.problem_description}.\n\n"
                f"Static Analysis (Ruff):\n{static_analysis_report}\n\n"
                f"Execution Results:\n{execution_report}\n\n"
                f"Review the code below and provide detailed feedback to the coder. "
                f"Include suggestions to fix execution errors if they exist:\n{code}\n\n")

        feedback = self.generate(prompt)
        
        # Compile the feedback into a structured report
        report = self._generate_report(static_analysis_report, execution_report, feedback)
        
        # Score based on issues found and improvements suggested
        score = self._calculate_score(static_analysis_report, success)

        return report, score

    def _static_analysis_ruff(self, code):
        """
        Uses Ruff to perform static analysis on the code.
        :param code: Code to be analyzed.
        :return: Report from Ruff as a string.
        """
        try:
            # Save code temporarily to pass it to Ruff
            temp_file_path = pathlib.Path("temp_code.py").resolve()  # Generate absolute path
            with open(temp_file_path, "w") as f:
                f.write(code)

            print(f"Temporary file path for Ruff: {temp_file_path}")  # Debugging path

            # Run Ruff with "check" subcommand
            ruff_result = subprocess.run(
                ["ruff", "check", str(temp_file_path)],
                capture_output=True,
                text=True
            )
            if ruff_result.returncode == 0:
                return ruff_result.stdout
            else:
                return f"Ruff Error: {ruff_result.stderr}"
        except FileNotFoundError:
            return "Error: Ruff is not installed or not found in the system PATH."
        except Exception as e:
            print(f"Error running Ruff: {e}")
            return "Error: Could not complete static analysis with Ruff."

    def _execute_code(self, code):
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
                timeout=20 # kind of big, but it worked
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

    def _generate_report(self, static_analysis_report, execution_report, feedback):
        """
        Generates a detailed report including static analysis, execution results, and feedback.
        :param static_analysis_report: Results from static analysis.
        :param execution_report: Results from code execution.
        :param feedback: Feedback generated based on code quality.
        :return: Combined report as a string.
        """
        report = (
            f"=== Code Review Report ===\n\n"
            f"Static Analysis (Ruff):\n{static_analysis_report}\n\n"
            f"Execution Results:\n{execution_report}\n\n"
            f"Reviewer Feedback:\n{feedback}\n"
        )
        return report

    def _calculate_score(self, static_analysis_report, success):
        """
        Calculates a score based on the static analysis results and execution success.
        :param static_analysis_report: Results from static analysis.
        :param success: Boolean indicating if the code executed successfully.
        :return: Calculated score based on review quality.
        """
        # Scoring based on static analysis issues
        static_issues = static_analysis_report.count("\n")  # Count lines in the Ruff report
        static_score = max(0, 10 - static_issues)  # Deduct points for each issue

        # Scoring based on execution success
        execution_score = 5 if success else -5  # Reward for successful execution

        return static_score + execution_score
