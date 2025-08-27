import sys
#git commit -am "[any message]"

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    if pattern == "\d":
        return any(char.isdigit() for char in input_line)
    if pattern == "\w":
        return any(char.isalnum() or char == "_" for char in input_line)
    
    # Handle character group [abc]
    if pattern.startswith("[") and pattern.endswith("]"):
        group_chars = pattern[1:-1]  # everything inside the brackets
        return any(char in group_chars for char in input_line)

    # Handle negated character group [^abc]
      # Negative character group [^abc]
    if pattern.startswith("[^") and pattern.endswith("]"):
        excluded_chars = pattern[2:-1]  # everything after ^ and before ]
        return any(char not in excluded_chars for char in input_line)
    
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
