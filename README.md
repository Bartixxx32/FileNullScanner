# FileScannerNullByteChecker

This script allows you to scan files in a directory (including subdirectories) to detect files that are corrupted or filled with null bytes. It can be used for identifying broken or incomplete files like JPG, MP4, or other types, by analyzing a specified portion of the file for null bytes. The script also supports multi-threading for faster processing and allows you to specify different file extensions for scanning.

## Features

- Scans files in a given directory and its subdirectories.
- Detects files with null bytes, indicating they may be corrupted or incomplete.
- Supports multi-threading for faster scans.
- Allows specifying multiple file extensions (e.g., `.mp4`, `.jpg`, etc.).
- Option to delete the found corrupted files.
- Configurable threshold to scan a portion of the file (for faster checks).

## Installation

To run this script, you need Python 3

Install Python 3 from [python.org](https://www.python.org/downloads/) (if you haven't already).


## Usage

To run the script, use the following command:

````
python3 scanner.py /path/to/scan /path/to/output.txt --threshold 0.2 --workers 4 --extension jpg,mp4 --delete
````

### Arguments:

- **`/path/to/scan`**: The directory to scan for corrupted files.
- **`/path/to/output.txt`**: The output file where results will be saved.
- **`--threshold`**: Percentage of the file to check for null bytes (default: `0.2` for 20%).
- **`--workers`**: Number of threads to use for scanning (default: `4`).
- **`--extension`**: Comma-separated list of file extensions to scan (e.g., `jpg,mp4`).
- **`--delete`**: Deletes the files that are found to be corrupted or filled with null bytes.

## Example

To scan a directory and save the results to an output file, using 4 threads and checking for `.jpg` and `.mp4` files:

````
python3 scanner.py /path/to/scan /path/to/output.txt --threshold 0.1 --workers 4 --extension jpg,mp4
````

If you want to delete the corrupted files as well:

````
python3 scanner.py /path/to/scan /path/to/output.txt --threshold 0.1 --workers 4 --extension jpg,mp4 --delete
````

## How it Works

1. **File Scan**: The script recursively scans the specified directory for files matching the given extensions.
2. **Null Byte Check**: For each file, it reads a portion of the file (based on the threshold) and checks if it contains only null bytes (`0x00`).
3. **Results**: The script logs the files that are corrupted or filled with null bytes to the output file (`output.txt`).
4. **File Deletion**: If the `--delete` flag is used, the script will remove the corrupted files listed in the output file.

## Contributing

Feel free to fork this repository and submit pull requests if you have improvements, bug fixes, or new features. Please make sure to add tests and documentation for any new functionality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
