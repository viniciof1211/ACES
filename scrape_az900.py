import os
import pandas as pd
from bs4 import BeautifulSoup

# Directory where the HTML files are stored
html_dir = "."

# List to store the extracted data
data = []

# Loop through each HTML file
for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(html_dir, filename)

        # Open and parse the HTML file
        with open(filepath, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "lxml")

            # Extract questions, answers, and explanations
            # Adjust these based on the actual structure of the HTML
            questions = soup.find_all("div", class_="question")
            answers = soup.find_all("div", class_="answer")
            explanations = soup.find_all("div", class_="explanation")

            # Loop through each question, answer, and explanation
            for i in range(min(len(questions), len(answers), len(explanations))):
                question_text = questions[i].get_text(strip=True)
                answer_text = answers[i].get_text(strip=True)
                explanation_text = explanations[i].get_text(strip=True)

                # Add the data to the list
                data.append({
                    "Episode": filename.split("-")[1].replace(".html", ""),
                    "Question": question_text,
                    "Answer": answer_text,
                    "Explanation": explanation_text
                })

# Convert the data to a DataFrame and save it as a CSV file
df = pd.DataFrame(data)
csv_path = "AZ-900_Practice_Test_Questions.csv"
df.to_csv(csv_path, index=False)

print(f"Scraping complete. Data saved to {csv_path}")
