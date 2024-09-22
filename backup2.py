# Written by Vinicio S. Flores <v-viniciof@microsoft.com> 
# Modified to handle semicolon-delimited CSV files
# Copyright & under Software IP rights (intellectual-property)
import random
import os
import csv
import io
import sys
import textwrap
import pandas as pd

questions_input_file = 'az900_questions.csv'

class FontColours:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

class Question:
    def __init__(self, question, options, correct_answer, explanation=""):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation

class ExamSimulator:
    def __init__(self, csv_file):
        self.renderer = FontColours()
        self.curate_exam_file()
        self.csv_file = csv_file
        self.questions = self.load_questions()
        self.score = 0
        self.total_questions = len(self.questions)

    def curate_exam_file(self):
        # Read the CSV file with semicolon delimiter
        df = pd.read_csv(questions_input_file, sep=';')
        # Prepare a backup (just in case) - Murphy's Law
        df.to_csv(questions_input_file + 'bak', sep=';', index=False)
        # Replace ',' with ' ' and trim tabs/whitespaces in the 'long-text' columns
        columns_to_clean = ['Question', 'OptionA', 'OptionB', 'OptionC', 'OptionD', 'Explanation']
        for col in columns_to_clean:
            df[col] = df[col].str.replace(',', ' ').replace('[', ' ').replace(']', ' ').str.strip()

        # Save the updated CSV with semicolon delimiter
        df.to_csv(questions_input_file, sep=';', index=False)
        df.head()

    def load_questions(self):
        questions = []
        try:
            # Set the field size limit to a more reasonable value
            csv.field_size_limit(min(sys.maxsize, 2147483647))  # Use 2GB as max on 32-bit systems

            with open(self.csv_file, 'r', encoding='utf-8', newline='') as file:
                content = file.read()
                csv_file = io.StringIO(content)
                csv_reader = csv.reader(csv_file, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    if len(row) >= 6:
                        question = row[0]
                        options = [
                            f"A. {row[1]}",
                            f"B. {row[2]}",
                            f"C. {row[3]}",
                            f"D. {row[4]}",
                            f"Q. Abort"
                        ]
                        correct_answer = row[5]
                        explanation = row[6] if len(row) > 6 else ""
                        wrapped_explanation = textwrap.fill(explanation, width=70)  # Adjust width as necessary
                        questions.append(Question(question, options, correct_answer, wrapped_explanation))
        except FileNotFoundError:
            print(f"{self.renderer.FAIL}Error: The file '{self.csv_file}' was not found.{self.renderer.ENDC}")
            sys.exit(1)
        except csv.Error as e:
            print(f"{self.renderer.FAIL}Error reading CSV file: {e}{self.renderer.ENDC}")
            sys.exit(1)
        
        if not questions:
            print(f"{self.renderer.WARNING}No questions were loaded from the CSV file.{self.renderer.ENDC}")
            sys.exit(1)
        
        return questions

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run_exam(self):
        random.shuffle(self.questions)
        for i, question in enumerate(self.questions, 1):
            self.clear_screen()
            print(f"{self.renderer.OKBLUE}Question #{self.renderer.ENDC}{self.renderer.BOLD}{i} of {self.renderer.BOLD}{self.total_questions}{self.renderer.ENDC}")
            print(f"{self.renderer.UNDERLINE}{question.question}{self.renderer.ENDC}")
            for option in question.options:
                print(option)
            
            user_answer = input(f"Your answer (A, B, C, D or Abort(Q)): ").strip().upper()
            while user_answer not in ['A', 'B', 'C', 'D', 'Q']:
                user_answer = input(f"{self.renderer.WARNING}Invalid input. Please enter A, B, C, or D: {self.renderer.ENDC}").strip().upper()
            
            if user_answer == 'Q':
                print(f"{self.renderer.WARNING}Exiting and aborting exam test ... See You Later!!")
                quit()

            if user_answer == question.correct_answer:
                print(f"{self.renderer.OKGREEN}\nCorrect!{self.renderer.ENDC}")
                self.score += 1
            else:
                print(f"{self.renderer.WARNING}\nIncorrect. The correct answer is {self.renderer.UNDERLINE}{question.correct_answer}.{self.renderer.ENDC}")
            
            if question.explanation:
                print(f"{self.renderer.BOLD}Explanation: {self.renderer.ENDC}{question.explanation.replace('Solution:','\nSolution:')}")
            input("\nPress Enter to continue...")

    def show_results(self):
        self.clear_screen()
        percentage = (self.score / self.total_questions) * 1000
        print(f"{self.renderer.OKBLUE}Exam completed! Your score (Microsoft Notation - Max Score is 1000, Passing Score is 700): {self.score}/{self.total_questions} ({percentage:.2f}%){self.renderer.ENDC}")
        if percentage >= 700:
            print(f"{self.renderer.OKGREEN}Congratulations! You have passed the exam.{self.renderer.ENDC}")
        else:
            print(f"{self.renderer.FAIL}You did not pass the exam. Keep studying and try again!{self.renderer.ENDC}")

def main():
    csv_file = questions_input_file  # Replace with your CSV file name
    simulator = ExamSimulator(csv_file)
    print(f"{simulator.renderer.HEADER}Welcome to the AZ-900 (Microsoft Azure Fundamentals) Exam Simulator!{simulator.renderer.ENDC}{simulator.renderer.UNDERLINE} -Copyright Vinicio S. Flores <v.flores.hernandez@accenture.com>")
    input(f"{simulator.renderer.BOLD}Press Enter to start the exam...{simulator.renderer.ENDC}")
    simulator.run_exam()
    simulator.show_results()

if __name__ == "__main__":
    main()