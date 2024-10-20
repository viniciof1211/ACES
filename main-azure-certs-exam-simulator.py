# Written by Vinicio S. Flores <v.flores.hernandez@accenture.com>
# Modified to include certification menu selection
# Modified to handle semicolon-delimited CSV files
# Copyright & under Software IP rights (intellectual-property)
# MIT-Licensed 

"""
     This program simulates Microsoft Azure certification exams in multiple languages.
     It allows users to practice for various Azure certifications and provides detailed feedback.
"""

import random
import os
import csv
import io
import re
import sys
import textwrap
import asyncio
import subprocess
import aiohttp
import pandas as pd
from googletrans import Translator, LANGUAGES
from functools import lru_cache
import nltk
from nltk.tokenize import word_tokenize
from concurrent.futures import ThreadPoolExecutor
import time
import spacy
import json
import matplotlib.pyplot as plt 
from matplotlib import font_manager

print("[DEBUG] Loading initial and background modules ... Please wait ....")

# Load the English language model
nlp = spacy.load("en_core_web_sm")
# Global variable to store the selected CSV file
questions_input_file = ''
translation_enabled = True
# Preps the fetches from Punkt model package (NLTK = Natural Language Toolkit), 
# Contains sentence & word tokenization data needed for NLP operations.
def download_nltk_data():
    try:
        nltk.download('punkt')
        nltk.download('punkt_tab')
        print("NLTK 'punkt' & 'punkt_tab' resource downloaded and verified successfully.")
    except Exception as e:
        print(f"Failed to download NLTK 'punkt' resource: {e}")
        sys.exit(-1)

download_nltk_data()
nltk.data.path.append('C:/nltk_data')  # Add your NLTK data path manually


class Sources:
    def __init__(self):
        self.cert_name = cert_name
        self.apa_quotes = [('','')] # List of Tuples (category per cert, source)

    def add_apa_citation(self, category, quotes):
        for cite in quotes:
            self.apa_quotes.append((category, cite))

class Languages:
    # This class manages language selection and translation functionality
    # It supports multiple languages for a global audience of exam takers
    def __init__(self):
        self.ENGLISH = 'en'
        self.SPANISH = 'es'
        self.PORTUGUESE = 'pt'
        self.FRENCH = 'fr'
        self.JAPANESE = 'ja'
        self.needs_translation = True

    def set_language(self, lang):
        # Sets the exam language and initializes the translator if needed
        # This allows the exam to be taken in the user's preferred language
        global gtr
        self.needs_translation = (lang != self.ENGLISH)
        if self.needs_translation:
            gtr = Translator(user_agent='ETC-CertTester/1.0')
        else:
            gtr = None

    # Decorator Least-Recently-Used (LRU) side-in-memory-local-cache design-pattern to avoid "DDoS Carpet Bombing"
    # against Google Translator's API so we don't get throttled & banned, thus our
    # multilanguage simulator gets rid of 'single point of failures' caused by Google Cloud's DDoS hardening.
    @lru_cache(maxsize=2048)
    # Here we achieve 'memoization', typical of 'Dynamic Programming' paradigm so we reuse previous results locally 
    # instead of brute force, going from O(n) complexity runtimes to O(nlog[n])
    def translate(self, text):
        # Translates text using caching to improve performance and reduce API calls
        # This ensures efficient multilingual support throughout the exam process
        global lang, translation_enabled
        if self.needs_translation and translation_enabled:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return gtr.translate(text, dest=lang, src='auto').text
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"Translation attempt {attempt + 1} failed. Retrying...")
                        time.sleep(1)
                    else:
                        print(f"Translation failed after {max_retries} attempts: {e}")
                        print("Proceeding without translation. To retry, please restart the program.")
                        translation_enabled = False
                        return text
        return text

# Global translator - will be set in set_language() method
gtr = None

class FontColours:
    # Defines color codes for text formatting in the console
    # Enhances user experience by providing visual cues and emphasis
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

# *********************************************************************************

class Question:
    def __init__(self, question, options, correct_answer, explanation=""):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.category = None # Initialize category as None, will be set by ExamSimulator

