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
from PyQt6.QtGui import QPainter, QFont
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

class ExamSimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        # Initialize attributes before creating UI
        self.langs = Languages()
        self.questions = []
        self.current_question = 0
        self.score = 0
        # Initialize category_scores as a dictionary with proper structure
        self.category_scores = {}
        # Initialize components
        self.results_title = QLabel()
        self.score_label = QLabel()
        self.certification_title = QLabel()
        self.chart_view = None
        self.cert_name = ""
        # Create UI elements
        self.load_certification_data()
        self.exam_in_progress = False
        self.init_ui()

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

        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create different screens
        self.create_language_screen()
        self.create_certification_screen()
        self.create_exam_screen()
        self.create_results_screen()

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
        categories = self.get_certification_categories()
        if not categories or categories == ["Uncategorized"]:
            return "Uncategorized - no categories found."
        doc = self.nlp(question_text.lower())
        # Initialize a dictionary to store keyword match counts for each category
        category_keyword_counts = {}
        # Iterate over all categories loaded for the current certification
        for cert in self.certification_data["certifications"]:
            if cert['certification'] == self.cert_name:
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
                              if cert["certification"] == self.cert_name), None)
        if certification:
            categories = [cat["category"] for cat in certification.get("categories", [])]
            if not categories:
                # print(f"Warning: No categories found for certification {self.cert_name}")
                return [f"Uncategorized: No categories found for certification {self.cert_name}"]
            return categories
        print(f"Error: Certification {self.cert_name} not found in the JSON data.")
        return [f"Uncategorized - Error: Certification {self.cert_name} not found in the JSON data."]

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
        self.progress_layout.addWidget(self.certification_title)
        self.progress_layout.addWidget(self.question_number_label)
        self.progress_layout.addWidget(self.progress_bar)
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

    def create_results_screen(self):
        self.results_widget = QWidget()
        layout = QVBoxLayout(self.results_widget)

        # Scrollable area for results
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Initialize results UI with the correct layout
        self.init_results_ui(scroll_layout)

        # Results title
        self.results_title = QLabel()
        self.results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        scroll_layout.addWidget(self.results_title)

        # Score label
        self.score_label = QLabel()
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(self.score_label)

        # Chart container
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        scroll_layout.addWidget(self.chart_container)

        # Category details
        self.category_details = QLabel()
        self.category_details.setWordWrap(True)
        scroll_layout.addWidget(self.category_details)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Buttons
        btn_layout = QHBoxLayout()
        retry_btn = QPushButton("Try Again")
        retry_btn.clicked.connect(self.restart_exam)
        new_exam_btn = QPushButton("New Exam")
        new_exam_btn.clicked.connect(self.select_new_exam)
        quit_btn = QPushButton("Terminate exam")
        quit_btn.clicked.connect(self.confirm_abort)
        btn_layout.addWidget(retry_btn)
        btn_layout.addWidget(new_exam_btn)
        btn_layout.addWidget(quit_btn)
        layout.addLayout(btn_layout)

        self.stacked_widget.addWidget(self.results_widget)

    def load_certification_data(self):
        try:
            with open('scoring.json', 'r') as f:
                self.certification_data = json.load(f)
        except Exception as e:
            print(f"Error loading certification data: {e}")
            self.certification_data = None

    def select_language(self, lang_code):
        self.langs.set_language(lang_code)
        self.langs.current_lang = lang_code
        self.stacked_widget.setCurrentIndex(1)

    def start_exam(self):
        self.cert_name = self.cert_combo.currentText()
        csv_file = f"{self.cert_name.split(':')[0].lower()}_questions.csv"

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

        # Determine the question's category
        category = self.categorize_question(question.question)
        
        # Ensure category exists in scores
        if category not in self.category_scores:
            self.category_scores[category] = {
                'correct': 0,
                'total': 0,
                'questions': []
            }

        # Update category scores
        self.category_scores[category]['total'] += 1
        if selected_answer == question.correct_answer:
            self.score += 1
            self.category_scores[category]['correct'] += 1
            result_text = f"Correct!"
            color = "green"
        else:
            result_text = f"Incorrect. The correct answer was {question.correct_answer}."
            color = "red"

        # Store question details
        self.category_scores[category]['questions'].append({
            'question': question.question,
            'correct': selected_answer == question.correct_answer
        })

        self.explanation_label.setText(
            f"<p style='color: {color}'>{result_text}</p>"
            f"<p><b>Explanation:</b> {self.langs.translate(question.explanation)}</p>"
        )
        self.explanation_label.show()
        self.submit_btn.setEnabled(False)
        self.quit_btn.setEnabled(True)

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

    def show_results(self):
        # Calculate overall score
        percentage = (self.score / len(self.questions)) * 1000 # Microsoft/OnVue scoring system
        passed = percentage >= 700
    
        # Update title and overall score
        self.results_title.setText("Exam Results")
        self.score_label.setText(
            f"Final Score: {self.score}/{len(self.questions)} ({percentage:.2f}/1000)\n"
            f"{'PASS' if percentage >= 700 else 'FAIL'}"
        )

        # Create and display the stacked chart
        self.create_category_chart(self.category_scores)

        # Clear previous chart if exists
        for i in reversed(range(self.chart_layout.count())): 
            self.chart_layout.itemAt(i).widget().setParent(None)

        # Create category breakdown
        category_scores = {}
        category_totals = {}
        category_details = {}

        for question in self.questions:
            category = question.category
            if category not in category_scores:
                category_scores[category] = {'correct': 0, 'incorrect': 0}
                category_totals[category] = 0
                category_details[category] = []

            category_totals[category] += 1
            if hasattr(question, 'user_answer'):
                if question.user_answer == question.correct_answer:
                    category_scores[category]['correct'] += 1
                else:
                    category_scores[category]['incorrect'] += 1

        # Create chart
        chart = QChart()
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setTitle("Performance by Category")

        # Create bar sets
        correct_set = QBarSet("Correct")
        incorrect_set = QBarSet("Incorrect")
    
        # Set colors
        correct_set.setColor(QColor("#2ecc71"))  # Green
        incorrect_set.setColor(QColor("#e74c3c"))  # Red

        categories = []
        for category in category_scores:
            categories.append(category)
            correct_set.append(category_scores[category]['correct'])
            incorrect_set.append(category_scores[category]['incorrect'])

        # Create series
        series = QStackedBarSeries()
        series.append(correct_set)
        series.append(incorrect_set)
        chart.addSeries(series)

        # Create axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, max([sum(cat.values()) for cat in category_scores.values()]))
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(400)
        self.chart_layout.addWidget(chart_view)

        # Generate detailed text breakdown
        details_text = "<h3>Detailed Category Breakdown:</h3>"
        for category in category_scores:
            correct = category_scores[category]['correct']
            total = category_totals[category]
            cat_percentage = (correct / total) * 100 if total > 0 else 0
            details_text += f"<p><b>{category}</b>: {correct}/{total} ({cat_percentage:.1f}%)</p>"

        self.category_details.setText(details_text)
    
        # Switch to results screen
        self.stacked_widget.setCurrentIndex(3)

        """Create and display the category performance chart"""
    def create_category_chart(self, category_scores):
        # Safety check for empty category scores
        if not category_scores:
            print("Warning: No category scores available")
            return

         # Remove existing chart if any
        if hasattr(self, 'chart_view') and self.chart_view is not None:
            self.chart_view.deleteLater()

        # Create chart
        chart = QChart()
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setTitle("Category Performance Breakdown")

        # Create series & sets
        series = QStackedBarSeries()

        # Process category scores
        categories = []
        correct_set = QBarSet("Correct")
        incorrect_set = QBarSet("Incorrect")

        for category, stats in category_scores.items():
            if stats['total'] > 0: # Only include categories with questions
                categories.append(category)
                correct_set.append(stats['correct'])
                incorrect_set.append(stats['total'] - stats['correct'])

        # Exception handling for empty categories
        if not categories:
            print(f"{renderer.WARNING}[WARNING] No valid categories with questions found{renderer.ENDC}")
            return

        series.append(correct_set)
        series.append(incorrect_set)
        chart.addSeries(series)

        # Setup axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        max_questions = max([stats['total'] for stats in category_scores.values()])
        axis_y.setRange(0, max_questions)
        axis_y.setTitleText("Number of Questions")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Customize appearance
        chart.setTheme(QChart.ChartTheme.ChartThemeLight)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Create chart view
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMinimumHeight(400)

        # Add to the layout
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
            self.show_results()
            # Show results for 30 seconds, then quit app
            QTimer.singleShot(30000, sys.exit(0))

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