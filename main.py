from classes.ArithmeticEncoder import ArithmeticEncoder
from classes.HeaderManager import HeaderManager
from time import time
from os import getcwd

# Paths
CURRENT_DIR = getcwd().replace("\\", "/")
TXT_FILE_PATH = f"{CURRENT_DIR}/out/to_compress.txt"
BIN_FILE_PATH = f"{CURRENT_DIR}/out/compressed.bin"
UNZIPPED_PATH = f"{CURRENT_DIR}/out/decompressed.txt"

# TXT_FILE_PATH = f"{CURRENT_DIR}/out/1.png"
# BIN_FILE_PATH = f"{CURRENT_DIR}/out/1.bin"
# UNZIPPED_PATH = f"{CURRENT_DIR}/out/2.png"


# Integer constants
ENCODER_BYTE_PRECISION = 4  # 32 bits
BLOCK_BUFFER_SIZE = 8192  # 8 Ko
CHAR_PRECISION = 1 << ENCODER_BYTE_PRECISION * 8 // 6

# Global utility
HEADER_MANAGER = HeaderManager(
    length_bytes=8,
    char_nbr_bytes=4,
    char_bytes=4,
    pb_bytes=4,
    char_prob_precision=CHAR_PRECISION
)


# Some functions :)
def compress(encoder: ArithmeticEncoder) -> None:
    start = time()
    encoder.compress(TXT_FILE_PATH, BIN_FILE_PATH)
    print(f"Compression: {time() - start}s")


def decompress(encoder: ArithmeticEncoder) -> None:
    start = time()
    encoder.decompress(BIN_FILE_PATH, UNZIPPED_PATH)
    print(f"Decompression: {time() - start}s")


def fill_text_file(file_path: str) -> None:
    # around 12,5 Mo of text data
    with open(file_path, "w") as f:
        f.write("Hello World  " * 1_000_000)


if __name__ == '__main__':

    coder = ArithmeticEncoder(
        HEADER_MANAGER, ENCODER_BYTE_PRECISION, BLOCK_BUFFER_SIZE)

    while True:

        choice = int(
            input("--- (1) Compress, (2) decompress, (3) fill text file, (0) quit ---  ")
        )

        if choice == 0:
            print("Quit :'")
            break
        elif choice == 1:
            print("Compressing...")
            compress(coder)
        elif choice == 2:
            print("Decompressing...")
            decompress(coder)
        elif choice == 3:
            print(f"Filled \"{TXT_FILE_PATH}\"")
            fill_text_file(TXT_FILE_PATH)
        else:
            print("Invalid choice")
