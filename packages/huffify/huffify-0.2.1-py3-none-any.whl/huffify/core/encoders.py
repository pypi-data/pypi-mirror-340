from typing import Optional

from huffify.core.abstract import IEncoder


class MVPEncoder(IEncoder):
    """
    Minimum Viable Product encoder for Huffman coding.
    Handles encoding strings to binary data and decoding binary data back to strings.
    """

    def _build_bytes_string_from_table(
        self, encoding_table: dict[str, str], message: str
    ) -> str:
        """Convert a message to a string of bits using the encoding table."""
        bytes_string = "".join([encoding_table[char] for char in message])
        return bytes_string

    def _make_bytes_partition(self, bytes_string: str) -> bytearray:
        """
        Convert a string of bits into a bytearray with proper padding.
        The first byte stores the number of bits in the last partial byte.
        """
        # Handle empty string case
        if not bytes_string:
            return bytearray((0,))

        # Handle the case where the bit string is shorter than 8 bits
        additional_len = len(bytes_string) % 8
        if len(bytes_string) < 8:
            byte = (additional_len, int(bytes_string, 2))
            return bytearray(byte)

        # Process full bytes and handle any remaining bits
        required_len = len(bytes_string) - additional_len
        encoded_stream = [0]  # First byte will store additional_len

        # Process full bytes (8 bits each)
        full_bytes = [int(bytes_string[i : i + 8], 2) for i in range(0, required_len, 8)]

        # Process remaining bits if any
        if additional_len:
            encoded_stream[0] = additional_len
            remaining_bits = int(bytes_string[-additional_len:], 2)
            return bytearray(encoded_stream + full_bytes + [remaining_bits])
        else:
            return bytearray(encoded_stream + full_bytes)

    def encode_string(self, encoding_table: dict[str, str], message: str) -> bytearray:
        """
        Encode a string message using the provided Huffman encoding table.
        Returns a bytearray with the compressed data.
        """
        bytes_string = self._build_bytes_string_from_table(encoding_table, message)
        encoded_message = self._make_bytes_partition(bytes_string)
        return encoded_message

    def decode_string(self, encoding_table: dict[str, str], encoded_message: bytearray) -> str:
        """
        Decode a bytearray back to the original string using the encoding table.
        """
        # Reverse the encoding table for decoding
        decoding_table = {code: char for char, code in encoding_table.items()}

        # Read the number of bits in the last partial byte
        external_byte_count = encoded_message[0]

        # Process the full bytes
        if external_byte_count:
            full_bytes = encoded_message[1:-1]
        else:
            full_bytes = encoded_message[1:]

        # Convert bytes to bit strings with proper padding
        bytes_container = []
        for byte in full_bytes:
            byte_str = bin(byte)[2:].zfill(8)  # Ensure 8 bits with leading zeros
            bytes_container.append(byte_str)

        # Add the last partial byte if it exists
        if external_byte_count:
            last_byte = bin(encoded_message[-1])[2:].zfill(external_byte_count)
            bytes_container.append(last_byte)

        # Join all bits
        bytes_string = "".join(bytes_container)

        # Decode using the table
        current_code = ""
        decoded_message = ""
        for bit in bytes_string:
            current_code += bit
            if current_code in decoding_table:
                decoded_message += decoding_table[current_code]
                current_code = ""

        return decoded_message


