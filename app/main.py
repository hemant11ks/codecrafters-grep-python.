import sys

def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    if pattern == "\d":
        return any(char.isdigit() for char in input_line)
    if pattern == "\w":
        return any(char.isalnum() or char == "_" for char in input_line)
    
    # Handle negated character group [^abc]
    if pattern.startswith("[^") and pattern.endswith("]"):
        excluded_chars = pattern[2:-1]
        return any(char not in excluded_chars for char in input_line)

    # Handle positive character group [abc]
    if pattern.startswith("[") and pattern.endswith("]"):
        group_chars = pattern[1:-1]
        return any(char in group_chars for char in input_line)

    # Fallback: simple substring match
    return pattern in input_line


def main():
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    pattern = sys.argv[2]
    input_lines = sys.stdin.read().splitlines()

    matched = False
    for line in input_lines:
        if match_pattern(line, pattern):
            print(line)
            matched = True

    if matched:
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
