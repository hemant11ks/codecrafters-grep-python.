import sys
from pathlib import Path
try:
    from .execution_engine import *
except ImportError:
    from execution_engine import *

# import pyparsing - available if you need it!
# import lark - available if you need it!

def main():
    files = []
    if sys.argv[1] == "-r":
        if sys.argv[2] != "-E":
            print("Expected second argument to be '-E'")
            exit(1)
        pattern = sys.argv[3]
        directory = sys.argv[4]
        path = Path(directory)
        for txt_file in path.rglob("*.txt"):
            files.append(txt_file)
    else:
        if sys.argv[1] != "-E":
            print("Expected first argument to be '-E'")
            exit(1)
        
        pattern = sys.argv[2]

        for arg in sys.argv[3:]:
            if arg != "-E":
                files.append(arg)

    any_match = False
    for file in files:
        try:
            with open(file, 'r') as f:
                input_lines = f.readlines()
        except FileNotFoundError:
            print(f"File not found: {file}")
            exit(1)
        
        for input_line in input_lines:
            input_line = input_line.rstrip('\n')
            result = False
            try:
                parser = Regexparser(pattern)
                ast = parser.parse()

                engine = ExecutionEngine(ast, input_line)
                if pattern != input_line:
                    result = engine.execute()
                else:
                    result = True
            except ValueError as ve:
                pass

            if result:
                if len(files) > 1:
                    print(f"{file}:{input_line}")
                else:
                    print(input_line)

                any_match = True
    
    if len(files) == 0:
        input_line = sys.stdin.read()
        result = False
        try:
            parser = Regexparser(pattern)
            ast = parser.parse()

            engine = ExecutionEngine(ast, input_line)
            if pattern != input_line:
                result = engine.execute()
            else:
                result = True
        except ValueError as ve:
            exit(1)

        if result:
            exit(0)
        else:
            exit(1)


    if not any_match:
        exit(1)


if __name__ == "__main__":
    main()