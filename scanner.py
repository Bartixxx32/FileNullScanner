import os
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_null_bytes(file_path, threshold=0.2):
    """Check if the first `threshold` percentage of the file contains only null bytes."""
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return f"{file_path} - Empty file"
        
        read_size = int(file_size * threshold)  # Read only the first `threshold`% of the file
        with open(file_path, "rb") as f:
            chunk = f.read(read_size)
            if all(byte == 0 for byte in chunk):  # Check if all bytes are null
                return f"{file_path} - Filled with null bytes"
    except Exception as e:
        return f"{file_path} - Error: {str(e)}"
    return None  # File is not filled with null bytes

def scan_file(file_path, threshold):
    """Wrapper for thread-based file scanning."""
    return check_null_bytes(file_path, threshold)

def scan_directory(directory, output_file, threshold=0.2, max_workers=4, file_extensions=None):
    """Scan a directory for specific file types with null bytes using multithreading."""
    with open(output_file, "w") as output, ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file_extensions:
                    if not any(file.lower().endswith(ext.lower()) for ext in file_extensions):
                        continue  # Skip files that don't match the specified extensions
                file_path = os.path.join(root, file)
                futures.append(executor.submit(scan_file, file_path, threshold))
        
        for future in as_completed(futures):
            result = future.result()
            if result:  # If there's an issue or null-byte-filled file, log it
                output.write(result + "\n")

def delete_files_from_output(output_file):
    """Delete files listed in the output file."""
    with open(output_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            file_path = line.split(" - ")[0].strip()  # Extract file path from the result line
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {str(e)}")
            else:
                print(f"File not found: {file_path}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scan for files filled with null bytes.")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("output", help="Output file to save the results")
    parser.add_argument("--threshold", type=float, default=0.2, help="Percentage of file to check (default: 20%)")
    parser.add_argument("--workers", type=int, default=4, help="Number of threads to use (default: 4)")
    parser.add_argument("--extension", type=str, default=None, help="Comma-separated list of file extensions to scan (e.g., .mp4,.jpg)")
    parser.add_argument("--delete", action="store_true", help="Delete the files found in the output.txt")

    args = parser.parse_args()

    # Convert the --extension argument to a list of extensions
    file_extensions = None
    if args.extension:
        file_extensions = [ext.strip() for ext in args.extension.split(',')]

    print(f"Scanning directory: {args.directory}")
    print(f"Saving results to: {args.output}")
    print(f"Threshold: {args.threshold}")
    print(f"Using {args.workers} workers")
    print(f"File extensions filter: {file_extensions}")

    # Run the scan with the given extension filter
    scan_directory(args.directory, args.output, threshold=args.threshold, max_workers=args.workers, file_extensions=file_extensions)
    
    # If delete flag is set, delete the files listed in the output file
    if args.delete:
        print("Deleting files found in the output file...")
        delete_files_from_output(args.output)
