import sys

LITERAL = 0
DIGIT = 1
ALNUM = 2
POS_CHAR_GROUP = 3
NEG_CHAR_GROUP = 4
START_ANCHOR = 5  # new

numbers = list("0123456789")
alphanum = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")


def match_one(input_line, token, pattern, at_start):
    if token == DIGIT:
        return input_line[1:] if input_line and input_line[0] in numbers else False
    elif token == ALNUM:
        return input_line[1:] if input_line and input_line[0] in alphanum else False
    elif token == LITERAL:
        return input_line[1:] if input_line and input_line[0] == pattern[0] else False
    elif token == POS_CHAR_GROUP:
        inclusion = pattern[1 : pattern.index("]")]
        return input_line[1:] if input_line and input_line[0] in inclusion else False
    elif token == NEG_CHAR_GROUP:
        exclusion = pattern[2 : pattern.index("]")]
        return input_line[1:] if input_line and input_line[0] not in exclusion else False
    elif token == START_ANCHOR:
        return input_line if at_start else False
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
    at_start = True
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
            at_start = False
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
