import sys

LITERAL = 0
DIGIT = 1
ALNUM = 2
POS_CHAR_GROUP = 3
NEG_CHAR_GROUP = 4

numbers = list("0123456789")
alphanum = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")


# Matches exactly one instance of next_token
# Returns False or what's left of the input
def match_one(input_line, token, pattern):
    if token == DIGIT:
        if input_line[0] in numbers:
            return input_line[1:]
        else:
            return False
    elif token == ALNUM:
        if input_line[0] in alphanum:
            return input_line[1:]
        else:
            return False
    elif token == LITERAL:
        if input_line[0] == pattern[0]:
            return input_line[1:]
        else:
            return False
    elif token == POS_CHAR_GROUP:
        inclusion = pattern[1 : pattern.index("]")]
        if input_line[0] in list(inclusion):
            return input_line[1:]
        else:
            return False
    elif token == NEG_CHAR_GROUP:
        exclusion = pattern[2 : pattern.index("]")]
        if input_line[0] not in list(exclusion):
            return input_line[1:]
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
    elif pattern[0] == "[":
        return POS_CHAR_GROUP, pattern[pattern.index("]") + 1 :]
    else:
        return LITERAL, pattern[1:]


# Can match multiple of next_token
def match_multiple(input_line, token, pattern):
    result = match_one(input_line, token, pattern)
    return False


def match_pattern(input_line, pattern, latest_token_satisfied):
    while input_line:
        if pattern == "":
            return True
        next_token, remaining_pattern = determine_next_token(pattern)
        if input_line == "" and remaining_pattern == "" and latest_token_satisfied:
            return True
        result = match_one(input_line, next_token, pattern)
        if result == False:
            input_line = input_line[1:]
        else:
            input_line = result
            pattern = remaining_pattern
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