# Let's first load and inspect the contents of the CSV file to ensure each row has 7 fields.
import csv
from tkinter import NO

# File path for the uploaded CSV
file_path = 'ms900_questions.csv'

# List to capture rows with incorrect number of fields
invalid_rows = []
no_header = False
hdr = 'Question;OptionA;OptionB;OptionC;OptionD;CorrectAnswer;Explanation'

# Read the CSV file and validate the number of fields per row
with open(file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    if hdr not in csvfile.read():
            no_header = True
    else:
        for row_number, row in enumerate(csvreader, start=1):
            if len(row) != 7:
                invalid_rows.append((row_number, row))

if len(invalid_rows) <= 0 and no_header != True:
    print(f"{file_path} file is a correct CSV.")

for row in invalid_rows:
    print(row)