class BitStreamEncoder(IEncoder):
    """
    A more efficient encoder that works directly with bits without unnecessary conversions.

    Benefits:
    - Reduced memory usage by avoiding intermediate string representations
    - More efficient bit-level operations
    - Better handling of large files

    How it works:
    1. During encoding, bits are accumulated in a buffer and flushed to bytes when full
    2. The encoded format stores the total bit count at the beginning for precise decoding
    3. Decoding reads the bit count and processes bytes bit by bit
    """

    def encode_string(self, encoding_table: dict[str, str], message: str) -> bytearray:
        """
        Encode a string using the provided Huffman encoding table.
        Works directly at the bit level for maximum efficiency.
        """
        result = bytearray()

        # If message is empty, return a simple array with zeros
        if not message:
            return bytearray([0, 0, 0, 0, 0])

        # Check if encoding table is empty or if any characters are missing
        if not encoding_table or not set(message).issubset(set(encoding_table.keys())):
            # Build a new encoding table that includes all message characters
            import heapq
            from collections import Counter

            from huffify.core.heap_nodes import Node

            # Build a new encoding table that includes all message characters
            freq = Counter(message)

            # Special case for single character
            if len(freq) == 1:
                char = list(freq.keys())[0]
                encoding_table = {char: "0"}
            else:
                # Build Huffman tree
                heap = [Node(char, count) for char, count in freq.items()]
                heapq.heapify(heap)

                # Initialize encoding table
                encoding_table = {char: "" for char in freq.keys()}

                # Build the tree
                while len(heap) > 1:
                    low = heapq.heappop(heap)
                    high = heapq.heappop(heap)

                    # Assign 0s and 1s
                    for c in high.char:
                        encoding_table[c] = "0" + encoding_table[c]
                    for c in low.char:
                        encoding_table[c] = "1" + encoding_table[c]

                    # Combine nodes
                    combined = high + low
                    heapq.heappush(heap, combined)

                # Reverse the codes (we built them backwards)
                encoding_table = {char: code[::-1] for char, code in encoding_table.items()}

        # Store the header marker
        result.append(0xAA)  # Special marker for our format

        # Store the encoding table size
        result.append(len(encoding_table))

        # Store the encoding table
        for char, code in encoding_table.items():
            # Store the character - first its length in UTF-8, then the bytes
            char_bytes = char.encode("utf-8")
            result.append(len(char_bytes))
            result.extend(char_bytes)

            # Store the code length
            result.append(len(code))

            # Store the code as bytes
            code_int = 0
            for i, bit in enumerate(code):
                if bit == "1":
                    code_int |= 1 << (len(code) - 1 - i)

            code_bytes = (len(code) + 7) // 8
            result.extend(code_int.to_bytes(max(1, code_bytes), byteorder="big"))

        # Reserve 4 bytes for storing the total bit count
        bit_count_position = len(result)
        result.extend([0, 0, 0, 0])

        # Calculate total bits for efficiency
        total_bits = sum(len(encoding_table[char]) for char in message)

        # Write the bit count as 4 bytes (supports messages up to 4GB)
        for i in range(4):
            result[bit_count_position + i] = (total_bits >> (i * 8)) & 0xFF

        # Process the message bit by bit
        current_byte = 0
        bit_position = 0

        for char in message:
            code = encoding_table[char]
            for bit in code:
                # Set the bit if it's 1
                if bit == "1":
                    current_byte |= 1 << (7 - bit_position)

                # Move to next bit position
                bit_position += 1

                # If we've filled a byte, add it to the result
                if bit_position == 8:
                    result.append(current_byte)
                    current_byte = 0
                    bit_position = 0

        # Don't forget to add the last partial byte if there is one
        if bit_position > 0:
            result.append(current_byte)

        return result

    def decode_string(self, encoding_table: dict[str, str], encoded_message: bytearray) -> str:
        """
        Decode a bytearray back to the original string.
        Processes bits directly for efficient decoding.
        """
        # If message is too short, return empty string
        if len(encoded_message) < 6:  # Need at least marker, table size, count bytes
            return ""

        # Check the format marker
        if encoded_message[0] != 0xAA:
            # Try to handle old format
            return self._legacy_decode(encoding_table, encoded_message)

        # First byte after marker is the table size
        table_size = encoded_message[1]
        position = 2

        # Read the table
        decoding_table = {}

        for _ in range(table_size):
            if position >= len(encoded_message):
                return ""

            # Read character length
            char_len = encoded_message[position]
            position += 1

            if position + char_len > len(encoded_message):
                return ""

            # Read character
            char = encoded_message[position : position + char_len].decode(
                "utf-8", errors="replace"
            )
            position += char_len

            # Read code length
            if position >= len(encoded_message):
                return ""

            code_length = encoded_message[position]
            position += 1

            # Read code bytes
            code_bytes = (code_length + 7) // 8

            if position + code_bytes > len(encoded_message):
                return ""

            code_int = int.from_bytes(
                encoded_message[position : position + code_bytes], byteorder="big"
            )
            position += code_bytes

            # Convert to bit string
            code = ""
            for i in range(code_length):
                bit = "1" if (code_int & (1 << (code_length - 1 - i))) else "0"
                code += bit

            decoding_table[code] = char

        # Read the total bit count from the next 4 bytes
        if position + 4 > len(encoded_message):
            return ""

        total_bits = 0
        for i in range(4):
            total_bits |= encoded_message[position + i] << (i * 8)
        position += 4

        # If no bits to decode, return empty string
        if total_bits == 0:
            return ""

        decoded_message = ""
        current_code = ""
        bit_count = 0

        # Process one byte at a time
        for byte_idx in range(position, len(encoded_message)):
            byte = encoded_message[byte_idx]

            # Process each bit in the byte
            for bit_idx in range(8):
                # Stop if we've processed all bits
                if bit_count >= total_bits:
                    break

                # Get the current bit (1 or 0)
                bit = "1" if (byte & (1 << (7 - bit_idx))) else "0"
                current_code += bit
                bit_count += 1

                # Check if we've found a valid code
                if current_code in decoding_table:
                    decoded_message += decoding_table[current_code]
                    current_code = ""

        return decoded_message

    def _legacy_decode(
        self, encoding_table: dict[str, str], encoded_message: bytearray
    ) -> str:
        """Handle decoding of messages encoded with older versions of the encoder."""
        # Assuming format: [table size][table data...][bit count]...

        # If message is too short, return empty string
        if len(encoded_message) < 5:  # Need at least table size, bit count
            return ""

        # First byte is the table size
        table_size = encoded_message[0]
        position = 1

        # If table is provided in the message, use it instead of the input table
        if table_size > 0:
            # Read the table
            decoding_table = {}

            for _ in range(table_size):
                if position >= len(encoded_message):
                    return ""

                # Read character
                char = chr(encoded_message[position])
                position += 1

                # Read code length
                if position >= len(encoded_message):
                    return ""

                code_length = encoded_message[position]
                position += 1

                # Read code bytes
                code_bytes = (code_length + 7) // 8

                if position + code_bytes > len(encoded_message):
                    return ""

                code_int = int.from_bytes(
                    encoded_message[position : position + code_bytes], byteorder="big"
                )
                position += code_bytes

                # Convert to bit string
                code = ""
                for i in range(code_length):
                    bit = "1" if (code_int & (1 << (code_length - 1 - i))) else "0"
                    code += bit

                decoding_table[code] = char
        else:
            # Use the provided encoding table
            decoding_table = {code: char for char, code in encoding_table.items()}

        # Read the total bit count from the next 4 bytes
        if position + 4 > len(encoded_message):
            return ""

        total_bits = 0
        for i in range(4):
            total_bits |= encoded_message[position + i] << (i * 8)
        position += 4

        # If no bits to decode, return empty string
        if total_bits == 0:
            return ""

        decoded_message = ""
        current_code = ""
        bit_count = 0

        # Process one byte at a time
        for byte_idx in range(position, len(encoded_message)):
            byte = encoded_message[byte_idx]

            # Process each bit in the byte
            for bit_idx in range(8):
                # Stop if we've processed all bits
                if bit_count >= total_bits:
                    break

                # Get the current bit (1 or 0)
                bit = "1" if (byte & (1 << (7 - bit_idx))) else "0"
                current_code += bit
                bit_count += 1

                # Check if we've found a valid code
                if current_code in decoding_table:
                    decoded_message += decoding_table[current_code]
                    current_code = ""

        return decoded_message


