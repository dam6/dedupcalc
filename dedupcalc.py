#!/usr/bin/python

import hashlib
import argparse
import sys
import os

def parse_block_size(size_str):
    units = {"b": 1, "k": 1024, "m": 1024**2, "g": 1024**3}
    try:
        if size_str[-1].lower() in units:
            return int(size_str[:-1]) * units[size_str[-1].lower()]
        else:
            raise ValueError
    except ValueError:
        raise ValueError("invalid block size unit.\nTry 'dedupcalc.py --help' for more information.")

def read_blocks(file_path, block_size):
    try:
        with open(file_path, 'rb') as f:
            while block := f.read(block_size):
                yield block
    except OSError as e:
        raise OSError(f"dedupcalc.py: error reading file '{file_path}': {e}")

def hash_blocks(files, block_size=131072, verbose=False, algorithm='md5'):
    hash_table = {}
    if algorithm == 'md5':
        hash_function = hashlib.md5 
    elif algorithm == 'sha256':
        hash_function = hashlib.sha256

    for file in files:
        try:
            for block in read_blocks(file, block_size):
                block_hash = hash_function(block).hexdigest()
                hash_table[block_hash] = hash_table.get(block_hash, 0) + 1
        except OSError as e:
            print(f"dedupcalc.py: error processing file '{file}': {e}")
            sys.exit(1)

    if verbose:
        print_ddt(hash_table,algorithm)

    calculate_sizing(hash_table, block_size, len(files))

def print_ddt(hash_table, algorithm):
    hash_width = 32 if algorithm == 'md5' else 64
    hash_width += 2

    print(f"{'Block hash'.ljust(hash_width)} {'Hits'.rjust(6)}")
    for i, (hash, count) in enumerate(hash_table.items(), 1):
        print(f"{hash.ljust(hash_width)} {str(count).rjust(6)}")
    print("")

def calculate_sizing(hash_table, block_size, total_files):
    unique_blocks = len(hash_table)
    total_blocks = sum(hash_table.values())

    unique_size = round(unique_blocks * block_size / (1024 * 1024), 2)
    dedup_size = round((total_blocks - unique_blocks) * block_size / (1024 * 1024), 2)
    total_size = round(total_blocks * block_size / (1024 * 1024), 2)
    dedup_ratio = round(total_blocks / unique_blocks, 2) if unique_blocks > 0 else float('inf')

    label_width = 34 
    value_width = 6 

    print(f"{'Block size'.ljust(label_width)} {str(block_size / (1024 * 1024)).rjust(value_width)} MB")
    print(f"{'Files processed'.ljust(label_width)} {str(total_files).rjust(value_width)}")
    print(f"{'Total blocks'.ljust(label_width)} {str(total_blocks).rjust(value_width)}")
    print(f"{'Total size'.ljust(label_width)} {str(total_size).rjust(value_width)} MB")
    print(f"{'Unique blocks'.ljust(label_width)} {str(unique_blocks).rjust(value_width)}")
    print(f"{'Duplicated blocks'.ljust(label_width)} {str(total_blocks - unique_blocks).rjust(value_width)}")
    print(f"{'Unique size'.ljust(label_width)} {str(unique_size).rjust(value_width)} MB")
    print(f"{'Deduplicated size'.ljust(label_width)} {str(dedup_size).rjust(value_width)} MB")
    print(f"{'Deduplication ratio'.ljust(label_width)} {str(dedup_ratio).rjust(value_width)} :1")


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(
        description="Calculate deduplication statistics for provided files.",
        epilog="example: dedupcalc.py file1.txt file2.txt -b 256K -v -a sha256"
    )
    parser.add_argument(
        "files",
        nargs='+',
        help="List of files to process."
    )
    parser.add_argument(
        "-b", "--block_size",
        type=str,
        default="128k",
        help="Specify the block size. Acceptable units: B (bytes), K (kilobytes), M (megabytes), G (gigabytes). Default is 128K"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose mode. Display the hash table."
    )
    parser.add_argument(
        "-a", "--algorithm",
        type=str,
        choices=["md5", "sha256"],
        default="md5",
        help="Specify the hashing algorithm (md5 or sha256). Default is md5."
    )
    args = parser.parse_args()

    # Verify that all files exist before processing
    for file in args.files:
        if not os.path.isfile(file):
            print(f"dedupcalc.py: cannot access '{file}': No such file.")
            sys.exit(1)
    # Verify given size unit
    try:
        block_size = parse_block_size(args.block_size)
    except ValueError as e:
        print(f"dedupcalc.py: {e}")
        sys.exit(1)
    # Compute deduplication statistics
    try:
        hash_blocks(args.files, block_size, args.verbose, args.algorithm)
    except Exception as e:
        print(f"dedupcalc.py: {e}")
        sys.exit(1)