class ExamSimulator:
    # Core class that manages the entire exam simulation process
    def __init__(self, csv_file, renderer, translator, certification_json_path, certification_name):
        # Initializes the exam simulator with necessary components
        # Sets up the exam environment based on the selected certification
        self.renderer = renderer
        self.translator = translator
        self.csv_file = csv_file
        self.certification_name = certification_name
        self.certification_data = self.load_certification_json(certification_json_path)
        self.nlp = spacy.load("en_core_web_sm")
        self.questions = self.load_questions()
        self.score = 0
        self.total_questions = len(self.questions)
        self.category_scores = self.initialize_category_scores()
        self.src_mgr = Sources()

    # =====================================================#
    global translated_texts
    global questions

    def load_sources(self):
        src_mgr.add_apa_citation(self.certification_name, citations)
        src_mgr.add_apa_citation(self.certification_name, citations)
        src_mgr.add_apa_citation(self.certification_name, citations)
        src_mgr.add_apa_citation(self.certification_name, citations)

    def load_questions(self):
        # Loads and processes questions from the CSV file
        # Translates questions if necessary and categorizes them
        questions = []
        translated_texts  = []
        try:
            # Load the CSV file
            df = pd.read_csv(self.csv_file, sep=';')
            print(f"[DEBUG][load_questions] CSV file loaded successfully. Shape: {df.shape}")
            print(f"[DEBUG][load_questions] Columns: {df.columns}")

            # Check for expected columns
            expected_columns = ['Question', 'OptionA', 'OptionB', 'OptionC', 'OptionD', 'CorrectAnswer', 'Explanation']
            for col in expected_columns:
                if col not in df.columns:
                    print(f"[DEBUG][load_questions] Missing expected column: {col}")
                    return []

            texts_to_translate = []

            for index, row in df.iterrows():
                try:
                    # Check the type of 'row' to ensure it's a Series
                    if isinstance(row, pd.Series):
                        texts_to_translate.extend([
                            row.array[0],
                            row.array[1],
                            row.array[2],
                            row.array[3],
                            row.array[4],
                            row.array[5],
                            row.array[6]
                        ])
                    else:
                        print(f"[DEBUG][load_questions] Unexpected row type at index {index}: {type(row)}")
                except Exception as e:
                    print(f"[DEBUG][load_questions] Error processing row index {index}: {e}")

            # Proceed to translate texts
            translated_texts = self.parallel_translate(texts_to_translate)

            if isinstance(translated_texts, list) and all(isinstance(text, str) for text in translated_texts):
                print(f"{self.renderer.OKGREEN}[DEBUG][load_questions] All translated texts are strings.")
            else:
                print(f"{self.renderer.FAIL}[DEBUG][load_questions] Translated texts are not in the expected format!")
            
            #print(f"{self.renderer.WARNING}[DEBUG][load_questions] Type of translated_texts: {type(translated_texts)}")
            #print(f"{self.renderer.WARNING}[DEBUG][load_questions] Translated texts content (trimmed): {translated_texts[:7]}")
            #print(self.renderer.ENDC)

            # Check if any translations are empty
            if not any(translated_texts):
                print("[DEBUG][load_questions] No translations were returned. Please check your translation logic since 'parallel_translate' returned an empty list.")
            i = 0
            # Process translated texts safely (avoid looping 'out of bounds')
            while i < len(translated_texts):
                if i + 6 >= len(translated_texts):  # Ensure enough data for a full set of 6 items
                    print(f"[DEBUG][load_questions] Not enough translated texts to create a question for index {i}")
                    break  # Exit the loop if there's not enough data for a complete question
                # print(f"[DEBUG][load_questions] Processing translated_texts from index {i} to {i + 5}")
  
                try:
                    question = textwrap.fill(translated_texts[i], width=70).strip()
                    # print(f"{self.renderer.BOLD}[DEBUG][load_questions] Question text: {question}\n{self.renderer.ENDC}")
                
                    options = [
                        f"A.{translated_texts[i+1]}",
                        f"B.{translated_texts[i+2]}",
                        f"C.{translated_texts[i+3]}",
                        f"D.{translated_texts[i+4]}"
                    ]
                    correct_answer = translated_texts[i+5].upper()  # Ensure it's a string and uppercase
                    explanation = textwrap.fill(translated_texts[i+6].strip(), width=70)  # Ensure it's a string
                    question_obj = Question(question, options, correct_answer, explanation)
                    question_obj.category = self.categorize_question(question + " , " + explanation)
                    questions.append(question_obj)

                    i += 7      # Move to the next set of 7 items (Question + 6 fields)
                except IndexError as e:
                    print(f"[DEBUG][load_questions] IndexError at index {i}[ * is_integer = {i.is_integer()}]: {e}")
                except Exception as e:
                    print(f"[DEBUG][load_questions] Error processing translated texts at index {i}[ * is_integer = {i.is_integer()}]: {e}")

            if not questions:
                print(self.renderer.WARNING + self.translator.translate("No questions were loaded from the CSV file.") + self.renderer.ENDC)
                sys.exit(1)

            print(f"[DEBUG][load_questions] Loaded {len(questions)} questions successfully.")
            return questions

        except Exception as e:
            print(f"[DEBUG][load_questions] Error in 'load_questions()': {translated_texts}|{e.add_note}|{e.args}|{e.__traceback__}")
            raise

    # Execute translations asynchronously, concurrently & quasi-parallel runs - 
    # improving overall performance.
    async def translate_batch(self, texts):
        # Performs batch translation of texts asynchronously
        # Improves performance for translating large sets of exam questions
        async with aiohttp.ClientSession() as session:
            tasks = [self.translator.translate(text) for text in texts]
            return await asyncio.gather(*tasks)

    def clear_screen(self):
        # Clears the console screen for a clean user interface
        # Enhances readability during the exam process
        # For Windows
        if os.name == 'nt':
            _ = os.system('cls')
        # For Mac and Linux
        else:
            _ = os.system('clear')

    def load_certification_json(self, filename):
        # Loads certification-specific data from a JSON file
        # Allows for dynamic configuration of different exam types and their scoring breakdown categories
        try:
            print(f"{self.renderer.WARNING}[DEBUG][load_certification_json] Trying to open '{filename}'")
            with open(filename, 'r') as f:
                data = json.load(f)
                # print(f"{self.renderer.OKCYAN}[DEBUG][load_certification_json] Loaded certification data: {data}")
                return data
        except Exception as e:
            print(f"{self.renderer.FAIL}[FATAL][load_certification_json] Error loading JSON: {e}")
            return None            

    def initialize_category_scores(self):
        categories = self.get_certification_categories()
        if not categories:
            print(f"Warning: No categories found for certification {self.certification_name}")
            return {f"Uncategorized - Warning: No categories found for certification {self.certification_name}": 0}
        return {category: 0 for category in categories}

    def categorize_question(self, question_text):
        categories = self.get_certification_categories()
        if not categories or categories == ["Uncategorized"]:
            return "Uncategorized - no categories found."
        doc = self.nlp(question_text.lower())
        # Initialize a dictionary to store keyword match counts for each category
        category_keyword_counts = {}
        # Iterate over all categories loaded for the current certification
        for cert in self.certification_data["certifications"]:
            if cert['certification'] == self.certification_name:
                for category in cert['categories']:
                    # Count keyword matches
                    keywords = category['keywords']
                    count = sum(1 for token in doc if any(keyword.lower() in token.text for keyword in keywords))
                    # Store the count for this category
                    category_keyword_counts[category['category']] = count
        # Find the category with the highest keyword match count
        best_category = max(category_keyword_counts, key=category_keyword_counts.get)
        # Return the category with the most keyword matches
        return best_category

    def get_certification_categories(self):
        if not self.certification_data:
            print("Error: Certification data not loaded.")
            return []
        certification = next((cert for cert in self.certification_data.get("certifications", []) 
                              if cert["certification"] == self.certification_name), None)
        if certification:
            categories = [cat["category"] for cat in certification.get("categories", [])]
            if not categories:
                # print(f"Warning: No categories found for certification {self.certification_name}")
                return [f"Uncategorized: No categories found for certification {self.certification_name}"]
            return categories
        print(f"Error: Certification {self.certification_name} not found in the JSON data.")
        return [f"Uncategorized - Error: Certification {self.certification_name} not found in the JSON data."]

    def analyze_nlp_for_category(self, category_name):
        certification = next((cert for cert in self.certification_data["certifications"] 
                              if cert["certification"] == self.certification_name), None)
        if certification:
            category = next((cat for cat in certification["categories"] 
                             if cat["category"] == category_name), None)
            if category:
                return category.get("keywords", [])
        return None

    ######################################################

    def run_exam(self):
        # Executes the main exam process
        # Presents questions, captures user answers, and provides immediate feedback
        random.shuffle(self.questions)
        for i, question in enumerate(self.questions, 1):
            self.clear_screen()
            print(self.renderer.OKBLUE + self.translator.translate(f"Question #{i} of {self.total_questions}") + self.renderer.ENDC + "\n")
            """
            Ask the question!
            """
            # fprint(self.renderer.UNDERLINE + question.question + self.renderer.ENDC, "white")
            print(self.renderer.UNDERLINE + question.question + self.renderer.ENDC + "\n")
            for option in question.options:
                print(option)
            
            user_answer = input(self.translator.translate("Your answer (A, B, C, D or Abort[Q]): ")).strip().upper()
            while user_answer not in ['A', 'B', 'C', 'D', 'Q']:
                user_answer = input(self.renderer.WARNING + self.translator.translate("Invalid input. Please enter A, B, C, or D: ") + self.renderer.ENDC).strip().upper()
            
            if user_answer == 'Q':
                print(self.renderer.WARNING + self.translator.translate("Exiting and aborting exam test ... See You Later!!") + self.renderer.ENDC)
                print(f"{self.renderer.WARNING}Printing score up to this point until the exam was aborted: ")
                return

            if user_answer == question.correct_answer:
                print(self.renderer.OKGREEN + self.translator.translate("\nCorrect!") + self.renderer.ENDC)
                self.score += 1
                print(f"{self.renderer.OKCYAN}\n[Category bucket OnVue-Proctor Scored -> .... {self.renderer.WARNING}{question.category}{self.renderer.ENDC} ] - \n")
                self.category_scores[question.category] += 1

            else:
                print(self.renderer.WARNING + self.translator.translate(f"\nIncorrect. The correct answer is {question.correct_answer}.") + self.renderer.ENDC)
            
            if question.explanation:
                print(self.renderer.BOLD + self.translator.translate("Explanation: ") + self.renderer.ENDC + question.explanation)
            input(self.translator.translate("\nPress [Enter] to continue..."))

    def show_results(self):
        # Executes the main exam process
        # Presents questions, captures user answers, and provides immediate feedback
        self.clear_screen()
        percentage = (self.score / self.total_questions) * 1000
        print(self.renderer.OKBLUE + self.translator.translate(f"Exam {self.renderer.BOLD}{cert_name}{self.renderer.ENDC} completed! Your score (Microsoft Notation - Max Score is 1000, Passing Score is 700): {self.score}/{self.total_questions} ({percentage:.2f}%)") + self.renderer.ENDC)
        if percentage >= 700:
            print(self.renderer.OKGREEN + self.translator.translate("Congratulations! You have passed the exam: ") + "" + f"{self.renderer.BOLD}{cert_name}" + "" + self.renderer.ENDC)
        else:
            print(self.renderer.FAIL + self.translator.translate("You did not pass the exam. Keep studying and try again the " + f"{self.renderer.BOLD}{cert_name}{self.renderer.ENDC}" + " exam, Good Luck next time, Mate!") + self.renderer.ENDC)
        print(f"\n{self.renderer.WARNING}Score breakdown by category:{self.renderer.ENDC}")
        self.display_category_scores()

    ######################################################

    def initialize_category_scores(self):
        categories = self.get_certification_categories()
        return {category: 0 for category in categories}

    def get_certification_categories(self):
        certification = next((cert for cert in self.certification_data["certifications"] 
                              if cert["certification"] == self.certification_name), None)
        if certification:
            return [cat["category"] for cat in certification["categories"]]
        return []

    def display_category_scores(self):
        max_length = max(len(category) for category in self.category_scores.keys())
        for category, score in self.category_scores.items():
            category_score = (score / self.total_questions) * 1000 # OnVue max score is 1000
            bar_length = int(category_score / 20)  # Scale to 50 characters max
            bar = '█' * bar_length + '▒' * (50 - bar_length)
            # Get category weight from JSON
            category_weight = self.get_category_weight(category)
            # Analyze NLP keywords for the category
            keywords = self.analyze_nlp_for_category(category)
 
            if keywords:
                keyword_info = f"\nTop keywords: {', '.join(keywords[:10])}"
            else:
                keyword_info = "\nNo keywords available for this category."
            print(f"{category.ljust(max_length)} : {bar} {category_score:.2f} (Weight: {category_weight})")

    def get_category_keywords(self, category_name):
        certification = next((cert for cert in self.certification_data["certifications"] 
                              if cert["certification"] == self.certification_name), None)
        if certification:
            category = next((cat for cat in certification["categories"] 
                             if cat["category"] == category_name), None)
            if category:
                return category.get("keywords", {})
        return None

    def get_category_weight(self, category_name):
        # Retrieves the weight of a specific category in the exam
        # Ensures accurate scoring based on the certification's requirements
        certification = next((cert for cert in self.certification_data["certifications"] 
                              if cert["certification"] == self.certification_name), None)
        if certification:
            category = next((cat for cat in certification["categories"] 
                             if cat["category"] == category_name), None)
            if category:
                weight = category.get("weight", "0%")
                return float(weight.split('-')[0].strip('%')) / 100  # Convert percentage to decimal
        return 0

    def tokenize_and_translate(self, text):
        # Breaks down and translates text for more accurate language processing
        # Supports the multilingual aspect of the exam simulator
        # print(f"[DEBUG][tokenize_and_translate] Received text for translation: {text}")  # Debug input
        if not isinstance(text, str):
            print(f"[DEBUG][tokenize_and_translate] Received a '{text}' data type instead of a string. Converting to string.")
            text = str(text)
        try:
            # Ensure the Punkt tokenizer is downloaded
            try:
                nltk.data.find('tokenizers/punkt')
            except Exception:
                print(f"[DEBUG][tokenize_and_translate] NLTK's {nltk.data.find('tokenizers/punkt')} not found, downloading again ...")
                download_nltk_data()
            tokens = word_tokenize(text)
            translated_tokens = [self.translator.translate(token) for token in tokens]
            result = ' '.join(translated_tokens)
            # print(f"[DEBUG][tokenize_and_translate] Translated result: {result}")  # Debug output
            # print(f"[DEBUG][tokenize_and_translate] Translated result's count: {result.count(result)}")  # Debug output
            return result if result else ''
        except LookupError:
            return ' '.join([self.translator.translate(word) for word in text.split()])
        except Exception as e:
            print(f"[WARNING][tokenize_and_translate] Tokenization failed: {e}. Using original text.")
            return self.translator.translate(text)  
        
    def parallel_translate(self, texts):
        # Performs translations in parallel to improve efficiency
        # Speeds up the process of preparing multilingual exam content
        # Filter out None or non-string types from texts
        
        valid_texts = [text for text in texts] # if isinstance(text, str) and text.strip()]

        with ThreadPoolExecutor() as executor:
            translated_texts = list(executor.map(self.tokenize_and_translate, texts))
            """
            print(f"{self.renderer.BOLD}[DEBUG][parallel_translate] -> 'translated_texts[0]'' = {translated_texts[0]}{self.renderer.ENDC}")
            print(f"{self.renderer.BOLD}[DEBUG][parallel_translate] -> 'translated_texts[1]'' = {translated_texts[1]}{self.renderer.ENDC}")
            print(f"{self.renderer.BOLD}[DEBUG][parallel_translate] -> 'translated_texts[2]'' = {translated_texts[2]}{self.renderer.ENDC}")
            print(f"{self.renderer.BOLD}[DEBUG][parallel_translate] -> 'translated_texts[3]'' = {translated_texts[3]}{self.renderer.ENDC}")
            print(f"{self.renderer.BOLD}[DEBUG][parallel_translate] -> 'translated_texts[4]'' = {translated_texts[4]}{self.renderer.ENDC}")
            print(f"{self.renderer.BOLD}[DEBUG][parallel_translate] -> 'translated_texts[5]'' = {translated_texts[5]}{self.renderer.ENDC}")
            print(f"{self.renderer.BOLD}[DEBUG][parallel_translate] -> 'translated_texts[6]'' = {translated_texts[6]}{self.renderer.ENDC}")            
            """
            # Verify that all elements in translated_texts are strings
        # if not all(isinstance(text, str) for text in translated_texts):
        #    print("[DEBUG][parallel_translate] Warning: Non-string value detected in translated_texts!")
        
        # Debugging: Log the translated texts
        # print(f"[DEBUG][parallel_translate] <<<<$$$ Total translated texts count &&&>>>>: {len(translated_texts)}")  # Count of total translations
        # print(f"[DEBUG][parallel_translate] Translated texts: {translated_texts}")  # Show contents of the list
        return translated_texts

