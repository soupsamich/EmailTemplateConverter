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

# Function to replace words in the JSON data
def replace_words(data, file_name):
    pattern = r"(\[[A-Za-z]+\])([A-Za-z0-9]+)\s(.+?)\.html" # Create regex to grab the sender, address, and subject from the filename (This assumes the file name format as "[L]Sender subject title for email.html")
    match = re.search(pattern, file_name)
    if match:
        phishing_type = match.group(1)
        email_sender = match.group(2)
        email_address = f'{email_sender}@mail.{email_sender}.com'.lower()
        data['email']['sender_display_name'] = email_sender
        print(email_sender)
        data['email']['sender_address'] = email_address
        data['email']['subject'] = match.group(3)
        if "P" in phishing_type:
            data['email']['is_legit'] = False
            #print(match.group(2))
            if "S" in phishing_type:
                data['email']['sender_display_name'] = f'FAKE{email_sender}'
                print(match.group(2))
                data['email']['sender_address'] = f'FAKE{email_sender}@hotmail.com'
                data['phishing_attributes']['sender'] = True
            if "C" in phishing_type:
                data['phishing_attributes']['content'] = True
            if "L" in phishing_type:
                data['phishing_attributes']['links'] = True
                data['phishing_attributes']['link_display_url'] = f'MALICIOUSWEBSITE.COM/VICTIM'
            if "A" in phishing_type:
                data['email']['attachments'] = ["FAKEATTACHMENT.EXE"]
                data['phishing_attributes']['attachments'] = True
            if "Q" in phishing_type:
                data['phishing_attributes']['qrcode'] = True
                data['phishing_attributes']['qrcode_display_url'] = "MALICIOUSWEBSITE.COM"
    return data

# Function to iterate through html files and create a pairing json file with the same name
def create_json_files(input_path):
    for filename in os.listdir(input_path):
        if filename.endswith('.html'):
            json_filename = f"{os.path.splitext(filename)[0]}.json" # Create a json file with the same name as the html file
            input_json_file = os.path.join(input_path, json_filename)
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
        print(f"{YELLOW}REMEMBER TO CHECK AND MODIFY EACH JSON FILE WITH THE CORRECT VALUES! For instance: if you have links as true phishing then make sure to change the link_display_url, if you have sender as true phishing make sure to change the sender_display_name and sender_address etc.!{RESET}")
    except Exception as error:
        print(f"{RED}An exception offcured:{RESET}, {error}{RESET}")

# Run it
if __name__ == '__main__':
    main()
