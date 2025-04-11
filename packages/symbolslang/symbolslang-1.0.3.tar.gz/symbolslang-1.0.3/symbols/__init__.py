import os
import re
import json
import subprocess
import sys
from .c_executor import execute_c_code  # Import the C executor module

# Automatically add the module's parent directory to PATH
module_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(module_dir)
if parent_dir not in os.environ["Path"]:
    os.environ["Path"] += os.pathsep + parent_dir


class symlink():
    """
    Represents a symbolic link to a symbols file. Provides methods to connect to and execute algorithms.
    """
    def __init__(self, path):
        """
        Initialize the symlink object.

        Args:
            path (str): The path to the symbols file.
        """
        self.path = path
        if os.path.exists(self.path):
            self.path_exists = True
        else:
            self.path_exists = False
        self.symbols_processor = symbols(path)  # Initialize the symbols processor

    def connect(self, linkname, *args, **kwargs):
        """
        Connect to an algorithm from the symbols file or process the linkname argument.

        Args:
            linkname (str): The name of the algorithm to execute or a string representing a link.
            *args: Positional arguments to pass to the algorithm.
            **kwargs: Keyword arguments to pass to the algorithm.

        Returns:
            The result of the algorithm execution or None if linkname is not an algorithm.
        """
        self.linkname = linkname
        if self.path_exists:
            # Compile the symbols file to populate self.symbols_processor.data
            self.symbols_processor.compile()

            # Check if the linkname corresponds to an algorithm in the symbols file
            if linkname in self.symbols_processor.data:
                # Execute the algorithm with the provided arguments
                return self.symbols_processor.execute(*args, funcname=linkname)
            else:
                # If linkname is not an algorithm, treat it as a string or other type
                print(f"Connected to link: {linkname}")
                return None
        else:
            raise FileNotFoundError(f"The path '{self.path}' does not exist.")