#############################################################################
############## MAIN ENTRY POINT #############################################
#############################################################################

def main():

    """

        Main entry point of the program
        Manages the overall flow of the exam simulation process

        User selects language and certification
        This allows for a personalized exam experience

        Exam simulation is initiated
        The user goes through the exam process

        Results are displayed and the user is given the option to retry
        Provides immediate feedback and encourages continued learning

    """

    global questions_input_file
    global cert_name
    global lang
    global translation_enabled

    renderer = FontColours()
    langs = Languages()

    while True:
        try:
            simulator = None

            ### Interactive menu to implemented Spaced-Repetition (Leibniz Algorithm) 
            ### and microlearning tecniques.Main loop.
            print("Welcome to the ETC-CertTester Azure Exam Simulator!\n")
            print("Please choose your preferred language to take the test:")
            print(f"{renderer.OKCYAN}1. English{renderer.ENDC}")
            print(f"{renderer.OKCYAN}2. Español{renderer.ENDC}")
            print(f"{renderer.OKCYAN}3. Português{renderer.ENDC}")
            print(f"{renderer.OKCYAN}4. Français{renderer.ENDC}")
            print(f"{renderer.OKCYAN}5. 日本語{renderer.ENDC}")
            print(f"{renderer.OKCYAN}Q. Any key to quit{renderer.ENDC}")

            choice = input("Enter the number corresponding to your language: ").strip()

            if choice == '1':
                lang = langs.ENGLISH
            elif choice == '2':
                lang = langs.SPANISH
            elif choice == '3':
                lang = langs.PORTUGUESE
            elif choice == '4':
                lang = langs.FRENCH
            elif choice == '5':
                lang = langs.JAPANESE
            else:
                print("Invalid selection or chose to quit. Exiting...")
                sys.exit(0)

            langs.set_language(lang)  # Set the language and initialize translator if needed
