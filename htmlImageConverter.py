import os
import base64
import requests
import argparse
from bs4 import BeautifulSoup
import re

# Create arguments
parser = argparse.ArgumentParser(
    description='Converts image links in HTML files to base64 so they can be used offline.',
    epilog='Example: python3 htmlImageConverter.py -i "/home/user/Desktop/Original" -o "/home/user/Desktop/Converted"')
parser.add_argument('-i', '--input', required=True, help='The directory or html file path location. If a directory, then all html files in that location will be converted. If a file path, then just that file will be converted.')
parser.add_argument('-o', '--output-directory', required=True, help='Directory output location where the converted file(s) will be created.')
parser.add_argument('-n', '--keep-default-names', help='Prevent the changing of default names to variables')
args = parser.parse_args()

# Create colored output variables
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# A function that takes an image link, converts the image data to base64, then returns it in a way that html can render it as an image offline
def fetch_image_base64(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            return f'data:image/png;base64,{img_base64}'
        else:
            print(f"{RED}-----------Failed to fetch image from {url}{RESET}")
            return 'FailedRequest' # removes the broken image link and replaces with a string
    except requests.RequestException as e:
        print(f"{RED}-----------Error fetching image from {url}: {e}{RESET}")
        return 'ExceptionError' # removes the broken image link and replaces with a string

# A function that takes in and reads an html file, then uses the fetch_image_base64 function to convert all image links within the file to base64 encoded images, then replaces the links with the encoded data, lastly writes it all as a new html file
def convert_image_links_to_base64(html_file_path, output_file_path):
    with open(html_file_path, 'r') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            img_src = img_tag.get('src')
            if img_src and img_src.startswith('https'):
                img_base64 = fetch_image_base64(img_src)
                if img_base64:
                    img_tag['src'] = img_base64
        if not args.keep_default_names: # If the -n tag is not  used, then change all Smiles Davis to firstname and lastname variables, and all hello@smilesdavis.yeah to email variable
            default_names = soup.find_all(string = re.compile('Smiles Davis'))
            for default_name in default_names:
                changed_name = default_name.replace('Smiles Davis', '[[firstName]] [[lastName]]')
                default_name.replace_with(changed_name)
            default_emails = soup.find_all(string = re.compile('hello@SmilesDavis.yeah'))
            for default_email in default_emails:
                changed_email = default_email.replace('hello@SmilesDavis.yeah', '[[email]]')
                default_email.replace_with(changed_email)

    with open(output_file_path, 'w') as output_file:
        output_file.write(str(soup))

# A function that takes in a directory or file, uses the convert_image_links_to_base64 function to convert the images within the html file, then outputs the file into the output directory
def process_html_files(input_path, output_directory):
    if os.path.isdir(input_path): # if the input is a directory, iterate through all html files within that directory
        for filename in os.listdir(input_path):
            if filename.endswith(".html"):
                input_html_file = os.path.join(input_path, filename)
                output_html_file = os.path.join(output_directory, filename)
                convert_image_links_to_base64(input_html_file, output_html_file)
                print(f"Modified HTML written to {BLUE}{output_html_file}{RESET}")
    elif os.path.isfile(input_path) and input_path.endswith(".html"): # if the input is a file, just convert that single file then output into the output directory
        output_html_file = os.path.join(output_directory, os.path.basename(input_path))
        convert_image_links_to_base64(input_path, output_html_file)
        print(f"Modified HTML written to {BLUE}{output_html_file}{RESET}")
    else:
        print(f"{RED}Invalid input or output. Please provide a valid directory or a single HTML file.{RESET}")

# The top level function to execute the process_html_files function with the user supplied arguments
def main():
    if os.path.isdir(args.output_directory):
        print(f"Starting conversion of html files in {YELLOW}{args.input}{RESET}")
        process_html_files(args.input, args.output_directory)
        print(f"Finished converting html files. Converted files can be found in {GREEN}{args.output_directory}{RESET}")
    else:
        print(f"{RED}Error: Output path cannot be a file. Please provide a valid directory for output.{RESET}")

# Run it
if __name__ == '__main__':
    main()
