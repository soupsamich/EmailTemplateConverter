# htmlImageConverter

Use to convert all image links in an html file to base64 encoded data that can be viewed offline

## Recommended Python Version:

htmlImageConverter currently supports **Python 3**.

* The recommended version for Python 3 is **3.4.x**

## Dependencies:

findInputs depends on the `requests`, `BeautifulSoup`, `argparse`, `base64`, and `os` python modules.

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

### Examples

* Supply a single html file and convert all image links to base64, then output the converted html file into the specified output directory:

```python3 htmlImageConverter.py -i "/home/user/OriginalFiles/index.html" -o "/home/user/ConvertedFiles"```

* Supply a directory and convert the images to base64 for all html files within that directory, then output each file as a new file in the specified output directory:

```python3 htmlImageConverter.py -i "/home/user/OriginalFiles" -o "/home/user/ConvertedFiles"```


## License:

This project is licensed under the GPL-3.0 License - see the LICENSE.md file for details

## Version:
**Current version is 1.0**
