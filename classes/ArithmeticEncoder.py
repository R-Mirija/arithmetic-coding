from io import SEEK_SET
from classes.BitReader import BitReader
from classes.BytesWriter import BytesWriter
from classes.HeaderManager import HeaderManager


class ArithmeticEncoder:

    def __init__(self, header_manager: HeaderManager, whole: int, block_buffer_size: int) -> None:
        self.header_manager = header_manager
        self.whole = whole
        self.half = whole // 2
        self.quarter = whole // 4
        self.block_buffer_size = block_buffer_size

    def compress(self, src_file: str, dest_file: str) -> None:
        """
        Compress the source file using arithmetic coding and write to the destination file.
        """
        with open(src_file, "r") as src_f, open(dest_file, "wb") as dest_f:

            bits = []
            a, b = 0, self.whole
            s = 0

            header = self.header_manager.get_header(src_f)
            if not header["pb"]:
                return

            cumulated = HeaderManager.get_header_cumulated(header)
            self.header_manager.encode_header(header, dest_f)
            src_f.seek(0, SEEK_SET)

            bytes_writer = BytesWriter(dest_f)

            while block := src_f.read(self.block_buffer_size):
                for char in block:
                    char_precision = self.header_manager.get_char_prob_precision()
                    w = b - a
                    b = a + w * cumulated["pb"][char]["max"] // char_precision
                    a = a + w * cumulated["pb"][char]["min"] // char_precision

                    while b < self.half or a > self.half:
                        if b < self.half:
                            # emit 0 and s ones
                            bits.extend([0] + ([1] * s))
                            a *= 2
                            b *= 2
                            s = 0
                        elif a > self.half:
                            # emit 1 and s zeros
                            bits.extend([1] + ([0] * s))
                            a = 2 * (a - self.half)
                            b = 2 * (b - self.half)
                            s = 0

                        # uncomment this line for very, very large files
                        # bits = bytes_writer.write_bytes(bits)

                    while a > self.quarter and b < 3 * self.quarter:
                        a = 2 * (a - self.quarter)
                        b = 2 * (b - self.quarter)
                        s += 1
            s += 1
            bits.extend([0] + ([1] * s) if a <=
                        self.quarter else [1] + ([0] * s))
            bits = bytes_writer.write_bytes(bits)
            bytes_writer.write_remaining_bytes(bits)

    def decompress(self, src_file: str, dest_file: str, precision: int) -> None:
        """
        Decompress the file using arithmetic coding.
        """
        with open(src_file, "rb") as src_f, open(dest_file, "w") as dest_f:

            header = self.header_manager.decode_header(src_f)
            cumulated = HeaderManager.get_header_cumulated(header)
            bit_reader = BitReader(src_f, buffer_size=self.block_buffer_size)

            a, b = 0, self.whole

            # Getting tag approximation
            tag = int.from_bytes(src_f.read(precision // 8), byteorder="big")
            count = 0
            sequence = ""

            while True:
                for char in cumulated["pb"]:
                    char_precision = self.header_manager.get_char_prob_precision()
                    w = b - a
                    a0 = a + w * cumulated["pb"][char]["min"] // char_precision
                    b0 = a + w * cumulated["pb"][char]["max"] // char_precision

                    # if character matches interval
                    if a0 <= tag < b0:
                        a, b = a0, b0
                        sequence += char
                        count += 1

                        if len(sequence) >= 100:
                            dest_f.write(sequence)
                            sequence = ""
                        if count == header["sequence_length"]:
                            dest_f.write(sequence)
                            return

                        break

                while b < self.half or a > self.half:
                    if b < self.half:
                        a *= 2
                        b *= 2
                        tag *= 2
                    elif a > self.half:
                        a = 2 * (a - self.half)
                        b = 2 * (b - self.half)
                        tag = 2 * (tag - self.half)
                    tag += bit_reader.read_bit() or 0

                while a > self.quarter and b < 3 * self.quarter:
                    a = 2 * (a - self.quarter)
                    b = 2 * (b - self.quarter)
                    tag = 2 * (tag - self.quarter)
                    tag += bit_reader.read_bit() or 0
