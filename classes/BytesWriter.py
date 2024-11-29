from typing import BinaryIO


class BytesWriter:

    def __init__(self, file: BinaryIO) -> None:
        self.file = file

    def write_bytes(self, bits: list[int]) -> list[int]:
        if not all(bit in {0, 1} for bit in bits):
            raise ValueError("The bits list must contain only 0s and 1s.")

        # Calculate the number of complete bytes
        bytes_nbr = len(bits) // 8
        if not bytes_nbr:
            return bits

        bytes_to_write = bits[:bytes_nbr * 8]
        remaining_bits = bits[bytes_nbr * 8:]

        # Convert bits to bytes and write them to the file
        byte_values = [
            int(''.join(map(str, bytes_to_write[i:i + 8])), 2)
            for i in range(0, len(bytes_to_write), 8)
        ]
        self.file.write(bytes(byte_values))

        return remaining_bits

    def write_remaining_bytes(self, bits: list[int]) -> None:
        if bits:
            while len(bits) % 8 != 0:
                bits.append(0)
            self.write_bytes(bits)
