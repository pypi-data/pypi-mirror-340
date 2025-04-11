import argparse
from . import symbols

def main():
    """
    Entry point for the CLI. Parses arguments and invokes the appropriate commands.
    """
    parser = argparse.ArgumentParser(description="CLI for compiling and executing symbols.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for the 'compile' command
    compile_parser = subparsers.add_parser("compile", help="Compile the symbols file.")
    compile_parser.add_argument("filename", type=str, help="Path to the symbols file to compile.")

    # Subparser for the 'execute' command
    execute_parser = subparsers.add_parser("execute", help="Execute functions from the symbols file.")
    execute_parser.add_argument("filename", type=str, help="Path to the symbols file to execute.")
    execute_parser.add_argument("funcname", type=str, nargs="?", default=None, help="Name of the function to execute. If not provided, all functions will be executed.")
    execute_parser.add_argument("args", type=str, nargs="*", help="Arguments to pass to the function(s).")

    # Map '-c' to 'compile' and '-e' to 'execute'
    parser.add_argument("-c", "--compile", dest="command", action="store_const", const="compile", help="Shortcut for compile command.")
    parser.add_argument("-e", "--execute", dest="command", action="store_const", const="execute", help="Shortcut for execute command.")

    args = parser.parse_args()

    if args.command == "compile":
        symbols_processor = symbols.symbols(args.filename)
        symbols_processor.compile()
        print(f"Compilation completed for file: {args.filename}")

    elif args.command == "execute":
        symbols_processor = symbols.symbols(args.filename)
        if args.funcname:
            result = symbols_processor.execute(args=args.args, funcname=args.funcname)
            print(f"Result of executing function '{args.funcname}': {result}")
        else:
            results = symbols_processor.execute(args=args.args)
            print("Results of executing all functions:")
            for func, result in results.items():
                print(f"  {func}: {result}")
