import sys

LITERAL = 0
DIGIT = 1
ALNUM = 2
POS_CHAR_GROUP = 3
NEG_CHAR_GROUP = 4
START_ANCHOR = 5   # NEW

numbers = list("0123456789")
alphanum = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")


def match_one(input_line, token, pattern, at_start):
    if token == DIGIT:
        if input_line and input_line[0] in numbers:
            return input_line[1:]
        else:
            return False
    elif token == ALNUM:
        if input_line and input_line[0] in alphanum:
            return input_line[1:]
        else:
            return False
    elif token == LITERAL:
        if input_line and input_line[0] == pattern[0]:
            return input_line[1:]
        else:
            return False
    elif token == POS_CHAR_GROUP:
        inclusion = pattern[1 : pattern.index("]")]
        if input_line and input_line[0] in list(inclusion):
            return input_line[1:]
        else:
            return False
    elif token == NEG_CHAR_GROUP:
        exclusion = pattern[2 : pattern.index("]")]
        if input_line and input_line[0] not in list(exclusion):
            return input_line[1:]
        else:
            return False
    elif token == START_ANCHOR:
        # Only matches at very beginning
        if at_start:
            return input_line
        else:
            return False
    else:
        return False


def determine_next_token(pattern):
    if len(pattern) >= 2 and pattern[:2] == "\\d":
        return DIGIT, pattern[2:]
    elif len(pattern) >= 2 and pattern[:2] == "\\w":
        return ALNUM, pattern[2:]
    elif len(pattern) >= 2 and pattern[:2] == "[^":
        return NEG_CHAR_GROUP, pattern[pattern.index("]") + 1 :]
    elif pattern and pattern[0] == "[":
        return POS_CHAR_GROUP, pattern[pattern.index("]") + 1 :]
    elif pattern and pattern[0] == "^":
        return START_ANCHOR, pattern[1:]
    else:
        return LITERAL, pattern[1:]


def match_pattern(input_line, pattern, latest_token_satisfied):
    at_start = True  # Track if we are at beginning
    while True:
        if pattern == "":
            return True
        if input_line == "" and pattern != "":
            return False

        next_token, remaining_pattern = determine_next_token(pattern)
        result = match_one(input_line, next_token, pattern, at_start)

        if result is False:
            return False
        else:
            input_line = result
            pattern = remaining_pattern
            at_start = False  # after consuming first check
    return pattern == ""


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if match_pattern(input_line, pattern, False):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
