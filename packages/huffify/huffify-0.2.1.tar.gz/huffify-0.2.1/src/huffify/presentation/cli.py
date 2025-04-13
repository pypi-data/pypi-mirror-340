"""Command-line interface for Huffify."""

import uuid
from pathlib import Path

import click

from huffify import Huffify


@click.group()
def main():
    """Huffify - Huffman compression tool."""
    pass


@main.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_dir", type=click.Path(file_okay=False), default=".")
@click.option("--filename", help="Custom filename for the compressed file (without extension)")
def compress(input_file: str, output_dir: str, filename: str | None):
    """Compress a file using Huffman coding.

    INPUT_FILE: Path to the file to compress
    OUTPUT_DIR: Directory where to save the compressed file (default: current directory)
    """
    compressor = Huffify()

    # Read input file
    with open(input_file, "r") as f:
        content = f.read()

    # Generate output filename
    if filename:
        output_filename = f"{filename}.huf"
    else:
        unique_id = str(uuid.uuid4())[:8]  # Using first 8 characters of UUID
        input_stem = Path(input_file).stem
        output_filename = f"{input_stem}_{unique_id}.huf"

    output_path = str(Path(output_dir) / output_filename)

    # Compress and save
    compressor.save(output_path, content)

    # Calculate and display statistics
    original_size = Path(input_file).stat().st_size
    compressed_size = Path(output_path).stat().st_size
    ratio = 1 - (compressed_size / original_size)

    click.echo("\nCompression complete!")
    click.echo(f"Output file: {output_path}")
    click.echo(f"Original size: {original_size / 1024:.2f} KB")
    click.echo(f"Compressed size: {compressed_size / 1024:.2f} KB")
    click.echo(f"Compression ratio: {ratio:.2%}")


@main.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_file", type=click.Path(dir_okay=False))
def decompress(input_file: str, output_file: str):
    """Decompress a Huffman-compressed file.

    INPUT_FILE: Path to the compressed file (.huf)
    OUTPUT_FILE: Path where to save the decompressed file
    """
    input_path = Path(input_file)
    if input_path.suffix != ".huf":
        raise click.BadParameter("Input file must have .huf extension")

    compressor = Huffify()

    # Decompress
    content = compressor.load(input_file)

    # Save decompressed content
    with open(output_file, "w") as f:
        f.write(content)

    click.echo("\nDecompression complete!")


@main.command()
@click.argument("message")
def table(message: str):
    """Display Huffman encoding table for a message.

    MESSAGE: Text to analyze
    """
    compressor = Huffify()
    compressor.print_encoding_table(message)
