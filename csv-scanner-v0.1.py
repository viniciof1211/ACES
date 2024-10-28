# Now I will load and inspect the uploaded file to ensure it follows the correct schema and fix any potential issues.

import pandas as pd

# Load the CSV file
file_path = 'az-305_questions.csv'
df = pd.read_csv(file_path, delimiter=';', header=None)

# The expected schema and header format:
expected_columns = ['Question', 'OptionA', 'OptionB', 'OptionC', 'OptionD', 'CorrectAnswer', 'Explanation']

# Check if the number of columns is correct
if len(df.columns) != len(expected_columns):
    df.columns = expected_columns[:len(df.columns)]  # Rename columns according to schema

# Checking for any potential misalignments, incomplete rows, or missing fields
incomplete_rows = df[df.isnull().any(axis=1)]

# Display rows with missing data for inspection
for bad_row in incomplete_rows:
    print(f"{bad_row}\n")
