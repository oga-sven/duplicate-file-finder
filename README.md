# Duplicate File Finder

This is a Python script that finds duplicate files in a directory. It works by comparing the hashes (SHA-256) of the files. If two or more files have the same hash, they are considered duplicates.

The script generates a log file, a JSON file, and an HTML file. The log file contains the paths of all duplicate files. The JSON file contains the same information but in JSON format. The HTML file presents the duplicate files in a user-friendly way. Each group of duplicate files is displayed with their thumbnails, file paths, and sizes. A command to delete the selected duplicates is also generated.

## Usage

You can run the script from the command line like this:

```bash
python compare.py "your/directory/path" "output/directory/path" --verbose
```
`your/directory/path`: The path of the directory you want to search for duplicate files. This is a required argument.

`output/directory/path`: (optional) The path of the directory where you want to save the output files. This is an optional argument. If not provided, the output files will be saved in a folder named "output" in the same directory as the script.

`--verbose`: (optional) If this flag is set, the script will also create a verbose log file named "script_log.log" that details every action the script is doing.
After running the script, you can open the generated duplicates.html file in your web browser to view and manage the duplicate files.

## Installation

This project uses Python 3.8 or Later. You need to have it installed to run the script.

1. Clone the repository & Move into the project directory::
    ```sh
    git clone https://github.com/oga-sven/duplicate-file-finder.git
    ```

2. Install the required packages:
    ```sh
    pip install tqdm
    # Additionally: python3 -m pip install tqdm
    ```

3. Run the command 
   ```sh
   python compare.py "D:/myPhotos" 
   ```

___

License: Just keep my name in your thoughts when you go to sleep at night (Just MIT or something. What all the other peeps do)
