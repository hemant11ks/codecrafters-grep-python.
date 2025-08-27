import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_plus(text, match, regexp):
    while text and text[0] == match:
        text = text[1:]
        if match_here(text, regexp):
            return True
    return False


def match_question_mark(text, match, regexp):
    return (
        match_here(text[1:], regexp) if text[0] == match else match_here(text, regexp)
    )


def match_here(text, regexp):
    if regexp == "":
        return True
    if regexp and not text:
        return regexp == "$"
    if text == "":
        return False
    if len(regexp) == 1:
        return regexp == text[0]
    if len(regexp) > 1 and regexp[1] == "?":
        return match_question_mark(text, regexp[0], regexp[2:])
    if len(regexp) > 1 and regexp[1] == "+":
        return match_plus(text, regexp[0], regexp[2:])
    if regexp[0] == ".":
        return match_here(text[1:], regexp[1:])
    if r"\d" == regexp[:2] and text[0].isdigit():
        return match_here(text[1:], regexp[2:])
    if r"\w" == regexp[:2] and text[0].isalnum():
        return match_here(text[1:], regexp[2:])
    if regexp[0] == "(" and regexp[-1] == ")":
        patterns = regexp[1:-1].split("|")
        return any(match_here(text, p) for p in patterns)
    if regexp[0] == text[0]:
        return match_here(text[1:], regexp[1:])
    else:
        return False


def match_pattern(input_line, pattern):
    if pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            return all(c not in input_line for c in pattern[2:-1])
        return any(c in input_line for c in pattern[1:-1])
    if pattern[0] == "^":
        return match_here(input_line, pattern[1:])
    while input_line:
        if match_here(input_line, pattern):
            return True
        input_line = input_line[1:]
    return False


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()