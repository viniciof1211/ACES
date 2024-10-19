import ast
import sys
import tokenize

def validate_syntax(file_path):
    """
    Validates the syntax of a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        bool: True if the syntax is valid, False otherwise.
    """
    try:
        # Read and parse the file into an Abstract Syntax Tree (AST)
        with open(file_path, 'r', encoding='utf-8') as file:
            source = file.read()
        ast.parse(source, filename=file_path)
        
        # Tokenizing the file for further checks
        with tokenize.open(file_path) as f:
            tokens = list(tokenize.generate_tokens(f.readline))
        
        print(f"Syntax validation successful for: {file_path}")
        return True
    
    except (SyntaxError, tokenize.TokenError) as e:
        print(f"Syntax error in file {file_path}:")
        print(f"Error message: {e}")
        print(f"Line number: {e.lineno}, Offset: {e.offset if hasattr(e, 'offset') else 'N/A'}")
        print(f"Line content: {e.text.strip() if hasattr(e, 'text') else 'N/A'}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while validating the file {file_path}:")
        print(str(e))
        return False

def check_encoding(file_path):
    """
    Checks if the file has a valid UTF-8 encoding.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        bool: True if the encoding is valid, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read()
        print("Encoding check passed: File is UTF-8 encoded.")
        return True
    except UnicodeDecodeError:
        print(f"Encoding error: The file {file_path} is not UTF-8 encoded.")
        return False

def validate_indentation(file_path):
    """
    Validates the indentation of the Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        bool: True if indentation is valid, False otherwise.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        stack = []
        for i, line in enumerate(lines, start=1):
            stripped_line = line.lstrip()
            if not stripped_line or stripped_line.startswith("#"):
                # Skip empty lines and comments
                continue

            # Calculate leading spaces/tabs
            indent_level = len(line) - len(stripped_line)
            
            if indent_level % 4 != 0:
                print(f"Indentation error at line {i}: Indentation level should be a multiple of 4 spaces.")
                return False

            if stripped_line.endswith(":"):
                stack.append(indent_level)
            elif len(stack) > 0 and indent_level <= stack[-1]:
                print(f"Indentation error at line {i}: Block should be indented further.")
                return False

        print("Indentation check passed.")
        return True

def main(file_path):
    """
    Main function to validate a Python file for syntax, encoding, and indentation.

    Args:
        file_path (str): The path to the Python file.
    """
    print(f"Validating file: {file_path}")
    if check_encoding(file_path):
        syntax_valid = validate_syntax(file_path)
        indentation_valid = validate_indentation(file_path)
        
        if syntax_valid and indentation_valid:
            print(f"The file '{file_path}' passed all validation checks.")
        else:
            print(f"The file '{file_path}' has issues that need to be fixed.")
    else:
        print("Aborting validation due to encoding issues.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_python_file.py <path_to_python_file>")
    else:
        main(sys.argv[1])
