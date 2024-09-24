# Written by Vinicio S. Flores <v-viniciof@microsoft.com>
# Modified to include certification menu selection
# Modified to handle semicolon-delimited CSV files
# Copyright & under Software IP rights (intellectual-property)

import random
import os
import csv
import io
import sys
import textwrap
import asyncio
import aiohttp
import pandas as pd
from googletrans import Translator, LANGUAGES
from functools import lru_cache
import nltk
from nltk.tokenize import word_tokenize
from concurrent.futures import ThreadPoolExecutor
import time
import spacy

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
        print("NLTK 'punkt' resource downloaded and verified successfully.")
    except Exception as e:
        print(f"Failed to download NLTK 'punkt' resource: {e}")

download_nltk_data()
nltk.download('punkt')

class Languages:
    def __init__(self):
        self.ENGLISH = 'en'
        self.SPANISH = 'es'
        self.PORTUGUESE = 'pt'
        self.FRENCH = 'fr'
        self.JAPANESE = 'ja'
        self.needs_translation = True

    def set_language(self, lang):
        global gtr
        self.needs_translation = (lang != self.ENGLISH)
        if self.needs_translation:
            gtr = Translator(user_agent='ETC-CertTester/1.0')
        else:
            gtr = None

    # Decorator Least-Recently-Used (LRU) side-in-memory-local-cache design-pattern to avoid "DDoS Carpet Bombing"
    # against Google Translator's API so we don't get throttled & banned, thus our
    # multilanguage simulator gets rid of 'single point of failures' caused by Google Cloud's DDoS hardening.
    @lru_cache(maxsize=1000)
    # Here we achieve 'memoization', typical of 'Dynamic Programming' paradigm so we reuse previous results locally 
    # instead of brute force, going from O(n) complexity runtimes to O(nlog[n])
    def translate(self, text):
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

# Category 1: Describe cloud concepts
cloud_concepts_keywords = [
    "cloud computing", "scalability", "elasticity", "agility", "fault tolerance",
    "disaster recovery", "high availability", "load balancing", "capex", "opex",
    "iaas", "paas", "saas", "public cloud", "private cloud", "hybrid cloud",
    "community cloud", "multi-cloud", "cloud-native", "serverless", "pay-as-you-go",
    "metered service", "economies of scale", "vertical scaling", "horizontal scaling",
    "cloud migration", "cloud adoption", "cloud strategy", "cloud security",
    "cloud compliance", "cloud governance", "cloud service provider", "virtualization",
    "containerization", "orchestration", "microservices", "distributed computing",
    "edge computing", "fog computing", "cloud storage", "cloud database",
    "cloud networking", "cloud analytics", "cloud ai", "cloud ml", "cloud iot",
    "cloud big data", "cloud devops", "cloud devsecops", "cloud automation",
    "cloud optimization", "cloud cost management", "cloud performance", "cloud sla",
    "cloud redundancy", "georeplication", "data residency", "data sovereignty",
    "shared responsibility model", "multi-tenancy", "resource pooling", "on-demand self-service",
    "rapid elasticity", "measured service", "cloud bursting", "cloud brokerage",
    "cloud marketplace", "cloud portal", "cloud console", "cloud api", "cloud sdk",
    "cloud cli", "cloud powershell", "cloud shell", "cloud monitoring", "cloud logging",
    "cloud auditing", "cloud billing", "cloud pricing", "cloud tco", "cloud roi",
    "cloud vendor lock-in", "cloud portability", "cloud interoperability", "cloud standards",
    "cloud certifications", "cloud architecture", "cloud design patterns", "cloud best practices",
    "cloud reference architecture", "cloud operating model", "cloud center of excellence",
    "cloud competency center", "cloud enablement", "cloud transformation", "digital transformation",
    "business agility", "innovation", "time-to-market", "global reach", "data center",
    "infrastructure modernization", "application modernization", "legacy systems",
    "hybrid it", "cloud-first strategy", "mobile-first strategy", "cloud wash",
    "shadow it", "bring your own device", "byod", "data gravity", "data lake",
    "data warehouse", "etl", "real-time processing", "batch processing", "stream processing",
    "event-driven architecture", "pub/sub", "message queue", "api gateway", "service mesh",
    "infrastructure as code", "gitops", "devsecops", "shift-left", "continuous integration",
    "continuous delivery", "continuous deployment", "blue-green deployment", "canary deployment",
    "a/b testing", "feature flags", "dark launching", "chaos engineering", "site reliability engineering",
    "observability", "telemetry", "distributed tracing", "service level objectives", "service level indicators",
    "error budgets", "capacity planning", "demand forecasting", "auto-scaling", "predictive scaling",
    "reserved instances", "spot instances", "serverless computing", "function as a service",
    "event-driven computing", "cloud-native security", "zero trust security", "identity and access management"
]

