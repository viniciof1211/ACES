# Let's validate the CSV file to check if it follows the schema exactly.
import csv

global file_path

 # File path for the uploaded CSV
file_path = 'az-305_questions.csv'

def validate():
    # Schema definition
    expected_header = ["Question", "OptionA", "OptionB", "OptionC", "OptionD", "CorrectAnswer", "Explanation"]
    expected_field_count = len(expected_header)

    # Result variable to capture any errors
    errors = []

    # Reading the CSV file and validating each row
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader, None)
    
        # Check if the header matches the expected schema
        if header != expected_header:
            errors.append("Header does not match the expected schema.")
    
        err_str = " "
        # Check each row for the correct number of fields
        for i, row in enumerate(reader, start=2):  # Start at 2 to account for the header row
            if len(row) != expected_field_count:
                err_str = f"Row {i} does not have {expected_field_count} fields: {row}\n"
                errors.append(err_str)
                print(err_str)

    if errors:
        return
    # Output the result
    #for error in errors:
    #        print(f"\n{error}")
    #        return
    print("CSV is valid according to the schema.")

def main():
    validate()

if __name__ == "__main__":
    main()