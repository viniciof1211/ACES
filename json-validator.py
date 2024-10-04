# Let's load and attempt to parse the provided JSON file to identify any issues with its syntax.
import json

# File path for the uploaded JSON
json_file_path = 'scoring.json'

global data 
global result

# Attempt to load the JSON file and capture any errors
try:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        # print(f"[DEBUG] json.load() = [{data}]")
        result = "JSON is valid."
except json.JSONDecodeError as e:
    result = f"JSON syntax error: {str(data)}"
    print(f"[FATAL] Error {str(e.args)} at column {e.colno} and row [{e.lineno}]{result}")

if(len(result) <= 0):
    print(f"[{result}]{json_file_path} file is a correct CSV.")