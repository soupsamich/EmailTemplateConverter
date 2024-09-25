import os
import base64
import requests
import argparse
from bs4 import BeautifulSoup
import re

# Check the characters placed in the --phishing argument to make sure they are valid
def check_phishing_chars(phishingargs_value):
    phishingargs_value = phishingargs_value.lower()
    valid_chars = "sclaq"
    if not all(char in valid_chars for char in phishingargs_value):
        raise argparse.ArgumentTypeError(f"Invalid characters in the -p/--phishing argument. Use only '{valid_chars}'.")
    return phishingargs_value

# Create arguments
parser = argparse.ArgumentParser(
    description='Converts image links in HTML files to base64 so they can be used offline.',
    epilog='Example: python3 htmlImageConverter.py -i "/home/user/Desktop/Original" -o "/home/user/Desktop/Converted"')
parser.add_argument('-i', '--input', required=True, help='The directory or html file path location. If a directory, then all html files in that location will be converted. If a file path, then just that file will be converted.')
parser.add_argument('-o', '--output-directory', required=True, help='Directory output location where the converted file(s) will be created.')
parser.add_argument('-n', '--keep-default-names', help='Prevent the changing of default names and emails to variables')
parser.add_argument('-p', '--phishing', type=check_phishing_chars, nargs='*', help='Creat phishing html files as well by supplying argument options of s, c, l, and/or a (sender, content, links, and/or attachments, respectfully)')
args = parser.parse_args()

# Create colored output variables
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Create the [PSCLA] name prefix depending on what arguments are supplied to the -p parameter, and always order them correctly regardless of how they are supplied
def generate_prefix(characters):
    ordered_chars = ''.join(sorted(characters, key=lambda c: 'sclaq'.index(c.lower())))
    return f"[P{ordered_chars}]".upper()

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
# Also removes all href links and replaces with javvascript:void(0)
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
        links = soup.find_all('a')
        for original_link in links:
            original_link['href'] = 'javascript:void(0)'
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
    # if the input is a directory, iterate through all html files within that directory
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            # create html files with the same names as the original
            if filename.endswith(".html"):
                input_html_file = os.path.join(input_path, filename)
                output_html_file = os.path.join(output_directory, filename)
                convert_image_links_to_base64(input_html_file, output_html_file)
                print(f"Modified HTML written to {BLUE}{output_html_file}{RESET}")
                # if the user supplied phishing arguments, then also create .html files with the [P] prefix depending on the arguments supplied.
                if args.phishing:
                    pattern = r"(\[[A-Za-z]+\])([A-Za-z0-9]+)\s(.+?\.html)"
                    match = re.search(pattern, filename)
                    if match:
                        original_prefix = match.group(1)
                        filename_noprefix = f"{match.group(2)} {match.group(3)}"
                        # the user can supply multiple -p arguments, this will iterate through them and create an html file for each
                        for phish_choice in args.phishing:
                            name_prefix = generate_prefix(phish_choice)
                            # create the new phishing html files only if the original wasn't also a phishing file, for example if the original was [PL] and the user supplied argument was '-p l', then skip that one because there was already an html file converted and created in the first part of this function
                            if original_prefix != name_prefix:
                                output_filename = f"{name_prefix}{filename_noprefix}"
                                output_html_file = os.path.join(output_directory, output_filename)
                                convert_image_links_to_base64(input_html_file, output_html_file)
                                print(f"Modified HTML written to {BLUE}{output_html_file}{RESET}")
                            else:
                                print(f"Skipping creation of file using args flag {phish_choice} because it's the same as the original conversion which was done already by default.")
    # if the input is a file, just convert that single file then output into the output directory     
    elif os.path.isfile(input_path) and input_path.endswith(".html"):
        output_html_file = os.path.join(output_directory, os.path.basename(input_path))
        convert_image_links_to_base64(input_path, output_html_file)
        print(f"Modified HTML written to {BLUE}{output_html_file}{RESET}")
        if args.phishing:
                    pattern = r"(\[[A-Za-z]+\])([A-Za-z0-9]+)\s(.+?\.html)"
                    match = re.search(pattern, input_path)
                    if match:
                        original_prefix = match.group(1)
                        filename_noprefix = f"{match.group(2)}{match.group(3)}"
                        # the user can supply multiple -p arguments, this will iterate through them and create an html file for each
                        for phish_choice in args.phishing:
                            name_prefix = generate_prefix(phish_choice)
                            # create the new phishing html files only if the original wasn't also a phishing file, for example if the original was [PL] and the user supplied argument was '-p l', then skip that one because there was already an html file converted and created in the first part of this function
                            if original_prefix != name_prefix:
                                output_filename = f"{name_prefix}{filename_noprefix}"
                                output_html_file = os.path.join(output_directory, output_filename)
                                convert_image_links_to_base64(input_path, output_html_file)
                                print(f"Modified HTML written to {BLUE}{output_html_file}{RESET}")
                            else:
                                print(f"Skipping creation of file:{BLUE}{output_html_file}{RESET} using args flag {phish_choice} because it's the same as the original and that has been converted already by default.")
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
