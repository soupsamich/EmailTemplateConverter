### Walkthrough example:
- Download the script files and template file listed in this github repo.
- Download email templates you'd like to convert and place them into a directory together
```example: /home/user/OriginalFiles/email.html```
- Use this naming format for each of the email templates: [L]Sender This will be the subject title.html
```example: [L]Disney Get $10 off your first Disney+ Membership.html```
- Use the htmlImageConverter.py script to iterate through the html files in the specified directory converting all images into base64 data and changing all names and emails to name and email variables
```example:  python3 htmlImageConverter.py -i '/home/user/OriginalFiles/' -o '/home/user/ConvertedFiles/'```
- Open all of the .html files to double check they look the way you expect them to look, and that all of the names and emails have been replaced with [[variables]]
```in the above examples, these converted html files would be located in the /home/user/ConvertedFiles/ directory```
- Use the createJsonFilesFromTemplate.py script to utilize a template file to create json files that will pair with each of the html files. The sender_display_name, sender_address, and subject fields will be auto-filled by the script using the .html filename if formatted correctly. They will be placed into the same directory with the .html files
```example: python3 createJsonFilesFromTemplate.py -f '/home/user/LegitTemplate.json' -i '/home/user/ConvertedFiles'```
- Open all of the .json files and fill in the "scenario" value, along with the "attachments" value if necessary. Also, double check that the other values were filled in as expected

<br>
<br>
<br>

# htmlImageConverter

Use to convert all image links in an html file to base64 encoded data that can be viewed offline

## Recommended Python Version:

htmlImageConverter currently supports **Python 3**.

* The recommended version for Python 3 is **3.4.x**

## Dependencies:

findInputs depends on the `requests`, `BeautifulSoup`, `argparse`, `base64`, `re`, and `os` python modules.

The beautifulsoup4 module can be installed as shown below.

#### Modules (http://docs.python-requests.org/en/latest/)

- Install for Windows:
```
c:\python38\python3.exe -m pip3 install beautifulsoup4
```

- Install using pip on Linux:
```
sudo pip3 install beautifulsoup4
```

## Usage:

Short Form    | Long Form           | Description
------------- | ------------------- |-------------
-h            | --help              | Show the help message and exit
-i            | --input             | The directory or html file path location. If a directory, then all html files in that location will be converted. If a file path, then just that file will be converted.
-o            | --output-directory  | Directory output location where the converted file(s) will be created.
-n            | --keep-default-names| Prevent the changing of default names and emails to variables.

### Examples

* Supply a single html file and convert all image links to base64, then output the converted html file into the specified output directory:

```python3 htmlImageConverter.py -i "/home/user/OriginalFiles/index.html" -o "/home/user/ConvertedFiles"```

* Supply a directory and convert the images to base64 for all html files within that directory, then output each file as a new file in the specified output directory:

```python3 htmlImageConverter.py -i "/home/user/OriginalFiles" -o "/home/user/ConvertedFiles"```

<br>
<br>
<br>

# createJsonFilesFromTemplate.py

Use to create json file pairings for converted html files


## Dependencies:

findInputs depends on the `json`, `argparse`, `re`, and `os` python modules.


## Usage:

Short Form    | Long Form           | Description
------------- | ------------------- |-------------
-f            | --file-template     | The full path for the json template file.
-i            | --input             | Directory containing all of the html files you want json files created for.

### Examples

* Use the LegitTemplate.json file to create json files for all html files in the HTMLFiles directory:

```python3 createJsonFilesFromTemplate.py -f "/home/user/Desktop/LegitTemplate.json" -i "/home/user/Desktop/Converted/HTMLFiles/"```

<br>
<br>

# License:

This project is licensed under the GPL-3.0 License - see the LICENSE.md file for details

<br>

## References:

Help building regex:
* https://regex-generator.olafneumann.org/
* https://regex101.com/

