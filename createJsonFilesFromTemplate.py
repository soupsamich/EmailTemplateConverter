import json
import os
import argparse
import re

# Create arguments
parser = argparse.ArgumentParser(
    description='Creates json files of the same name for each html files in a directory',
    epilog='Example: python3 createJsonFilesFromTemplate.py -f "/home/user/Desktop/LegitTemplate.json" -i "/home/user/Desktop/HTMLFiles/"')
parser.add_argument('-f', '--file-template', required=True, help='The json template file to use')
parser.add_argument('-i', '--input', required=True, help='Directory containing all of the html files you want json files created for')
args = parser.parse_args()

# Create colored output variables
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Create regex to grab the sender, address, and subject from the filename (This assumes the file name format as "[L]Sender subject title for email.html")
def get_filename_values(file_name):
    pattern = r"\[L\]([A-Za-z0-9]+)\s(.+?)\.html"
    match = re.search(pattern, file_name)
    if match:
        sender = match.group(1)
        address = f'{sender}@mail.{sender}.com'.lower()
        subject = match.group(2)
        #return sender, address, subject
    else: # If the filename is not formatted correctly for the regex, then make the sender and subject placeholders that will have to be manually changed
        sender = "Enter Sender"
        address = "Enter Address"
        subject = "Enter Subject"
    return sender, address, subject

# Function to replace words in the JSON data
def replace_words(data, email_sender, email_address, email_subject):
    if isinstance(data, dict):
        return {key: replace_words(value, email_sender, email_address, email_subject) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_words(element, email_sender, email_address, email_subject) for element in data]
    elif isinstance(data, str):
        return data.replace('Enter Sender', email_sender).replace('Enter Address', email_address).replace('Enter Subject', email_subject)
    else:
        return data

# Load the JSON template file
with open(args.file_template, 'r') as file:
    json_data = json.load(file)

# Function to iterate through html files and create a pairing json file with the same name
def create_json_files(input_path):
    for filename in os.listdir(input_path):
        if filename.endswith('.html'):
            sender, address, subject = get_filename_values(filename)
            json_filename = f"{os.path.splitext(filename)[0]}.json" # Create a json file with the same name as the html file
            input_json_file = os.path.join(input_path, json_filename)
            new_json_data = replace_words(json_data, sender, address, subject) # Replace 'Enter Sender' with 'Sender from filename.html' and 'Enter Subject' with 'Subject from filename.html'
            with open(input_json_file, 'w') as file: # Save the modified data to a new JSON file
                json.dump(new_json_data, file, indent=4)
            print(f"json file written to {BLUE}{input_json_file}{RESET}")

def main():
    try:
        create_json_files(args.input)
        print(f"{GREEN}Finished creating json files!{RESET}")
        print(f"{YELLOW}Remember to modify each json file with the correct scenario, sender, sender address, subject, and any attachments!{RESET}")
    except Exception as error:
        print(f"{RED}An exception offcured:{RESET}, {error}{RESET}")

# Run it
if __name__ == '__main__':
    main()