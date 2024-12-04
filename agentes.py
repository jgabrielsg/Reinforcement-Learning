import ollama
import ast
import re
import ruff
import subprocess
import sys
import os
import pathlib
import time
import psutil
from sklearn.metrics import precision_score, recall_score, f1_score

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
                f"Review the code below and provide detailed feedback based on the following criteria:\n\n"
                f"1. **Data Analysis (20 points)** - Evaluate the clarity and quality of the data analysis. Give a score from 0 to 20.\n"
                f"2. **Adherence to PEP-8 (20 points)** - Evaluate the use of good naming practices and PEP-8 compliance. Give a score from 0 to 20.\n"
                f"3. **Code logic and structure (20 points)** - Evaluate the clarity and efficiency of the code logic and structure. Give a score from 0 to 20.\n"
                f"4. **Code comments (10 points)** - Evaluate the quantity and clarity of the comments in the code. Give a score from 0 to 10.\n"
                f"5. **Visualizations (10 points)** - Evaluate the clarity and usefulness of the visualizations. Give a score from 0 to 10.\n"
                f"6. **Error prevention (10 points)** - Evaluate whether the code implements checks to prevent errors. Give a score from 0 to 10.\n"
                f"7. **Code optimization (10 points)** - Evaluate the efficiency of the code. Give a score from 0 to 10.\n\n"
                f"Code to review:\n{code}\n. Don't send any code back to the Coder, just review the code, don't send more code back.")

        feedback = self.generate(prompt)
        
        # Compile the feedback into a structured report
        report = self._generate_report(static_analysis_report, execution_report, feedback)
        
        # Score based on issues found and improvements suggested
        score = self._calculate_score(static_analysis_report, success, feedback)

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

    def _calculate_score(self, static_analysis_report, success, feedback):
        """
        Calculates a score based on the static analysis results, execution success, and reviewer feedback.
        :param static_analysis_report: Results from static analysis.
        :param success: Boolean indicating if the code executed successfully.
        :param feedback: The feedback string containing the scores.
        :return: Calculated score based on review quality.
        """
        try:
            # Extract scores from feedback
            scores, total_score = self._getScore(feedback)
        except ValueError:
            # Default scores if extraction fails
            scores = [0, 0, 0, 0, 0, 0, 0]
            total_score = -1
            return total_score


        static_issues = static_analysis_report.count("\n")  # Count lines in the Ruff report
        static_score = max(-20, 10 - static_issues)  # Deduct points for each issue

        execution_score = 20 if success else -20  # Reward for successful execution
        
        total_score + static_score + execution_score # Final score
        return max(0, total_score)
    
    def _getScore(self, feedback):
        """
        Extracts the scores from the feedback and calculates the total score.
        :param feedback: The feedback string containing the scores.
        :return: Tuple with a list of individual scores and the total score.
        """

        # Regular expression to match scores in almost any format with "(X 'something')"
        pattern = r"\(\s*(\d+)\s*(?:[^)]*)?\)"
        scores = re.findall(pattern, feedback)  # Extract all scores as strings
        
        if scores:
            scores = list(map(int, scores))  # Convert to a list of integers
            total_score = sum(scores)  # Calculate the total score
            return scores, total_score
        else:
            raise ValueError("Scores not found in the feedback.")
            
class MonitoringAndFeedbackAgent:
    def __init__(self):
        # Inicialização do agente com valores padrão
        self.start_time = None
        self.end_time = None

    def monitor_execution_time(self, code):
        """
        Monitora o tempo de execução de um código e retorna o tempo gasto.
        """
        self.start_time = time.time()  # Começa a medir o tempo
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.end_time = time.time()  # Termina a medição do tempo
        execution_time = self.end_time - self.start_time
        return result, execution_time

    def monitor_resource_usage(self):
        """
        Monitora o uso de memória e CPU durante a execução.
        """
        # Obtém informações do sistema de recursos
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / (1024 * 1024)  # Memória usada em MB
        cpu_usage = psutil.cpu_percent(interval=1)  # Percentual de uso de CPU
        return memory_usage, cpu_usage

    def calculate_score_ratio(self, score, max_score=130):
        """
        Calcula o score em uma escala de score/130 e aplica um limiar (threshold).
        :param score: A pontuação do código.
        :param max_score: O valor máximo da pontuação (por padrão 130).
        :return: A razão do score/130.
        """
        score_ratio = score / max_score  # Calcular a razão score/130
        return score_ratio

    def provide_feedback(self, code, score):
        """
        Fornece feedback contínuo sobre o código e o modelo.
        """
        # Monitoramento do modelo
        result, execution_time = self.monitor_execution_time(code)
        memory_usage, cpu_usage = self.monitor_resource_usage()
        score_ratio = self.calculate_score_ratio(score)


        feedback = f"""
        === Performance Feedback ===
        Tempo de execução do código: {execution_time:.2f} segundos
        Uso de memória: {memory_usage:.2f} MB
        Uso de CPU: {cpu_usage:.2f}%
        """
        
        # Sugestões de melhorias
        if execution_time > 10:
            feedback += "\nSugestão: O tempo de execução está muito alto. Considere otimizar o algoritmo."
        if memory_usage > 100:
            feedback += "\nSugestão: O código está consumindo muita memória. Verifique o uso de estruturas de dados."
        if cpu_usage > 10:
            feedback += "\nSugestão: O código está utilizando muita CPU. Tente otimizar a complexidade do algoritmo."
        if score_ratio < 0.60: 
            feedback += "\nSugestão: A pontuação do código está abaixo do esperado. Tente melhorar a eficiência e sofrer menos penalizações."

        # Imprimir feedback
        print("Feedback gerado:\n", feedback)

        return feedback, score