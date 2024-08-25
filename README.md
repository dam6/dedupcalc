# dedupcalc

![Project Logo](logo.png)

Deduplication calculator for calculating deduplication statistics across a set of files by identifying duplicate blocks of data.

**Note:** This script does not modify or deduplicate the provided files. It only computes potential deduplication statistics.

## What is Deduplication?

Deduplication is a data compression technique that eliminates duplicate copies of repeating data. It works by storing only unique blocks of data and referencing these blocks whenever the same data appears. Deduplication optimizes storage space but can impact system performance.

## How It Works

### Block Size

The script processes files in chunks known as "blocks." The size of these blocks is configurable to optimize storage usage. Blocks are read sequentially from each file, and each block is hashed to identify duplicates. These hash values are stored in a hash table.

### Hash Table

A data structure that maps the hash of each unique block to the number of times it appears across all files.

### Hashing Algorithms

- **MD5** (default): Faster and more performance-friendly but less reliable due to a higher likelihood of collisions.
- **SHA-256**: More reliable with a lower chance of collisions but slower and more resource-intensive.

#### Process Overview

1. Each block is hashed.
2. If the hash already exists in the hash table, the count for that hash is incremented (indicating a duplicate block).
3. If the hash does not exist in the table, it is added with a count of one.

This approach allows the script to efficiently track and calculate the total number of unique and duplicate blocks.

### Deduplication Metrics

The script calculates the following metrics:
- **Total Blocks**: The total number of blocks across all files.
- **Unique Blocks**: The number of unique blocks, identified by their hash values.
- **Duplicated Blocks**: The number of blocks that are duplicated.
- **Total Size**: The total size of all blocks in megabytes (MB).
- **Unique Size**: The size of the unique blocks in megabytes (MB).
- **Deduplicated Size**: The potential storage savings from eliminating duplicate blocks.
- **Deduplication Ratio**: The ratio of total blocks to unique blocks, indicating the level of redundancy.

The deduplication ratio is calculated as:

`Deduplication Ratio = Total Blocks / Unique Blocks`

A ratio of `1:1` indicates no potential for deduplication, while higher ratios suggest greater redundancy and potential storage savings.

## Usage

```bash
dedupcalc.py [-h] [-b BLOCK_SIZE] [-v] [-a {md5,sha256}] files [files ...]
```

Calculate deduplication statistics for the provided files.

### Positional Arguments:
- **files**: List of files to process.

### Optional Arguments:
- **-h, --help**: Show this help message and exit.
- **-b BLOCK_SIZE, --block_size BLOCK_SIZE**: Specify the block size. Acceptable units: B (bytes), K (kilobytes), M (megabytes), G (gigabytes). Default is `128K`.
- **-v, --verbose**: Enable verbose mode to display the contents of the hash table.
- **-a {md5, sha256}, --algorithm {md5, sha256}**: Specify the hashing algorithm. Options are `md5` (default) or `sha256`.

### Example:

```bash
dedupcalc.py file1.txt file2.txt -b 256K -v -a sha256
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
