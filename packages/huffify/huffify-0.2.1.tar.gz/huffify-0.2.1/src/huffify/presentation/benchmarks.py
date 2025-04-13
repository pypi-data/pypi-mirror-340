import os
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from huffify import Huffify
from huffify.core.file_manager import Picklefier


@dataclass
class CompressionStats:
    original_size: int
    compressed_size: int
    compression_ratio: float
    compression_time: float
    decompression_time: float

    def __str__(self) -> str:
        return (
            f"Original size: {self.original_size / 1024:.2f} KB\n"
            f"Compressed size: {self.compressed_size / 1024:.2f} KB\n"
            f"Compression ratio: {self.compression_ratio:.2%}\n"
            f"Compression time: {self.compression_time:.3f} s\n"
            f"Decompression time: {self.decompression_time:.3f} s"
        )


class HuffmanBenchmark:
    TEMP_DIR = Path("benchmark_samples")
    TEMP_COMPRESSED_FILE = "temp_compressed"

    def __init__(self):
        self.compressor = Huffify(file_manager=Picklefier)
        self.test_data: Dict[str, str] = {
            "repeated_text": "The sun shines bright today. " * 10000,
            "random_text": "".join(chr(i) for i in range(32, 127)) * 1000,
            "single_char": "a" * 10000,
            "binary_like": "01" * 5000,
        }

    def setup(self):
        """Setup benchmark environment and create sample files"""
        self._create_sample_files()

    def cleanup(self):
        """Clean up all temporary files and directories"""
        try:
            # Remove temporary compressed file if exists
            if os.path.exists(self.TEMP_COMPRESSED_FILE):
                os.remove(self.TEMP_COMPRESSED_FILE)

            # Remove benchmark samples directory if exists
            if self.TEMP_DIR.exists():
                shutil.rmtree(self.TEMP_DIR)

            print("\nCleanup completed successfully.")
        except Exception as e:
            print(f"\nError during cleanup: {e}")

    def _create_sample_files(self):
        """Create sample files with different characteristics"""
        self.TEMP_DIR.mkdir(exist_ok=True)

        # Text samples
        with open(self.TEMP_DIR / "lorem_ipsum.txt", "w") as f:
            f.write(self._get_lorem_ipsum() * 100)

        with open(self.TEMP_DIR / "code.py", "w") as f:
            f.write(self._get_sample_code() * 50)

        with open(self.TEMP_DIR / "json_data.json", "w") as f:
            f.write(self._get_sample_json() * 100)

    def _get_lorem_ipsum(self) -> str:
        return """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
        nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        """

    def _get_sample_code(self) -> str:
        return """
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def quick_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
        """

    def _get_sample_json(self) -> str:
        return """
{
    "id": 123456,
    "name": "Sample Product",
    "price": 99.99,
    "description": "This is a sample product description with some repeated text",
    "categories": ["electronics", "gadgets", "accessories"],
    "metadata": {
        "created_at": "2024-03-20T10:30:00Z",
        "updated_at": "2024-03-20T15:45:00Z",
        "version": "1.0.0"
    }
}
        """

    def measure_compression(self, data: str) -> CompressionStats:
        try:
            # Measure original size
            original_size = len(data.encode("utf-8"))

            # Measure compression
            start_time = time.time()
            self.compressor.save(self.TEMP_COMPRESSED_FILE, data)
            compression_time = time.time() - start_time

            # Get compressed size
            compressed_size = os.path.getsize(self.TEMP_COMPRESSED_FILE)

            # Measure decompression
            start_time = time.time()
            self.compressor.load(self.TEMP_COMPRESSED_FILE)
            decompression_time = time.time() - start_time

            return CompressionStats(
                original_size=original_size,
                compressed_size=compressed_size,
                compression_ratio=1 - (compressed_size / original_size),
                compression_time=compression_time,
                decompression_time=decompression_time,
            )
        finally:
            # Clean up temporary compressed file
            if os.path.exists(self.TEMP_COMPRESSED_FILE):
                os.remove(self.TEMP_COMPRESSED_FILE)

    def benchmark_predefined_data(self) -> Dict[str, CompressionStats]:
        results = {}
        for name, data in self.test_data.items():
            print(f"\nBenchmarking {name}...")
            results[name] = self.measure_compression(data)
        return results

    def benchmark_files(self) -> Dict[str, CompressionStats]:
        results = {}

        for file_path in self.TEMP_DIR.glob("*"):
            if file_path.is_file():
                print(f"\nBenchmarking {file_path.name}...")
                with open(file_path, "r") as f:
                    data = f.read()
                results[file_path.name] = self.measure_compression(data)

        return results

    def print_results(self, results: Dict[str, CompressionStats]):
        print("\n=== Compression Benchmark Results ===\n")
        for name, stats in results.items():
            print(f"\n--- {name} ---")
            print(stats)


def main():
    benchmark = HuffmanBenchmark()

    try:
        # Setup benchmark environment
        print("Setting up benchmark environment...")
        benchmark.setup()

        # Run benchmarks
        print("\nRunning predefined data benchmarks...")
        predefined_results = benchmark.benchmark_predefined_data()
        benchmark.print_results(predefined_results)

        print("\nRunning file benchmarks...")
        file_results = benchmark.benchmark_files()
        benchmark.print_results(file_results)

    except Exception as e:
        print(f"\nError during benchmarking: {e}")
    finally:
        # Always cleanup, even if an error occurred
        benchmark.cleanup()


if __name__ == "__main__":
    main()