# Category 2: Describe Azure architecture and services
azure_architecture_keywords = [
    "azure", "azure portal", "azure cli", "azure powershell", "azure cloud shell",
    "azure resource manager", "arm templates", "azure bicep", "azure blueprints",
    "azure regions", "azure availability zones", "azure paired regions", "azure sovereign regions",
    "azure virtual machines", "azure vm scale sets", "azure containers", "azure kubernetes service",
    "azure container instances", "azure container registry", "azure app service", "azure functions",
    "azure logic apps", "azure service fabric", "azure batch", "azure storage account",
    "azure blob storage", "azure file storage", "azure queue storage", "azure table storage",
    "azure disk storage", "azure data lake storage", "azure cosmos db", "azure sql database",
    "azure sql managed instance", "azure database for mysql", "azure database for postgresql",
    "azure database for mariadb", "azure synapse analytics", "azure databricks", "azure hdinsight",
    "azure data factory", "azure stream analytics", "azure analysis services", "azure time series insights",
    "azure purview", "azure virtual network", "azure vpn gateway", "azure expressroute",
    "azure dns", "azure traffic manager", "azure load balancer", "azure application gateway",
    "azure frontdoor", "azure cdn", "azure ddos protection", "azure firewall", "azure bastion",
    "azure network watcher", "azure private link", "azure active directory", "azure ad b2c",
    "azure ad domain services", "azure information protection", "azure key vault", "azure sentinel",
    "azure security center", "azure ddos protection", "azure dedicated host", "azure arc",
    "azure stack", "azure stack hub", "azure stack edge", "azure sphere", "azure iot hub",
    "azure iot central", "azure digital twins", "azure maps", "azure time series insights",
    "azure machine learning", "azure cognitive services", "azure bot service", "azure openai service",
    "azure video analyzer", "azure kinect dk", "azure virtual desktop", "azure backup",
    "azure site recovery", "azure monitor", "azure log analytics", "azure application insights",
    "azure advisor", "azure service health", "azure policy", "azure lighthouse", "azure migrate",
    "azure dev center", "azure devops", "azure pipelines", "azure boards", "azure repos",
    "azure test plans", "azure artifacts", "github actions", "github advanced security",
    "azure communication services", "azure open datasets", "azure confidential computing",
    "azure quantum", "azure orbital", "azure private 5g core", "azure private mobile networks",
    "azure vmware solution", "azure spring cloud", "azure api management", "azure cache for redis",
    "azure netapp files", "azure hpc cache", "azure cyclecloud", "azure batch",
    "azure media services", "azure video indexer", "azure speech services", "azure immersive reader",
    "azure form recognizer", "azure face api", "azure computer vision", "azure personalizer",
    "azure metrics advisor", "azure anomaly detector", "azure content moderator", "azure translator",
    "azure cognitive search", "azure health bot", "azure health data services", "azure genomics",
    "azure virtual wan", "azure route server", "azure web application firewall", "azure defender",
    "azure information protection", "azure attestation", "azure dedicated hsm", "azure confidential ledger",
    "azure chaos studio", "azure deployment environments", "azure container apps", "azure static web apps",
    "azure data share", "azure managed grafana", "azure managed prometheus", "azure automation",
    "azure update management", "azure automanage", "azure resource mover", "azure virtual network manager"
]

