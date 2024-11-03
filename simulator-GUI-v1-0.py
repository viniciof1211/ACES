from pydoc import render_doc
import sys
import os
import random
import json
import csv
import nltk
import spacy
from googletrans import Translator
from functools import lru_cache
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget, QRadioButton, QButtonGroup, QMessageBox, QProgressBar, QScrollArea,QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCharts import QChart, QChartView, QBarSet, QStackedBarSeries, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPainter, QFont
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon

print("[DEBUG] Loading initial and background modules ... Please wait ....")


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

global renderer
renderer = FontColours()

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

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class Languages:
    def __init__(self):
        self.ENGLISH = 'en'
        self.SPANISH = 'es'
        self.PORTUGUESE = 'pt'
        self.FRENCH = 'fr'
        self.JAPANESE = 'ja'
        self.HEBREW = 'he'
        self.needs_translation = True
        self.translator = None

    def set_language(self, lang):
        self.needs_translation = (lang != self.ENGLISH)
        if self.needs_translation:
            self.translator = Translator()
        else:
            self.translator = None

    @lru_cache(maxsize=2048)
    def translate(self, text):
        if self.needs_translation and self.translator:
            try:
                return self.translator.translate(text, dest=self.current_lang).text
            except Exception as e:
                print(f"Translation error: {e}")
                return text
        return text

class Question:
    def __init__(self, question, options, correct_answer, explanation=""):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.category = None

import json
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QLinearGradient

