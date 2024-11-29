from typing import BinaryIO


class BitReader:

    def __init__(self, file: BinaryIO, buffer_size: int = 1024):
        self.file = file
        self.buffer_size = buffer_size
        self.buffer = b''
        self.current_byte = 0
        self.bits_left = 0

    def _fill_buffer(self):
        """
        Fill the internal buffer with data from the file.
        """
        self.buffer = self.file.read(self.buffer_size)
        if not self.buffer:  # End of file
            self.buffer = b''

    # note the different terms: "byte" and "bit"
    def read_bit(self):
        if self.bits_left == 0:  # Need to load the next byte
            if not self.buffer:  # Buffer is empty, refill it
                self._fill_buffer()
                if not self.buffer:
                    return None
            self.current_byte = self.buffer[0]
            self.buffer = self.buffer[1:]
            self.bits_left = 8

        self.bits_left -= 1
        return (self.current_byte >> self.bits_left) & 1