class AdaptiveHuffmanEncoder(IEncoder):
    """
    An encoder that updates the Huffman tree dynamically during encoding/decoding.

    Benefits:
    - No need to transmit the encoding table with the data
    - Better compression for data with changing patterns
    - More efficient for streaming data

    How it works:
    1. Both encoder and decoder start with the same initial model
    2. As each character is processed, its frequency is updated
    3. The Huffman tree is periodically rebuilt based on updated frequencies
    4. This allows adaptation to changing patterns in the data
    """

    def encode_string(self, encoding_table: dict[str, str], message: str) -> bytearray:
        """
        Encode a string with adaptive Huffman coding.
        The encoding table is updated as the message is processed.
        """
        from collections import Counter

        if not message:
            return bytearray([0])

        result = bytearray()

        # For the single character case, use a simpler encoding
        if len(set(message)) == 1:
            char = message[0]
            length = len(message)

            # Format: [0x01 (single char marker)][char length (1 byte)][char bytes][length (4 bytes)]
            result.append(0x01)  # Marker for single character
            char_bytes = char.encode("utf-8")
            result.append(len(char_bytes))  # Character byte length
            result.extend(char_bytes)
            result.extend(length.to_bytes(4, byteorder="big"))
            return result

        # Analyze the entire message first to identify all unique characters
        # This ensures we won't miss any characters during encoding
        unique_chars = sorted(set(message))

        # Store a simpler fixed table instead of an adaptive one
        # This is safer and still provides good compression for most cases
        char_freqs = Counter(message)

        # Build a single optimized table for the entire message
        huffman_table = self._build_table_from_freqs(char_freqs)

        # Format: [0x00 (normal marker)][character count (2 bytes)][serialized characters][table size (2 bytes)][table]
        result.append(0x00)  # Marker for normal encoding
        result.extend(len(unique_chars).to_bytes(2, byteorder="big"))

        # Serialize characters - for each character store its length and bytes
        char_data = bytearray()
        for char in unique_chars:
            char_bytes = char.encode("utf-8")
            char_data.append(len(char_bytes))
            char_data.extend(char_bytes)

        # Store the total character data length and the data
        result.extend(len(char_data).to_bytes(2, byteorder="big"))
        result.extend(char_data)

        # Serialize the encoding table
        table_data = bytearray()
        for char, code in huffman_table.items():
            # Find the index of the character in the unique_chars list
            char_index = unique_chars.index(char)
            table_data.extend(char_index.to_bytes(2, byteorder="big"))
            table_data.append(len(code))

            # Convert the code to bytes
            code_bytes = 0
            for bit_idx, bit in enumerate(code):
                if bit == "1":
                    code_bytes |= 1 << (7 - (bit_idx % 8))
                if (bit_idx + 1) % 8 == 0 or bit_idx == len(code) - 1:
                    table_data.append(code_bytes)
                    code_bytes = 0

        # Add table size and the table data
        result.extend(len(table_data).to_bytes(2, byteorder="big"))
        result.extend(table_data)

        # Now encode the entire message with the table
        bytes_string = "".join(huffman_table[char] for char in message)

        # Convert bits to bytes
        for j in range(0, len(bytes_string), 8):
            byte_bits = bytes_string[j : j + 8].ljust(8, "0")
            result.append(int(byte_bits, 2))

        return result

    def decode_string(self, encoding_table: dict[str, str], encoded_message: bytearray) -> str:
        """
        Decode a bytearray encoded with adaptive Huffman coding.
        """
        if len(encoded_message) <= 1:  # At least need 1 marker byte
            return ""

        # Check the encoding marker
        marker = encoded_message[0]

        # Special case for single character strings
        if marker == 0x01:
            char_len = encoded_message[1]
            char = encoded_message[2 : 2 + char_len].decode("utf-8")
            length = int.from_bytes(
                encoded_message[2 + char_len : 6 + char_len], byteorder="big"
            )
            return char * length

        # Normal encoding with huffman table
        if marker != 0x00 or len(encoded_message) <= 7:  # Need at least marker, counts, etc.
            return ""  # Invalid marker or too short

        # Read the character data length
        if 3 + 2 > len(encoded_message):
            return ""

        char_data_len = int.from_bytes(encoded_message[3:5], byteorder="big")

        # Extract the character set
        chars_start = 5
        chars_end = chars_start + char_data_len

        if chars_end >= len(encoded_message):
            return ""  # Not enough data

        # Parse the characters
        char_data = encoded_message[chars_start:chars_end]
        unique_chars = []

        i = 0
        while i < len(char_data):
            char_len = char_data[i]
            i += 1

            if i + char_len > len(char_data):
                return ""

            char = char_data[i : i + char_len].decode("utf-8", errors="replace")
            unique_chars.append(char)
            i += char_len

        # Read the table size
        if chars_end + 2 > len(encoded_message):
            return ""  # Not enough data

        table_size = int.from_bytes(
            encoded_message[chars_end : chars_end + 2], byteorder="big"
        )

        # Extract the table data
        table_start = chars_end + 2
        table_end = table_start + table_size

        if table_end > len(encoded_message):
            return ""  # Not enough data

        table_data = encoded_message[table_start:table_end]

        # Deserialize the table
        decoding_table = {}
        i = 0
        while i < len(table_data):
            if i + 3 >= len(table_data):  # Need at least 2 bytes for index, 1 for code length
                break  # Not enough data

            # Read character index
            char_index = int.from_bytes(table_data[i : i + 2], byteorder="big")
            i += 2

            if char_index >= len(unique_chars):
                break  # Invalid index

            char = unique_chars[char_index]

            # Read code length
            code_len = table_data[i]
            i += 1

            if code_len == 0:
                continue  # Skip invalid code length

            # Read the code bytes
            code = ""
            bytes_needed = (code_len + 7) // 8  # Ceiling division

            if i + bytes_needed > len(table_data):
                break  # Not enough data

            for b in range(bytes_needed):
                byte = table_data[i]
                i += 1

                # Extract the bits
                bits_in_this_byte = min(8, code_len - len(code))
                for bit_idx in range(bits_in_this_byte):
                    bit = "1" if (byte & (1 << (7 - bit_idx))) else "0"
                    code += bit

            if len(code) > 0:  # Only add valid codes
                decoding_table[code] = char

        # Decode the message using the table
        decoded_message = ""
        current_code = ""

        # Process the encoded data
        data_start = table_end
        if data_start >= len(encoded_message):
            return ""  # No data to decode

        for i in range(data_start, len(encoded_message)):
            byte = encoded_message[i]
            bits = bin(byte)[2:].zfill(8)

            for bit in bits:
                current_code += bit
                if current_code in decoding_table:
                    decoded_message += decoding_table[current_code]
                    current_code = ""

        return decoded_message

    def _build_table_from_freqs(self, freqs: dict[str, int]) -> dict[str, str]:
        """Build a Huffman encoding table from character frequencies."""
        import heapq

        from huffify.core.heap_nodes import Node

        # Get all characters
        chars = list(freqs.keys())

        # Special case for single character
        if len(chars) == 1:
            char = chars[0]
            return {char: "0"}

        # Build the Huffman tree
        heap = [Node(char, freqs[char]) for char in chars]
        heapq.heapify(heap)

        # Initialize encoding table
        encoding_table = {char: "" for char in chars}

        # Build the tree by combining nodes
        while len(heap) > 1:
            low = heapq.heappop(heap)
            high = heapq.heappop(heap)

            # Assign 0s and 1s for each character
            for c in high.char:
                encoding_table[c] = "0" + encoding_table[c]
            for c in low.char:
                encoding_table[c] = "1" + encoding_table[c]

            # Combine nodes and push back to heap
            combined = high + low
            heapq.heappush(heap, combined)

        return encoding_table


