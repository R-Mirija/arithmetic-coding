# Arithmetic Coding

This project is a simple implementation of compression and decompression using arithmetic coding. It allows compressing a text file into a binary file and decompressing it to retrieve the original text.

## Features

- **Compression**: Converts a text file into a compressed binary file.
- **Decompression**: Reconstructs the original text file from the compressed binary file.

## Prerequisites

- **Python 3.8+**
- Ensure all required modules (`BitReader`, `BytesWriter`, `ArithmeticEncoder`, `HeaderManager`) are in the correct directory (classes/)

## File Structure

- **Input/Output Files**:
  - `out/to_compress.txt`: The text file to be compressed.
  - `out/compressed.bin`: The compressed binary file.
  - `out/decompressed.txt`: The decompressed text file.

## Key Files and Modules

This project is organized into several utility classes and modules to handle specific tasks:

- **`ArithmeticEncoder.py`**: 
  Implements the arithmetic encoding algorithm for compressing and decompressing data.

- **`HeaderManager.py`**: 
  Handles metadata management, including the text's **original length**, **number of different characters**, and **character mappings**.

- **`BytesWriter.py`**: 
  Manages writing binary data to files, ensuring efficient storage of compressed information.

- **`BitReader.py`**: 
  Handles bit-level reading operations for binary files, which is essential for decompression.

### File Locations

Ensure these files are in the `classes` folder, or adjust your imports accordingly in the main script.