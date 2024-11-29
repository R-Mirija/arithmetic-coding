from classes.ArithmeticEncoder import ArithmeticEncoder
from classes.HeaderManager import HeaderManager
from time import time

# Paths
TXT_FILE_PATH = "out/to_compress.txt"
BIN_FILE_PATH = "out/compressed.bin"
UNZIPPED_PATH = "out/decompressed.txt"

# Integer constants
PRECISION = 24
WHOLE = pow(2, PRECISION)
BLOCK_BUFFER_SIZE = 8192  # 8 Ko

# Global utility
HEADER_MANAGER = HeaderManager(length_bytes=8, char_nbr_bytes=4, char_bytes=4, pb_bytes=4, char_prob_precision=WHOLE // 6)


# Some functions :)
def compress(encoder: ArithmeticEncoder) -> None:
    start = time()
    encoder.compress(TXT_FILE_PATH, BIN_FILE_PATH)
    print(f"Compression: {time() - start}s")


def decompress(encoder: ArithmeticEncoder) -> None:
    start = time()
    encoder.decompress(BIN_FILE_PATH, UNZIPPED_PATH, PRECISION)
    print(f"Decompression: {time() - start}s")


def fill_text_file(file_path: str) -> None:
    # around 12 Mo of text data
    with open(file_path, "w") as f:
        f.write("Hello World " * 1_000_000)


if __name__ == '__main__':

    coder = ArithmeticEncoder(HEADER_MANAGER, WHOLE, BLOCK_BUFFER_SIZE)

    while True:
        choice = int(input("Compress (1), decompress (2), fill text file (3), quit (0) ---  "))

        if choice == 1:
            print("Compressing...")
            compress(coder)
        elif choice == 2:
            print("Decompressing...")
            decompress(coder)
        elif choice == 3:
            print(f"Filled \"{TXT_FILE_PATH}\"")
            fill_text_file(TXT_FILE_PATH)
        elif choice == 0:
            print("Quit :'")
            break