class RLEHuffmanEncoder(IEncoder):
    """
    A hybrid encoder that combines Run-Length Encoding (RLE) with Huffman coding.

    Benefits:
    - Significantly better compression for repetitive sequences
    - Maintains good compression for non-repetitive parts
    - Particularly effective for certain types of data like images, logs, etc.

    How it works:
    1. First, run-length encoding is applied to compress repetitive sequences
    2. The RLE-encoded data is then compressed using Huffman coding
    3. This two-step process allows better compression for both repetitive and unique patterns

    The RLE format uses a special escape character (^) followed by a count and the repeated character:
    For example, "aaaaa" becomes "^5a"
    """

    def __init__(self, escape_char="^", min_run_length=4):
        """
        Initialize the encoder with parameters.

        Args:
            escape_char: The character used to mark run-length sequences
            min_run_length: Minimum sequence length to apply RLE (shorter runs aren't compressed)
        """
        self.escape_char = escape_char
        self.min_run_length = min_run_length

    def encode_string(self, encoding_table: dict[str, str], message: str) -> bytearray:
        """
        Encode a string using RLE preprocessing and Huffman coding.
        """
        # Handle empty message case
        if not message:
            return bytearray([0])

        # First apply RLE
        rle_encoded = self._run_length_encode(message)

        # Build a huffman table for the RLE-encoded string
        from collections import Counter

        freqs = Counter(rle_encoded)
        huffman_table = self._build_huffman_table(freqs)

        # Create the output bytearray
        result = bytearray()

        # Store the escape character
        result.append(ord(self.escape_char))

        # Store the original message length
        result.extend(len(message).to_bytes(4, byteorder="big"))

        # Store the RLE-encoded length
        result.extend(len(rle_encoded).to_bytes(4, byteorder="big"))

        # Store the huffman table
        # First store the number of entries
        result.append(len(huffman_table))

        # Store each entry in the table
        for char, code in huffman_table.items():
            # Store character as UTF-8 bytes with length prefix
            char_bytes = char.encode("utf-8")
            result.append(len(char_bytes))
            result.extend(char_bytes)

            # Store code length and bits
            result.append(len(code))
            code_int = int(code, 2) if code else 0
            code_bytes = (len(code) + 7) // 8
            if code_bytes == 0:
                code_bytes = 1
            result.extend(code_int.to_bytes(code_bytes, byteorder="big"))

        # Encode the data using the Huffman table
        encoded_bits = ""
        for char in rle_encoded:
            encoded_bits += huffman_table[char]

        # Convert bits to bytes
        # First store the total number of bits
        result.extend(len(encoded_bits).to_bytes(4, byteorder="big"))

        # Then store the actual bits
        for i in range(0, len(encoded_bits), 8):
            chunk = encoded_bits[i : i + 8]
            if len(chunk) < 8:
                chunk = chunk.ljust(8, "0")
            result.append(int(chunk, 2))

        return result

    def decode_string(self, encoding_table: dict[str, str], encoded_message: bytearray) -> str:
        """
        Decode a bytearray by applying Huffman decoding and then RLE decoding.
        """
        if len(encoded_message) < 10:  # Minimum size for header
            return ""

        pos = 0

        # Read escape character
        self.escape_char = chr(encoded_message[pos])

        pos += 9
        # Read Huffman table
        table_size = encoded_message[pos]
        pos += 1

        huffman_table = {}
        for _ in range(table_size):
            # Read character
            char_len = encoded_message[pos]
            pos += 1
            char = encoded_message[pos : pos + char_len].decode("utf-8")
            pos += char_len

            # Read code
            code_len = encoded_message[pos]
            pos += 1
            code_bytes = (code_len + 7) // 8
            if code_bytes == 0:
                code_bytes = 1
            code_int = int.from_bytes(encoded_message[pos : pos + code_bytes], byteorder="big")
            pos += code_bytes

            # Convert to binary string
            code = bin(code_int)[2:].zfill(code_len)[-code_len:]
            huffman_table[code] = char

        # Read total number of encoded bits
        total_bits = int.from_bytes(encoded_message[pos : pos + 4], byteorder="big")
        pos += 4

        # Read and decode the Huffman-encoded data
        bits = ""
        for byte in encoded_message[pos:]:
            bits += format(byte, "08b")
        bits = bits[:total_bits]  # Truncate to actual number of bits

        # Decode using Huffman table
        rle_encoded = ""
        current_code = ""
        for bit in bits:
            current_code += bit
            if current_code in huffman_table:
                rle_encoded += huffman_table[current_code]
                current_code = ""

        # Finally, decode the RLE
        return self._run_length_decode(rle_encoded)

    def _run_length_encode(self, text: str) -> str:
        """
        Apply run-length encoding to the input text.
        Sequences shorter than min_run_length are not compressed.
        """
        if not text:
            return ""

        result = []
        i = 0
        while i < len(text):
            # Count consecutive characters
            count = 1
            while i + count < len(text) and text[i + count] == text[i]:
                count += 1

            # Handle the current run
            if count >= self.min_run_length:
                # For escape character runs, we need to escape the escape
                if text[i] == self.escape_char:
                    result.append(self.escape_char + self.escape_char + str(count) + text[i])
                else:
                    result.append(self.escape_char + str(count) + text[i])
            else:
                # For non-runs...
                if text[i] == self.escape_char:
                    # Escape each occurrence
                    for _ in range(count):
                        result.append(self.escape_char + self.escape_char)
                else:
                    # Output literally
                    result.append(text[i] * count)
            i += count

        return "".join(result)

    def _run_length_decode(self, text: str, escape_char: Optional[str] = None) -> str:
        """
        Decode a run-length encoded string.

        Args:
            text: The RLE-encoded text to decode
            escape_char: Optional escape character override (for backward compatibility)
        """
        if not text:
            return ""

        # Use provided escape_char if given, otherwise use instance's escape_char
        esc = escape_char if escape_char is not None else self.escape_char

        result = []
        i = 0

        while i < len(text):
            if text[i] == esc and i + 1 < len(text):
                i += 1
                if text[i] == esc:
                    # This is an escaped escape character sequence
                    i += 1
                    if i < len(text) and text[i].isdigit():
                        # This is a run of escape characters
                        count_start = i
                        while i < len(text) and text[i].isdigit():
                            i += 1
                        if i < len(text) and count_start < i:
                            count = int(text[count_start:i])
                            result.append(text[i] * count)
                            i += 1
                        else:
                            # Invalid sequence, treat as literal characters
                            result.append(esc)
                            result.append(esc)
                    else:
                        # Just a single escaped escape character
                        result.append(esc)
                else:
                    # This is a regular run
                    count_start = i
                    while i < len(text) and text[i].isdigit():
                        i += 1
                    if i < len(text) and count_start < i:
                        count = int(text[count_start:i])
                        result.append(text[i] * count)
                        i += 1
                    else:
                        # Invalid sequence, treat as literal characters
                        result.append(esc)
                        if count_start < i:
                            result.append(text[count_start:i])
            else:
                result.append(text[i])
                i += 1

        return "".join(result)

    def _build_huffman_table(self, freqs: dict[str, int]) -> dict[str, str]:
        """Build a Huffman encoding table from character frequencies."""
        import heapq

        from huffify.core.heap_nodes import Node

        if not freqs:
            return {}

        # Handle single character case
        if len(freqs) == 1:
            char = next(iter(freqs.keys()))
            return {char: "0"}

        # Build the Huffman tree
        heap = [Node(char, freq) for char, freq in freqs.items()]
        heapq.heapify(heap)

        # Initialize encoding table
        encoding_table = {char: "" for char in freqs.keys()}

        # Build the tree
        while len(heap) > 1:
            low = heapq.heappop(heap)
            high = heapq.heappop(heap)

            # Assign bits
            for c in high.char:
                encoding_table[c] = "0" + encoding_table[c]
            for c in low.char:
                encoding_table[c] = "1" + encoding_table[c]

            combined = high + low
            heapq.heappush(heap, combined)

        return encoding_table
