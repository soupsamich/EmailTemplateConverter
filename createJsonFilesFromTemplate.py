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
parser.add_argument('-p', '--phishing', choices=['s,c,l,a'], nargs='+', help='Creat json files for phishing instead of legit by supplying argument options of s, c, l, and/or a (sender, content, links, and/or attachments, respectfully)')
args = parser.parse_args()

# Create colored output variables
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Function to replace words in the JSON data
def replace_words(data, file_name):
    pattern = r"(\[[A-Za-z]+\])([A-Za-z0-9]+)\s(.+?)\.html" # Create regex to grab the sender, address, and subject from the filename (This assumes the file name format as "[L]Sender subject title for email.html")
    match = re.search(pattern, file_name)
    if match:
        phishing_type = match.group(1)
        email_sender = match.group(2)
        email_address = f'{email_sender}@mail.{email_sender}.com'.lower()
        email_subject = match.group(3)
        email_attachments = '"attachments": = ""'
        if isinstance(data, dict): # Search recursively through dictionaries
            for key, value in data.items():
                if 'P' in phishing_type:
                    if key == 'is_legit' and isinstance(value,bool):
                        data[key] = not value
                    elif 'S' in phishing_type and key == 'sender' and isinstance(value,bool):
                        data[key] = not value
                    elif 'C' in phishing_type and key == 'content' and isinstance(value,bool):
                        data[key] = not value
                    elif 'L' in phishing_type and key == 'links' and isinstance(value,bool):
                        data[key] = not value
                    elif 'A' in phishing_type and key == 'attachments' and isinstance(value,bool):
                        data[key] = not value
                    else:
                        data[key] = replace_words(value, file_name)
            return data
        elif isinstance(data, list): # Search recursively through lists
            return [replace_words(element, file_name) for element in data]
        elif isinstance(data, str):
            if 'S' in phishing_type:
                email_sender = f'FAKE{email_sender}'
                email_address = f'FAKE{email_sender}@hotmail.com'
            elif 'A' in phishing_type:
                email_attachments = '"attachments": = ["FAKEATTACHMENT.EXE"]'
            return data.replace('Enter Sender', email_sender).replace('Enter Address', email_address).replace('Enter Subject', email_subject).replace('"attachments": = ""', email_attachments)
        else:
            return data

# Function to iterate through html files and create a pairing json file with the same name
def create_json_files(input_path):
    for filename in os.listdir(input_path):
        if filename.endswith('.html'):
            json_filename = f"{os.path.splitext(filename)[0]}.json" # Create a json file with the same name as the html file
            input_json_file = os.path.join(input_path, json_filename)
            # Load the JSON template file
            with open(args.file_template, 'r') as file:
                json_data = json.load(file)
            new_json_data = replace_words(json_data, filename) # Replace 'Enter Sender' with 'Sender from filename.html' and 'Enter Subject' with 'Subject from filename.html'
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
