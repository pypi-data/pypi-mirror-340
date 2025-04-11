# Symbols

Symbols is a CLI tool for compiling and executing symbols files. It allows you to process and execute algorithms defined in custom `.sym` files.

## Features

- Compile `.sym` files into executable algorithms.
- Execute specific functions or all functions from a `.sym` file.
- Easy-to-use CLI interface.

## Requirements

- **Python 3.8+**
- **GCC**: Required for compiling the generated C code.

## Installation

Install the package using pip:

```bash
pip install symbols
```

## Usage

### Compile a `.sym` File

```bash
symbols compile <filename>
```

### Execute a Function

```bash
symbols execute <filename> <funcname> <args>
```

- `<filename>`: Path to the `.sym` file.
- `<funcname>`: Name of the function to execute. If omitted, all functions will be executed.
- `<args>`: Arguments to pass to the function(s).

### Example

```bash
symbols compile file.sym
symbols execute file.sym add 10
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
