from collections import Counter
from typing import TextIO, BinaryIO


class HeaderManager:

    def __init__(
            self,
            length_bytes: int,
            char_nbr_bytes: int,
            char_bytes: int,
            pb_bytes: int,
            char_prob_precision: int
    ) -> None:
        self.length_bytes = length_bytes
        self.char_nbr_bytes = char_nbr_bytes
        self.char_bytes = char_bytes
        self.pb_bytes = pb_bytes
        self.char_prob_precision = char_prob_precision

    def get_char_prob_precision(self) -> int:
        return self.char_prob_precision

    def get_header(self, file: TextIO) -> dict:
        """
        Generate header containing character frequencies and sequence length.
        """

        pb = Counter()
        length = 0
        for line in file:
            pb.update(line)
            length += len(line)
        result = {
            "pb": {char: freq * self.char_prob_precision // length for char, freq in pb.items()},
            "char_nbr": len(pb),
            "sequence_length": length,
        }
        # need to complete values due to rounding
        if result["pb"]:
            result["pb"][list(result["pb"].keys())[
                0]] += self.char_prob_precision - sum(result["pb"].values())

        return result

    @staticmethod
    def get_header_cumulated(header: dict) -> dict:
        """
        Convert character probabilities into cumulative probabilities.
        """

        result = header.copy()
        cumulated = {}
        min_value = 0

        for char, prob in header["pb"].items():
            max_value = min_value + prob
            cumulated[char] = {"min": min_value, "max": max_value}
            min_value = max_value

        result["pb"] = cumulated
        return result

    def encode_header(self, header: dict, dest_file: BinaryIO) -> None:
        """
        Write header to the output file.
        """
        dest_file.write(header["sequence_length"].to_bytes(
            self.length_bytes, byteorder="big", signed=False))
        dest_file.write(header["char_nbr"].to_bytes(
            self.char_nbr_bytes, byteorder="big", signed=False))

        for char, pb in header["pb"].items():
            dest_file.write(ord(char).to_bytes(
                self.char_bytes, byteorder="big", signed=False))
            dest_file.write(pb.to_bytes(
                self.pb_bytes, byteorder="big", signed=False))

    def decode_header(self, src_file: BinaryIO) -> dict:
        """
        Read and reconstruct the header from the input file.
        """

        header = {
            "sequence_length": int.from_bytes(src_file.read(self.length_bytes), "big"),
            "char_nbr": int.from_bytes(src_file.read(self.char_nbr_bytes), "big"),
            "pb": {}
        }

        for _ in range(header["char_nbr"]):
            char = chr(int.from_bytes(src_file.read(
                self.char_bytes), byteorder="big", signed=False))
            value = int.from_bytes(src_file.read(
                self.pb_bytes), byteorder="big", signed=False)
            header["pb"][char] = value

        return header