\
            print(langs.translate("Please choose the Azure certification you want to practice:"))
            print(f"{renderer.BOLD}" + langs.translate("1. AZ-900: Microsoft Azure Fundamentals") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("2. AZ-104: Microsoft Azure Administrator") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("3. AZ-204: Developing Solutions for Microsoft Azure") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("4. AZ-305: Designing Microsoft Azure Infrastructure Solutions") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("5. AZ-400: Designing and Implementing Microsoft DevOps Solutions") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("6. AZ-500: Microsoft Azure Security Technologies") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("7. AZ-700: Designing and Implementing Microsoft Azure Networking Solutions") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("8. AZ-800: Administering Windows Server Hybrid Core Infrastructure") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("9. AZ-140: Configuring and Operating Microsoft Azure Virtual Desktop") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("10. MS-900: Microsoft 365 Certified: Fundamentals") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("11. PL-900: Microsoft Certified: Power Platform Fundamentals") + f"{renderer.ENDC}")
            print(f"{renderer.BOLD}" + langs.translate("Q. Abort/Exit Simulation Platform") + f"{renderer.ENDC}")

            choice = input(langs.translate("\nEnter the number corresponding to your certification: ")).strip().upper()

            ### Debugging print-outs - uncomment only when issues need to be investigated & fixed
            """
                print(f"{renderer.OKCYAN}[DEBUG] {choice}{renderer.ENDC}")
                print(f"{renderer.WARNING}[DEBUG] {choice.casefold}{renderer.ENDC}")
                print(f"{renderer.OKCYAN}[DEBUG] {choice}{renderer.ENDC}")
            """
            if choice == 'Q':
                print(f"{renderer.FAIL} Aborting ETC-CertTests simulation program ... See you later!\n {renderer.ENDC}")
                sys.exit(0)

            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
                cert_map = {
                    '1': ('az900_questions.csv', "AZ-900: Microsoft Azure Fundamentals"),
                    '2': ('az104_questions.csv', "AZ-104: Microsoft Azure Administrator"),
                    '3': ('az204_questions.csv', "AZ-204: Developing Solutions for Microsoft Azure"),
                    '4': ('az305_questions.csv', "AZ-305: Designing Microsoft Azure Infrastructure Solutions"),
                    '5': ('az400_questions.csv', "AZ-400: Designing and Implementing Microsoft DevOps Solutions"),
                    '6': ('az500_questions.csv', "AZ-500: Microsoft Azure Security Technologies"),
                    '7': ('az700_questions.csv', "AZ-700: Designing and Implementing Microsoft Azure Networking Solutions"),
                    '8': ('az800_questions.csv', "AZ-800: Administering Windows Server Hybrid Core Infrastructure"),
                    '9': ('az140_questions.csv', "AZ-140: Configuring and Operating Microsoft Azure Virtual Desktop"),
                    '10': ('ms900_questions.csv', "MS-900: Microsoft 365 Certified: Fundamentals"),
                    '11': ('pl900_questions.csv', "PL-900: Microsoft Certified: Power Platform Fundamentals")
                }
                questions_input_file, cert_name = cert_map[choice]

                # Check if the CSV file exists
                if not os.path.exists(questions_input_file):
                    raise FileNotFoundError(f"{renderer.FAIL}[FATAL] The file {questions_input_file} does not exist.")
            
                try:
                    simulator = ExamSimulator(questions_input_file, renderer, langs, 'scoring.json', cert_name)
        
                    if simulator is None:
                        print(f"{renderer.FAIL}[FATAL]'ExamSimulator' initialization failed. Please check input data.{renderer.ENDC}")
                    else:
                        print(f"{simulator.renderer.HEADER}" + langs.translate(f"Welcome to the {cert_name} Exam Simulator! -Copyright Vinicio S. Flores <v.flores.hernandez@accenture.com>") + f"{simulator.renderer.ENDC}")
                        input(f"{simulator.renderer.BOLD}" + langs.translate(f"Press Enter to start the exam...") + f"{simulator.renderer.ENDC}")
        
                        simulator.run_exam()
                        simulator.show_results()

                        continue_input = input(f"{simulator.renderer.BOLD}Want to try again another or same certification exam? (y/N) {simulator.renderer.ENDC}").strip().upper()
                        if continue_input == 'Y':
                            main()  # Restart from the beginning
                        elif continue_input == 'N':
                            break
                        else:
                            print(f"{renderer.WARNING} Invalid selection. Try again or press [Q] to abort simulation...")
                
                except FileNotFoundError as e:
                    print(f"{renderer.FAIL}Error: {e}{renderer.ENDC}")
                    print("Make sure the CSV file for this certification exists in the same directory as this script.")
                except Exception as e:
                    print(f"{renderer.FAIL}An error occurred during the exam: {e}{renderer.ENDC}")
                    print("The program will now return to the main menu.")
                    continue_input = input(f"{simulator.renderer.BOLD}Wanna try again another or same certification exam? (y/N) {simulator.renderer.ENDC}").strip().upper()
                    if continue_input != 'Y':
                        break
        except Exception as e:
            print(f"{renderer.FAIL}An error occurred in the main program: {e}{renderer.ENDC}")
            print("Please try again. If the problem persists, check your internet connection and make sure you have the necessary permissions to download NLTK data.")


if __name__ == "__main__":
    main()