# Category 3: Describe Azure management and governance
azure_management_keywords = [
    "azure resource manager", "azure resource groups", "azure subscriptions", "azure management groups",
    "azure rbac", "azure role assignments", "azure custom roles", "azure policy", "azure blueprints",
    "azure management locks", "azure tags", "azure cost management", "azure advisor", "azure monitor",
    "azure log analytics", "azure application insights", "azure service health", "azure resource graph",
    "azure arc", "azure lighthouse", "azure security center", "azure sentinel", "azure compliance",
    "azure trust center", "azure service trust portal", "azure governance", "azure management scope",
    "azure hierarchy", "azure tenant", "azure directory", "azure ad connect", "azure ad identity protection",
    "azure ad privileged identity management", "azure ad conditional access", "azure ad access reviews",
    "azure ad entitlement management", "azure ad terms of use", "azure ad b2b", "azure ad b2c",
    "azure ad domain services", "azure ad authentication", "azure ad authorization", "azure ad sso",
    "azure ad mfa", "azure ad self-service password reset", "azure ad identity secure score",
    "azure ad reporting", "azure ad auditing", "azure ad sign-in logs", "azure ad provisioning",
    "azure ad gallery applications", "azure ad app registrations", "azure ad enterprise applications",
    "azure ad managed identities", "azure ad certificates", "azure ad naming policy", "azure ad branding",
    "azure ad password protection", "azure ad identity governance", "azure ad access packages",
    "azure ad administrative units", "azure ad groups", "azure ad dynamic groups", "azure ad licenses",
    "azure ad hybrid identity", "azure ad connect health", "azure ad password writeback", "azure ad cloud sync",
    "azure policy initiatives", "azure policy exemptions", "azure policy compliance", "azure policy effects",
    "azure policy assignments", "azure policy definitions", "azure policy parameters", "azure policy remediation",
    "azure blueprints definition", "azure blueprints assignment", "azure blueprints versioning",
    "azure management api", "azure resource providers", "azure resource locks", "azure resource move",
    "azure resource export", "azure resource tagging", "azure resource naming", "azure resource organization",
    "azure cost allocation", "azure cost budgets", "azure cost alerts", "azure cost optimization",
    "azure cost forecasting", "azure cost recommendations", "azure billing", "azure invoices",
    "azure payment methods", "azure pricing calculator", "azure tco calculator", "azure reservations",
    "azure savings plans", "azure hybrid benefit", "azure free account", "azure support plans",
    "azure service level agreements", "azure preview features", "azure updates", "azure roadmap",
    "azure status", "azure security baselines", "azure security benchmarks", "azure defender for cloud",
    "azure network security groups", "azure ddos protection", "azure firewall", "azure private link",
    "azure vpn gateway", "azure expressroute", "azure bastion", "azure just-in-time vm access",
    "azure key vault", "azure information protection", "azure confidential computing", "azure backup",
    "azure site recovery", "azure update management", "azure automation", "azure logic apps",
    "azure event grid", "azure service bus", "azure queue storage", "azure api management",
    "azure devops", "azure pipelines", "azure boards", "azure repos", "azure artifacts",
    "azure test plans", "azure load testing", "azure dev center", "azure lab services",
    "azure mobile apps", "azure powerapps", "azure power automate", "azure power bi", "azure synapse",
    "azure purview", "azure data catalog", "azure data factory", "azure databricks", "azure machine learning"
]

# *********************************************************************************

class Question:
    def __init__(self, question, options, correct_answer, explanation=""):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.category = self.categorize_question()

    def categorize_question(self):
        # Process the question text
        doc = nlp(self.question.lower())
        
        # Count keyword matches for each category
        cloud_count = sum(1 for token in doc if any(keyword in token.text for keyword in cloud_concepts_keywords))
        architecture_count = sum(1 for token in doc if any(keyword in token.text for keyword in azure_architecture_keywords))
        management_count = sum(1 for token in doc if any(keyword in token.text for keyword in azure_management_keywords))

        # Determine the category based on keyword counts
        if cloud_count > architecture_count and cloud_count > management_count:
            return "Describe cloud concepts"
        elif architecture_count > cloud_count and architecture_count > management_count:
            return "Describe Azure architecture and services"
        else:
            return "Describe Azure management and governance"