class symbols():
    """
    Represents a symbols processor for compiling and executing algorithms defined in a symbols file.
    """
    def __init__(self, path):
        """
        Initialize the symbols processor.

        Args:
            path (str): The path to the symbols file.
        """
        self.path = path
        self.data = []
        module_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(module_dir)
        if parent_dir not in os.environ["Path"]:
           os.environ["Path"] += os.pathsep + parent_dir  # Initialize the data attribute
        if os.path.exists(self.path):
            self.path_exists = True
        else:
            self.path_exists = False

    def compile(self):
        """
        Compile the symbols file into executable algorithms.

        Raises:
            FileNotFoundError: If the symbols file does not exist.
            ValueError: If the symbols file does not start with 'symbols'.
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"The file '{self.path}' does not exist. Please ensure the file is in the correct location.")
        
        with open(self.path, 'r') as f:
            self.filedata = f.read()
        self.data = []  # Reset the data attribute during compilation
        algorithm_folder = '.algorithm'
        mapping_file = os.path.join(algorithm_folder, 'mapping.json')

        # Ensure the .algorithm folder exists
        if not os.path.exists(algorithm_folder):
            os.makedirs(algorithm_folder)

        # Load or initialize the mapping
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r') as map_file:
                file_mapping = json.load(map_file)
        else:
            file_mapping = {}

        has_function = False  # Track if at least one function is declared
        lines = self.filedata.splitlines()

        # Ensure the first line is 'symbols'
        if not lines or lines[0] != 'symbols':
            raise ValueError("The first line of the file must be 'symbols'.")

        imports = []  # Track imports for the algorithm file
        for i, line in enumerate(lines[1:]):  # Skip the 'symbols' line
            line = line.rstrip()
            if line.startswith('import math'):
                # Handle math imports for C
                if line == 'import math.*' or line == 'import math':
                    imports.append('#include <math.h>')  # Add math.h for C
                continue  # Skip to the next line

            if line.startswith('function ') and line.endswith(')'):
                has_function = True  # Mark that a function is declared
                match = re.match(r'function (\w+)\((.*?)\)', line)
                if match:
                    funcname = match.group(1)  # Extracted function name
                    args = match.group(2)      # Extracted arguments (e.g., "num1, num2" or "*args")
                    self.data.append(funcname)  # Store the function name
                    self.data.append(args)      # Store the arguments

                    # Extract lines belonging to this function
                    algorithm_code = []
                    for subsequent_line in lines[i + 2:]:  # Start from the next line
                        subsequent_line = subsequent_line.strip()
                        if subsequent_line.startswith('function '):
                            break  # Stop processing when another function is encountered
                        if not subsequent_line:  # Skip empty lines
                            continue
                        if re.match(r'.+\s[+\-*/]\s.+\s=\s.+', subsequent_line):
                            # Transform chained expressions into valid C code
                            expressions = subsequent_line.split(' = ')
                            for j, expr in enumerate(expressions):
                                if j == 0:
                                    algorithm_code.append(f"result = {expr.strip()};")
                                else:
                                    algorithm_code.append(f"result = {expr.strip().replace('args', 'result')};")
                        elif subsequent_line.startswith("return"):
                            # Handle return statements
                            return_expr = subsequent_line.replace("return", "").strip()
                            if return_expr == "args":
                                # Skip "return args" if named arguments are used
                                continue
                            elif return_expr:
                                algorithm_code.append(f"result = {return_expr};")
                        else:
                            # Handle standalone expressions (e.g., args/100)
                            algorithm_code.append(f"result = {subsequent_line};")

                    # Replace named arguments in the algorithm code
                    if args and args != "*args":
                        arg_names = [arg.strip() for arg in args.split(",")]
                        for idx, arg_name in enumerate(arg_names):
                            algorithm_code = [line.replace(arg_name, f"num{idx + 1}") for line in algorithm_code]

                    # Add imports to the top of the algorithm code
                    algorithm_code = imports + algorithm_code

                    # Save the algorithm code to a file in the .algorithm folder
                    base_filename = os.path.splitext(os.path.basename(self.path))[0]
                    algorithm_filename = f"{base_filename}_{funcname}.txt"
                    algorithm_filepath = os.path.join(algorithm_folder, algorithm_filename)
                    with open(algorithm_filepath, 'w') as algo_file:
                        algo_file.write("\n".join(algorithm_code))

                    # Update the mapping
                    file_mapping[f"{self.path}:{funcname}"] = algorithm_filename

        # If no function is declared, provide a user-friendly message
        if not has_function:
            print(f"Warning: No functions declared in the file '{self.path}'. Compilation skipped.")
            return

        # Save the updated mapping
        with open(mapping_file, 'w') as map_file:
            json.dump(file_mapping, map_file, indent=4)

    def execute(self, args, funcname=None):
        """
        Execute the specified function or all functions from the symbols file.

        Args:
            args (list): The arguments to pass to the function(s).
            funcname (str): The name of the function to execute. If None, execute all functions.

        Returns:
            The result of the function execution or a dictionary of results for all functions.

        Raises:
            FileNotFoundError: If the mapping file or algorithm file does not exist.
            ValueError: If the specified function is not found in the mapping.
        """
        algorithm_folder = '.algorithm'
        mapping_file = os.path.join(algorithm_folder, 'mapping.json')

        # Load the mapping to find the corresponding algorithm file(s)
        if not os.path.exists(mapping_file):
            raise FileNotFoundError("Mapping file not found. Please compile the algorithms first.")

        with open(mapping_file, 'r') as map_file:
            file_mapping = json.load(map_file)

        # If funcname is provided, execute only the specified function
        if funcname:
            key = f"{self.path}:{funcname}"
            if key not in file_mapping:
                raise ValueError(f"No algorithm found for the function '{funcname}' in the file '{self.path}'. Please compile it first.")

            algorithm_filename = file_mapping[key]
            algorithm_filepath = os.path.join(algorithm_folder, algorithm_filename)

            # Ensure the algorithm file exists
            if not os.path.exists(algorithm_filepath):
                raise FileNotFoundError(f"Algorithm file '{algorithm_filepath}' not found.")

            # Execute the algorithm using C
            return self._execute_in_c(algorithm_filepath, args)

        # If funcname is not provided, execute all functions
        results = {}
        for key, algorithm_filename in file_mapping.items():
            if not key.startswith(f"{self.path}:"):
                continue  # Skip functions not belonging to this file

            current_funcname = key.split(":")[1]  # Extract the function name
            algorithm_filepath = os.path.join(algorithm_folder, algorithm_filename)

            # Ensure the algorithm file exists
            if not os.path.exists(algorithm_filepath):
                raise FileNotFoundError(f"Algorithm file '{algorithm_filepath}' not found.")

            # Execute the algorithm using C
            results[current_funcname] = self._execute_in_c(algorithm_filepath, args)

        return results

    def _execute_in_c(self, algorithm_filepath, args):
        """
        Execute the algorithm using the C executor module.

        Args:
            algorithm_filepath (str): The path to the algorithm file.
            args (list): The arguments to pass to the algorithm.

        Returns:
            The result of the algorithm execution.
        """
        # Read the algorithm file
        with open(algorithm_filepath, 'r') as algo_file:
            algorithm_code = algo_file.read()

        # Use the C executor module to execute the code
        return execute_c_code(algorithm_code, args)