class StreakFlame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 40)
        self.streak_count = 0
        self.flame_height = 0.0
        self.flame_opacity = 0.8
        self.load_streak_data()
        
        # Animation setup
        self.animation = QPropertyAnimation(self, b"flame_height")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setLoopCount(-1)
        self.animation.start()
        
        # Timer for updating streak status
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_streak)
        self.check_timer.start(3600000)  # Check every hour
        
        self.streak_label = QLabel(str(self.streak_count), self)
        self.streak_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.streak_label.setStyleSheet("color: white; font-weight: bold;")
        self.streak_label.move(8, 12)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create flame path
        path = QPainterPath()
        width = self.width()
        height = self.height()
        
        # Animate flame
        flame_mod = abs(self.flame_height - 0.5) * 4
        
        # Base points
        path.moveTo(width/2, height)
        path.cubicTo(
            width * 0.2, height * 0.8,
            width * (0.3 + flame_mod * 0.1), height * 0.5,
            width/2, height * (0.3 + flame_mod * 0.1)
        )
        path.cubicTo(
            width * (0.7 - flame_mod * 0.1), height * 0.5,
            width * 0.8, height * 0.8,
            width/2, height
        )

        # Create gradient
        gradient = QLinearGradient(QPointF(width/2, 0), QPointF(width/2, height))
        gradient.setColorAt(0.0, QColor(255, 140, 0, int(255 * self.flame_opacity)))
        gradient.setColorAt(0.5, QColor(255, 69, 0, int(255 * self.flame_opacity)))
        gradient.setColorAt(1.0, QColor(255, 0, 0, int(255 * self.flame_opacity)))

        # Draw flame
        painter.fillPath(path, gradient)

    def load_streak_data(self):
        try:
            if os.path.exists('streak_data.json'):
                with open('streak_data.json', 'r') as f:
                    data = json.load(f)
                    self.streak_count = data.get('streak', 0)
                    last_practice = datetime.fromisoformat(data.get('last_practice'))
                    
                    # Check if streak is still valid
                    today = datetime.now().date()
                    if (today - last_practice.date()).days > 1:
                        self.streak_count = 0
            else:
                self.streak_count = 0
        except Exception as e:
            print(f"Error loading streak data: {e}")
            self.streak_count = 0

    def save_streak_data(self):
        data = {
            'streak': self.streak_count,
            'last_practice': datetime.now().isoformat()
        }
        try:
            with open('streak_data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving streak data: {e}")

    def check_streak(self):
        today = datetime.now().date()
        try:
            with open('streak_data.json', 'r') as f:
                data = json.load(f)
                last_practice = datetime.fromisoformat(data.get('last_practice')).date()
                
                if (today - last_practice).days > 1:
                    self.streak_count = 0
                    self.save_streak_data()
                    self.streak_label.setText(str(self.streak_count))
        except Exception:
            pass

    def update_streak(self):
        today = datetime.now().date()
        try:
            if os.path.exists('streak_data.json'):
                with open('streak_data.json', 'r') as f:
                    data = json.load(f)
                    last_practice = datetime.fromisoformat(data.get('last_practice')).date()
                    
                    if last_practice < today:
                        if (today - last_practice).days == 1:
                            self.streak_count += 1
                        else:
                            self.streak_count = 1
                        self.save_streak_data()
            else:
                self.streak_count = 1
                self.save_streak_data()
                
            self.streak_label.setText(str(self.streak_count))
        except Exception as e:
            print(f"Error updating streak: {e}")


class ExamSimulatorGUI(QMainWindow):
    def __init__(self):
        # Debug message for init start
        print("[DEBUG] Initializing ExamSimulatorGUI...", file=sys.stderr)
        super().__init__()
        # Debug message before loading spaCy model
        print("Loading spaCy model 'en_core_web_sm'...", file=sys.stderr)
        self.nlp = spacy.load("en_core_web_sm")
        print("[DEBUG] spaCy model loaded successfully.", file=sys.stderr)
        # Debug message for initializing attributes
        print("[DEBUG] Initializing attributes...", file=sys.stderr)
        self.langs = Languages()
        self.questions = []
        self.current_question = 0
        self.score = 0
        # Debug message for initializing category_scores and certification_data
        print("[DEBUG] Initializing category_scores and certification_data...", file=sys.stderr)
        # Initialize category_scores as a dictionary with proper structure
        self.category_scores = {}
        self.certification_data = {}
        # Debug message before loading certification data
        print("[DEBUG] Loading certification data...", file=sys.stderr)
        self.load_certification_data()
        print("[DEBUG] Certification data loaded successfully.", file=sys.stderr)
        # Initialize components
        print("[DEBUG] Initializing UI components...", file=sys.stderr)
        self.results_title = QLabel()
        self.score_label = QLabel()
        self.certification_title = QLabel()
        self.chart_view = None
        self.cert_name = ""
        self.streak_flame = None  # Will be initialized when creating exam screen
        # Create UI elements
        # Debug message before creating the UI
        print("[DEBUG] Initializing UI elements...", file=sys.stderr)
        self.exam_in_progress = False
        self.init_ui()
        print("UI initialization complete.", file=sys.stderr)

        # Debug message for init end
        print(f"{renderer.OKGREEN}ExamSimulatorGUI initialization complete.{renderer.ENDC}", file=sys.stderr)


    def init_results_ui(self, layout):
        # Configure title and score labels
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.results_title.setFont(title_font)
        
        score_font = QFont()
        score_font.setPointSize(12)
        self.score_label.setFont(score_font)
        
        layout.addWidget(self.results_title)
        layout.addWidget(self.score_label)

    def init_ui(self):
        self.setWindowTitle('Microsoft/ETC Certification Exams Simulator')
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon('logo.jpg'))

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        print("[DEBUG] Central widget object created")

        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        print("[DEBUG] Central widget object created")

        # Create different screens
        self.create_language_screen()
        print("[DEBUG] Central Language Screen created")
        self.create_certification_screen()
        print("[DEBUG] Certifications Menu Screen created")
        self.create_exam_screen()
        print("[DEBUG] Exam Screen created")
        self.create_results_screen()
        print("[DEBUG] Results Screen created")

    def create_language_screen(self):
        language_widget = QWidget()
        layout = QVBoxLayout(language_widget)

        # Title
        title = QLabel("Select Your Language")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Language buttons
        languages = [
            ("English", self.langs.ENGLISH),
            ("Español", self.langs.SPANISH),
            ("Português", self.langs.PORTUGUESE),
            ("Français", self.langs.FRENCH),
            ("日本語", self.langs.JAPANESE),
            ("עִברִית", self.langs.HEBREW)
        ]

        for lang_name, lang_code in languages:
            btn = QPushButton(lang_name)
            btn.clicked.connect(lambda checked, code=lang_code: self.select_language(code))
            layout.addWidget(btn)

        self.stacked_widget.addWidget(language_widget)

    def create_certification_screen(self):
        cert_widget = QWidget()
        layout = QVBoxLayout(cert_widget)

        title = QLabel("Select Certification Exam")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(title)

        self.cert_combo = QComboBox()
        self.cert_combo.addItems([
            "AZ-900: Microsoft Azure Fundamentals",
            "AZ-104: Microsoft Azure Administrator",
            "AZ-204: Developing Solutions for Microsoft Azure",
            "AZ-305: Designing Microsoft Azure Infrastructure Solutions",
            "AZ-400: Designing and Implementing Microsoft DevOps Solutions",
            "AZ-500: Microsoft Azure Security Technologies",
            "AZ-700: Designing and Implementing Microsoft Azure Networking Solutions",
            "AZ-800: Administering Windows Server Hybrid Core Infrastructure",
            "AZ-140: Configuring and Operating Microsoft Azure Virtual Desktop",
            "MS-900: Microsoft 365 Certified: Fundamentals",
            "PL-900: Microsoft Certified: Power Platform Fundamentals",
            "SC-900: Microsoft Security, Compliance, and Identity Fundamentals"
        ])
        layout.addWidget(self.cert_combo)

        start_btn = QPushButton("Start Exam")
        start_btn.clicked.connect(self.start_exam)
        layout.addWidget(start_btn)

        self.stacked_widget.addWidget(cert_widget)       

    def initialize_category_scores(self):
        # Reset category scores at the start of each exam
        self.category_scores = {}
        # Get categories for the current certification
        categories = self.get_certification_categories()
        # Initialize scores for each category
        for category in categories:
            self.category_scores[category] = {
                'correct': 0,
                'total': 0,
                'questions': []
            }

        if not categories:
            print(f"Warning: No categories found for certification {self.cert_name}")
            return {f"Uncategorized - Warning: No categories found for certification {self.cert_name}": 0}
        return {category: 0 for category in categories}

    def categorize_question(self, question_text):
        """
        Improved question categorization with better error handling
        """
        try:
            categories = self.get_certification_categories()
            if not categories or categories == ["Uncategorized"]:
                return "Uncategorized"

            doc = self.nlp(question_text.lower())
        
            # Initialize a dictionary to store keyword match counts for each category
            category_keyword_counts = {}
        
            # Find the certification in the data
            cert_found = False
            for cert in self.certification_data.get("certifications", []):
                if cert['certification'] == self.cert_name:
                    cert_found = True
                    # Count keyword matches for each category
                    for category in cert.get('categories', []):
                        category_name = category.get('category', '').strip()
                        keywords = category.get('keywords', [])
                        count = sum(1 for token in doc if any(keyword.lower() in token.text for keyword in keywords))
                        category_keyword_counts[category_name] = count

            if not cert_found or not category_keyword_counts:
                return "General Questions"

            # Find the category with the highest keyword match count
            best_category = max(category_keyword_counts.items(), key=lambda x: x[1])[0]
            return best_category if best_category else "General Questions"

        except Exception as e:
            print(f"Error in categorize_question: {e}")
            return "General Questions"

    def get_certification_categories(self):
        """
        Improved certification categories retrieval with error handling
        """
        try:
            if not self.certification_data:
                print("Warning: Certification data not loaded.")
                return ["General Questions"]

            certification = next(
                (cert for cert in self.certification_data.get("certifications", [])
                 if cert["certification"] == self.cert_name),
                None
            )

            if certification:
                categories = [cat["category"].strip() for cat in certification.get("categories", [])
                             if "category" in cat and cat["category"].strip()]
                return categories if categories else ["General Questions"]
        
            print(f"Warning: Certification {self.cert_name} not found in the JSON data.")
            return ["General Questions"]
    
        except Exception as e:
            print(f"Error in get_certification_categories: {e}")
            return ["General Questions"]

    def analyze_nlp_for_category(self, category_name):
        certification = next((cert for cert in self.certification_data["certifications"] 
                              if cert["certification"] == self.cert_name), None)
        if certification:
            category = next((cat for cat in certification["categories"] 
                             if cat["category"] == category_name), None)
            if category:
                return category.get("keywords", [])
        return None

    def create_exam_screen(self):
        exam_widget = QWidget()
        layout = QVBoxLayout(exam_widget)

        # Certification Title + Microsoft Code
        self.certification_title = QLabel()
        self.certification_title.setWordWrap(False)
        self.certification_title.setFont(QFont('Times New Roman', 24, QFont.Weight.Bold))
        self.certification_title.setText(self.cert_name)
        self.certification_title

        # Question number and progress
        self.progress_layout = QHBoxLayout()
        self.question_number_label = QLabel()
        self.progress_bar = QProgressBar()
        self.streak_flame = StreakFlame()
        self.progress_layout.addWidget(self.certification_title)
        self.progress_layout.addWidget(self.question_number_label)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.streak_flame)
        layout.addLayout(self.progress_layout)

        # Question text
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.question_label)

        # Answer options
        self.answer_group = QButtonGroup()
        self.answer_buttons = []
        for i in range(4):
            radio = QRadioButton()
            self.answer_buttons.append(radio)
            self.answer_group.addButton(radio, i)
            layout.addWidget(radio)

        # Submit button
        self.submit_btn = QPushButton("Submit Answer")
        self.submit_btn.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_btn)

        # Next Question (advance) button
        self.next_btn = QPushButton("Next >>")
        self.next_btn.clicked.connect(self.next_question)
        layout.addWidget(self.next_btn)

         # Abort button
        self.quit_btn = QPushButton("Abort Test")
        self.quit_btn.clicked.connect(self.confirm_abort)  # Connect directly to confirm & abort method
        layout.addWidget(self.quit_btn)

        # Explanation area
        self.explanation_label = QLabel()
        self.explanation_label.setWordWrap(True)
        self.explanation_label.hide()
        layout.addWidget(self.explanation_label)

        self.stacked_widget.addWidget(exam_widget)

    def abort_simulator(self):
        self.abort_count(30)
        sys.exit(0)

    def create_results_screen(self):
        self.results_widget = QWidget()
        layout = QVBoxLayout(self.results_widget)

        print("[DEBUG] Results Box Layout created")

        # Scrollable area for results
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        print("[DEBUG] Results Scroll Area & Content Widget created")

        # Initialize results UI with the correct layout
        self.init_results_ui(scroll_layout)

        # Results title
        self.results_title = QLabel()
        self.results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        scroll_layout.addWidget(self.results_title)

        print("[DEBUG] Results Title created")

        # Score label
        self.score_label = QLabel()
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(self.score_label)

        print("[DEBUG] Score label created")

        # Chart container
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        scroll_layout.addWidget(self.chart_container)

        print("[DEBUG] Chart container created")

        # Category details
        self.category_details = QLabel()
        self.category_details.setWordWrap(True)
        scroll_layout.addWidget(self.category_details)

        print("[DEBUG] Category Details created")

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Buttons
        btn_layout = QHBoxLayout()
        retry_btn = QPushButton("Try Again")
        retry_btn.clicked.connect(self.restart_exam)
        new_exam_btn = QPushButton("New Exam")
        new_exam_btn.clicked.connect(self.select_new_exam)
        quit_btn = QPushButton("Terminate exam")
        quit_btn.clicked.connect(self.abort_simulator)
        btn_layout.addWidget(retry_btn)
        btn_layout.addWidget(new_exam_btn)
        btn_layout.addWidget(quit_btn)
        layout.addLayout(btn_layout)

        print("[DEBUG] Buttons control panel created")

        self.stacked_widget.addWidget(self.results_widget)

    def load_certification_data(self):
        try:
            with open('scoring.json', 'r') as f:
                self.certification_data = json.load(f)
        except Exception as e:
            print(f"Error loading certification data: {e}")
            self.certification_data = {}

    def select_language(self, lang_code):
        self.langs.set_language(lang_code)
        self.langs.current_lang = lang_code
        self.stacked_widget.setCurrentIndex(1)

    def start_exam(self):
        self.cert_name = self.cert_combo.currentText()
        csv_file = f"{self.cert_name.split(':')[0].lower()}_questions.csv"

        # Update streak when starting a new exam
        if self.streak_flame:
            self.streak_flame.update_streak()

        try:
            self.load_questions(csv_file)
            # Initialize category scores when starting exam
            self.initialize_category_scores()
            self.current_question = 0
            self.score = 0
            self.exam_in_progress = True
            self.show_question()
            self.stacked_widget.setCurrentIndex(2)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load exam questions: {e}")

    def load_questions(self, csv_file):
        self.questions = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                next(reader)  # Skip header
                for row in reader:
                    question = Question(
                        question=row[0],
                        options=[row[1], row[2], row[3], row[4]],
                        correct_answer=row[5],
                        explanation=row[6]
                    )
                    self.questions.append(question)
            random.shuffle(self.questions)
        except Exception as e:
            raise Exception(f"Error loading questions: {e}")

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            
            # Update progress bar according to # total question of cert's assessment
            self.question_number_label.setText(f"Question {self.current_question + 1}/{len(self.questions)}")
            self.progress_bar.setValue(int((self.current_question / len(self.questions)) * 100))

            # Show question
            self.question_label.setText(self.langs.translate(question.question))
            
            # Show options
            for i, option in enumerate(question.options):
                self.answer_buttons[i].setText(self.langs.translate(option))

            # Reset state
            self.answer_group.setExclusive(True)
            for button in self.answer_buttons:
                button.setChecked(False)
            self.explanation_label.hide()
            self.submit_btn.setEnabled(True)
            self.quit_btn.setEnabled(True)

            # If we reach the end of the exam ... no need to display "Next question" Button

            if self.current_question >= len(self.questions):
                self.next_btn.setEnabled(False)
                self.next_btn.hide()
            else:
                self.next_btn.setEnabled(True)
                self.next_btn.show()

    def check_answer(self):
        if not self.answer_group.checkedButton():
            QMessageBox.warning(self, "Warning", "Please select an answer")
            return

        question = self.questions[self.current_question]
        selected_answer = chr(65 + self.answer_group.checkedId())  # Convert to A, B, C, D
    
        # Store the user's answer in the question object
        question.user_answer = selected_answer
    
        is_correct = selected_answer == question.correct_answer
        if is_correct:
            self.score += 1
            result_text = "Correct!"
            color = "green"
        else:
            result_text = f"Incorrect. The correct answer was {question.correct_answer}."
            color = "red"

        self.explanation_label.setText(
            f"<p style='color: {color}'>{result_text}</p>"
            f"<p><b>Explanation:</b> {self.langs.translate(question.explanation)}</p>"
        )
        self.explanation_label.show()
        self.submit_btn.setEnabled(False)

        # Wait 60 seconds before moving to next question - if user hasn't clicked "next >>" btn
        # QTimer.singleShot(60000, self.next_question)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def restart_exam(self):
        self.current_question = 0
        self.score = 0
        random.shuffle(self.questions)
        self.show_question()
        self.stacked_widget.setCurrentIndex(2)

    def select_new_exam(self):
        self.stacked_widget.setCurrentIndex(1)

    def clear_chart_layout(self):
        # Safely clear all widgets from the chart layout
        if hasattr(self, 'chart_layout'):
            while self.chart_layout.count():
                item = self.chart_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()


    def get_certification_scores(self, cert_name):
        # Extract relevant categories and their scores based on the certification
        cert_data = self.certification_data.get(cert_name, {})
        cert_categories = cert_data.get("categories", [])
    
        # Create a dictionary to hold correct/incorrect answers per category
        cert_scores = {}
        for category in cert_categories:
            category_name = category.get("name", "Unknown Category")
            correct = category.get("correct", 0)
            incorrect = category.get("incorrect", 0)
            cert_scores[category_name] = {"correct": correct, "incorrect": incorrect}
    
        return cert_scores

    
    def show_results(self):
        # Update streak when completing an exam
        if self.streak_flame:
            self.streak_flame.update_streak()
        # Calculate overall score
        percentage = (self.score / len(self.questions)) * 1000
        passed = percentage >= 700

        # Update title and score
        self.results_title.setText("Exam Results")
        self.score_label.setText(
            f"Final Score: {self.score}/{len(self.questions)} ({percentage:.2f}/1000)\n"
            f"{'PASS' if passed else 'FAIL'}"
        )

        # Initialize category tracking with proper error handling
        categories_data = {}
    
        # Process questions and track results by category
        for question in self.questions[:self.current_question + 1]:
            try:
                category = self.categorize_question(question.question)
                category = category.strip()  # Remove any leading/trailing whitespace
            
                # Initialize category if it doesn't exist
                if category not in categories_data:
                    categories_data[category] = {
                        'correct': 0,
                        'incorrect': 0,
                        'total': 0,
                        'questions': []
                    }
            
                categories_data[category]['total'] += 1
            
                # Track question result if user answered
                if hasattr(question, 'user_answer'):
                    is_correct = question.user_answer == question.correct_answer
                    if is_correct:
                        categories_data[category]['correct'] += 1
                    else:
                        categories_data[category]['incorrect'] += 1
                
                    # Store question details
                    categories_data[category]['questions'].append({
                        'question': question.question,
                        'correct': is_correct,
                        'user_answer': question.user_answer,
                        'correct_answer': question.correct_answer
                    })
            except Exception as e:
                print(f"Error processing question category: {e}")
                # Use a fallback category if categorization fails
                fallback_category = "General Questions"
                if fallback_category not in categories_data:
                    categories_data[fallback_category] = {
                        'correct': 0,
                        'incorrect': 0,
                        'total': 0,
                        'questions': []
                    }
                categories_data[fallback_category]['total'] += 1

        # Clear previous chart
        self.clear_chart_layout()

        # Create and display category chart
        self.create_category_chart(self.category_scores, categories_data)

        # Generate detailed breakdown text
        details_text = "<h3>Detailed Category Breakdown:</h3>"
        for category, data in categories_data.items():
            total = data['total']
            correct = data.get('correct', 0)  # Use get() with default value
            if total > 0:
                percentage = (correct / total) * 100
                details_text += f"<p><b>{category}</b>: {correct}/{total} ({percentage:.1f}%)</p>"
                # Add question details if available
                if 'questions' in data:
                    for q in data['questions']:
                        status = "✓" if q['correct'] else "✗"
                        details_text += f"<p style='margin-left: 20px;'>{status} {q['question']}</p>"

        self.category_details.setText(details_text)

        # Switch to results screen
        self.stacked_widget.setCurrentIndex(3)

    """Create and display the category performance chart"""
    def create_category_chart(self, category_scores, categories_data):
        # Safety check for empty data
        if not categories_data:
            print("Warning: No category data available")
            return

        # Create chart
        chart = QChart()
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setTitle("Category Performance Breakdown")

        # Create bar sets
        correct_set = QBarSet("Correct")
        incorrect_set = QBarSet("Incorrect")
        correct_set.setColor(QColor("#2ecc71"))  # Green
        incorrect_set.setColor(QColor("#e74c3c"))  # Red

        # Get categories from scoring.json for the current certification
        cert_categories = []
        try:
            for cert in self.certification_data.get("certifications", []):
                if cert["certification"] == self.cert_name:
                    cert_categories = [cat["category"] for cat in cert.get("categories", [])]
                    break
        except Exception as e:
            print(f"Error retrieving categories from scoring.json: {e}")
            cert_categories = list(categories_data.keys())  # Fallback to existing categories

        # If no categories found in scoring.json, use existing categories
        if not cert_categories:
            cert_categories = list(categories_data.keys())

        # Initialize data for all categories
        category_results = {cat: {'correct': 0, 'incorrect': 0} for cat in cert_categories}

        # Process questions and assign to proper categories
        for category in cert_categories:
            if category in categories_data:
                category_results[category]['correct'] = categories_data[category]['correct']
                category_results[category]['incorrect'] = (
                    categories_data[category]['total'] - categories_data[category]['correct']
                )

        # Add data to bar sets in the order of cert_categories
        for category in cert_categories:
            correct_set.append(float(category_results[category]['correct']))
            incorrect_set.append(float(category_results[category]['incorrect']))

        # Create stacked bar series
        series = QStackedBarSeries()
        series.append(correct_set)
        series.append(incorrect_set)
        chart.addSeries(series)

        # Setup axes
        axis_x = QBarCategoryAxis()
        axis_x.append(cert_categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        axis_x.setLabelsAngle(-45)  # Angle the labels for better readability
        axis_x.setTruncateLabels(False)

        # Setup y-axis with proper range
        max_total = max([
            category_results[cat]['correct'] + category_results[cat]['incorrect']
            for cat in cert_categories
        ])
        axis_y = QValueAxis()
        axis_y.setRange(0, max_total + 1)
        axis_y.setTitleText("Number of Questions")
        axis_y.setLabelFormat("%d")  # Use integer format
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Customize appearance
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Create and setup chart view with fixed size
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMinimumHeight(1024)
        self.chart_view.setMinimumWidth(748)

        # Add to layout
        self.chart_layout.addWidget(self.chart_view)

    def get_category_details(self, category_scores):
        details = []
        for category, stats in category_scores.items():
            percentage = (stats['correct'] / stats['total']) * 100
            details.append(f"{category}:")
            details.append(f"  Correct: {stats['correct']}/{stats['total']} ({percentage:.1f}%)")
            if 'questions' in stats:
                details.append("  Questions:")
                for q in stats['questions']:
                    status = "✓" if q['correct'] else "✗"
                    details.append(f"    {status} {q['question']}")
            details.append("")
        return "\n".join(details)

    def abort_count(self, seconds):
        i = seconds*1000
        while i >= 0:
            print(f"{renderer.FAIL}[WARNING] Abortion in 0.{i} miliseconds ...{renderer.ENDC}")
            i -= 1

    """Show confirmation dialog before aborting the exam"""
    def confirm_abort(self):
        reply = QMessageBox.question(
            self, 
            'Confirm Abort',
            'Are you sure you want to abort the exam? This will end the exam and show your current results.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Mark remaining questions as incorrect or unanswered
            for i in range(self.current_question, len(self.questions)):
                self.questions[i].user_answer = None
                print(f"{renderer.FAIL} Question not answered: [{i}]{self.questions[i]} {renderer.ENDC}")
            print(f"{renderer.WARNING}[ABORT] Loading partial results breakdown widget ... {renderer.ENDC}")
            self.show_results()

            # quit_btn = QPushButton("Terminate exam")
            # quit_btn.clicked.connect(self.confirm_abort)
            # self.chart_layout.addWidget();
            # Show results for 30 seconds, then quit app
            # QTimer.singleShot(30000, self.abort_count(30))

#############################################################################
############## MAIN ENTRY POINT #############################################
#############################################################################

if __name__ == '__main__':


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

    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon('logo.jpg'))
    
    # Create dark palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    
    app.setPalette(dark_palette)
    
    window = ExamSimulatorGUI()
    window.show()
    sys.exit(app.exec())