class ExamSimulator:
    def __init__(self, csv_file, renderer, translator):
        self.renderer = renderer
        self.translator = translator
        self.curate_exam_file(csv_file)
        self.csv_file = csv_file
        self.questions = self.load_questions()
        self.score = 0
        self.total_questions = len(self.questions)
        self.category_scores = {
            "Describe cloud concepts": 0,
            "Describe Azure architecture and services": 0,
            "Describe Azure management and governance": 0
        }

    # =====================================================#

    # Execute translations asynchronously, concurrently & quasi-parallel runs - 
    # improving overall performance.
    async def translate_batch(self, texts):
        async with aiohttp.ClientSession() as session:
            tasks = [self.translator.translate(text) for text in texts]
            return await asyncio.gather(*tasks)

    def clear_screen(self):
        # For Windows
        if os.name == 'nt':
            _ = os.system('cls')
        # For Mac and Linux
        else:
            _ = os.system('clear')

    def curate_exam_file(self, csv_file):
        # Read the CSV file with semicolon delimiter
        df = pd.read_csv(csv_file, sep=';')
        df = df.astype(str)                     # Convert all columns to strings
        # Prepare a backup (just in case)
        df.to_csv(csv_file + '.bak', sep=';', index=False)
        # Replace ',' with ' ' and trim tabs/whitespaces in the 'long-text' columns
        columns_to_clean = ['Question', 'OptionA', 'OptionB', 'OptionC', 'OptionD', 'Explanation']
        for col in columns_to_clean:
            df[col] = df[col].str.replace(',', ' ').replace('[', ' ').replace(']', ' ').str.strip()

        # Save the updated CSV with semicolon delimiter
        df.to_csv(csv_file, sep=';', index=False)
        df.head()

    def load_questions(self):
        questions = []
        
        # Open relevant (chosen Azure cert. by user) CSV exam into Pandas dataframe
        df = pd.read_csv(self.csv_file, sep=';')
        
        # Prep. all questionaires for translation
        texts_to_translate = []
        for _, row in df.iterrows():
            texts_to_translate.extend([row['Question'], row['OptionA'], row['OptionB'], row['OptionC'], row['OptionD'], row['Explanation']])
        
        # Batch & Async translation
        # loop = asyncio.get_event_loop()
        # translated_texts = loop.run_until_complete(self.translate_batch(texts_to_translate))
        # Parallel translate
        translated_texts = self.parallel_translate(texts_to_translate)

        # Prep. translated self-assessment cert's questions
        for i in range(0, len(translated_texts), 6):
            question = translated_texts[i]                                  # CSV Schema-Column: Question;
            options = [f"A.{translated_texts[i+1]}",                        # CSV Schema-Column: OptionA;
                       f"B.{translated_texts[i+2]}",                        # CSV Schema-Column: OptionB;
                       f"C.{translated_texts[i+3]}",                        # CSV Schema-Column: OptionC;
                       f"D.{translated_texts[i+4]}",                        # CSV Schema-Column: OptionD;
                       "Q. Abort"]

            correct_answer = df.iloc[i//6]['CorrectAnswer']                 # CSV Schema-Column: CorrectAnswer;
            explanation = textwrap.fill(translated_texts[i+5], width=70)    # CSV Schema-Column: Explanation;
        
            # Take the translated self-assessment into memory, interactive mode for the user
            questions.append(Question(question,options,correct_answer,explanation))

        if not questions or questions.__len__() <= 0:
            print(self.renderer.WARNING + self.translator.translate("No questions were loaded from the CSV file.") + self.renderer.ENDC)
            sys.exit(1)
        
        return questions

    def run_exam(self):
        random.shuffle(self.questions)
        for i, question in enumerate(self.questions, 1):
            self.clear_screen()
            print(self.renderer.OKBLUE + self.translator.translate(f"Question #{i} of {self.total_questions}") + self.renderer.ENDC)
            print(self.renderer.UNDERLINE + question.question + self.renderer.ENDC)
            for option in question.options:
                print(option)
            
            user_answer = input(self.translator.translate("Your answer (A, B, C, D or Abort[Q]): ")).strip().upper()
            while user_answer not in ['A', 'B', 'C', 'D', 'Q']:
                user_answer = input(self.renderer.WARNING + self.translator.translate("Invalid input. Please enter A, B, C, or D: ") + self.renderer.ENDC).strip().upper()
            
            if user_answer == 'Q':
                print(self.renderer.WARNING + self.translator.translate("Exiting and aborting exam test ... See You Later!!") + self.renderer.ENDC)
                print(f"{self.renderer.WARNING}Printing score up to this point until the exam was aborted: ")
                self.show_results()
                quit()
            if user_answer == question.correct_answer:
                print(self.renderer.OKGREEN + self.translator.translate("\nCorrect!") + self.renderer.ENDC)
                self.score += 1
                self.category_scores[question.category] += 1
            else:
                print(self.renderer.WARNING + self.translator.translate(f"\nIncorrect. The correct answer is {question.correct_answer}.") + self.renderer.ENDC)
            
            if question.explanation:
                print(self.renderer.BOLD + self.translator.translate("Explanation: ") + self.renderer.ENDC + question.explanation)
            input(self.translator.translate("\nPress [Enter] to continue..."))

    def show_results(self):
        self.clear_screen()
        percentage = (self.score / self.total_questions) * 1000
        print(self.renderer.OKBLUE + self.translator.translate(f"Exam {self.renderer.BOLD}{cert_name}{self.renderer.ENDC} completed! Your score (Microsoft Notation - Max Score is 1000, Passing Score is 700): {self.score}/{self.total_questions} ({percentage:.2f}%)") + self.renderer.ENDC)
        if percentage >= 700:
            print(self.renderer.OKGREEN + self.translator.translate("Congratulations! You have passed the exam: ") + "" + f"{self.renderer.BOLD}{cert_name}" + "" + self.renderer.ENDC)
        else:
            print(self.renderer.FAIL + self.translator.translate("You did not pass the exam. Keep studying and try again the " + f"{self.renderer.BOLD}{cert_name}{self.renderer.ENDC}" + " exam, Good Luck next time, Mate!") + self.renderer.ENDC)
        print(f"\n{self.renderer.WARNING}Score breakdown by category:{self.renderer.ENDC}")
        self.display_category_scores()

    def display_category_scores(self):
        max_length = max(len(category) for category in self.category_scores.keys())
        for category, score in self.category_scores.items():
            category_score = (score / self.total_questions) * 1000
            bar_length = int(category_score / 20)  # Scale to 50 characters max in the ASCII-based bar chart
            bar = '█' * bar_length + '▒' * (50 - bar_length)
            print(f"{category.ljust(max_length)} : {bar} {category_score:.2f}")

    def tokenize_and_translate(self, text):
        if isinstance(text, float):
            print("[DEBUG] Received a float instead of a string. Converting to string.")
            text = str(text)  # or handle as you see fit
        try:
            tokens = word_tokenize(text)
            translated_tokens = [self.translator.translate(token) for token in tokens]
            return ' '.join(translated_tokens)
        except LookupError:
            return ' '.join([self.translator.translate(word) for word in text.split()])
        except Exception as e:
            print(f"Tokenization failed: {e}. Using original text.")
            return self.translator.translate(text)

    def parallel_translate(self, texts):
        with ThreadPoolExecutor() as executor:
            return list(executor.map(self.tokenize_and_translate, texts))

def main():
    global questions_input_file
    global cert_name
    global lang
    global translation_enabled

    renderer = FontColours()
    langs = Languages()

    print("Welcome to the ETC-CertTester Azure Exam Simulator!\n")
    print("Please choose your preferred language to take the test:")
    print(f"{renderer.OKCYAN}1. English{renderer.ENDC}")
    print(f"{renderer.OKCYAN}2. Español{renderer.ENDC}")
    print(f"{renderer.OKCYAN}3. Português{renderer.ENDC}")
    print(f"{renderer.OKCYAN}4. Français{renderer.ENDC}")
    print(f"{renderer.OKCYAN}5. 日本語{renderer.ENDC}")

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
        print("Invalid selection. Exiting...")
        sys.exit(1)

    langs.set_language(lang)  # Set the language and initialize translator if needed

    print(langs.translate("Please choose the Azure certification you want to practice:"))
    print(f"{renderer.BOLD}" + langs.translate("1. AZ-900: Microsoft Azure Fundamentals") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("2. AZ-104: Microsoft Azure Administrator") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("3. AZ-204: Developing Solutions for Microsoft Azure") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("4. AZ-305: Designing Microsoft Azure Infrastructure Solutions") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("5. AZ-400: Designing and Implementing Microsoft DevOps Solutions") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("6. AZ-500: Microsoft Azure Security Technologies") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("7. AZ-700: Designing and Implementing Microsoft Azure Networking Solutions") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("8. AZ-800: Administering Windows Server Hybrid Core Infrastructure") + f"{renderer.ENDC}")
    print(f"{renderer.BOLD}" + langs.translate("9. AZ-140: Configuring and Operating Microsoft Azure Virtual Desktop\n") + f"{renderer.ENDC}")

    choice = input(langs.translate("Enter the number corresponding to your certification: ")).strip()

    if choice == '1':
        questions_input_file = 'az900_questions.csv'
        cert_name = "AZ-900: Microsoft Azure Fundamentals"
    elif choice == '2':
        cert_name = "AZ-104: Microsoft Azure Administrator"
        questions_input_file = 'az104_questions.csv'
    elif choice == '3':
        cert_name = "AZ-204: Developing Solutions for Microsoft Azure"
        questions_input_file = 'az204_questions.csv'
    elif choice == '4':
        cert_name = "AZ-305: Designing Microsoft Azure Infrastructure Solutions"
        questions_input_file = 'az305_questions.csv'
    elif choice == '5':
        questions_input_file = 'az400_questions.csv'
        cert_name = "AZ-400: Designing and Implementing Microsoft DevOps Solutions"
    elif choice == '6':
        questions_input_file = 'az500_questions.csv'
        cert_name = "AZ-500: Microsoft Azure Security Technologies"
    elif choice == '7':
        questions_input_file = 'az700_questions.csv'
        cert_name = "AZ-700: Designing and Implementing Microsoft Azure Networking Solutions"
    elif choice == '8':
        questions_input_file = 'az800_questions.csv'
        cert_name = "AZ-800: Administering Windows Server Hybrid Core Infrastructure"
    elif choice == '9':
        questions_input_file = 'az140_questions.csv'
        cert_name = "AZ-140: Configuring and Operating Microsoft Azure Virtual Desktop"
    else:
        print("Invalid selection. Exiting...")
        sys.exit(1)

    try:
        end_it = False 

        while end_it == False:
            simulator = ExamSimulator(questions_input_file, renderer, langs)
        
            print(f"{simulator.renderer.HEADER}" + langs.translate(f"Welcome to the {cert_name} Exam Simulator! -Copyright Vinicio S. Flores <v.flores.hernandez@accenture.com>") + f"{simulator.renderer.ENDC}")
            input(f"{simulator.renderer.BOLD}" + langs.translate(f"Press Enter to start the exam...") + f"{simulator.renderer.ENDC}")
        
            simulator.run_exam()
            simulator.show_results()

            continue_input = 'X'

            while continue_input not in ['Y','N']:
                continue_input = input(f"{simulator.renderer.BOLD}Wanna try again another or same certification exam? (y/N) {simulator.renderer.ENDC}")
                continue_input = continue_input.strip().upper();

                if(continue_input == 'Y'):
                    end_it = False
                elif (continue_input == 'N'):
                    end_it = True
                    break;
                else:
                    print("Invalid answer, answer 'Y' or 'N'")

    except Exception as e:
        print(f"{renderer.FAIL}An error occurred: {e}{renderer.ENDC}")
        print("Please try again. If the problem persists, check your internet connection and make sure you have the necessary permissions to download NLTK data.")

if __name__ == "__main__":
    main()