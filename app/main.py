import sys


# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern, must_match_now=False):
    # Debug investigation
    print(f"{input_line:>50} | {pattern:>20}")

    # Termination
    if len(pattern) == 0:
        return True
    if len(input_line) == 0:
        return False

    # Recurrence: tries to find 1st element of pattern
    # We build input_line_next and pattern_next that will be used for the next match_pattern call
    current_char, input_line_next, pattern_used, matched = input_line[0], input_line[1:], '', False
    if pattern.startswith(r"\d"):
        pattern_used, matched = r"\d", match_digit(current_char)
    elif pattern.startswith(r"\w"):
        pattern_used, matched = r"\w", match_alphanumeric(current_char)
    elif pattern[0] == '[':
        closingBracketIndex = pattern.index(']')
        pattern_used = pattern[:closingBracketIndex + 1]
        matched = (pattern[1] == '^' and match_negative_character_group(current_char, pattern[2:closingBracketIndex])) \
                  or \
                  (pattern[1] != '^' and match_positive_character_group(current_char, pattern[1:closingBracketIndex]))
    elif pattern[0] == '.':
        pattern_used, matched = '.', True
    elif pattern[0] == '(':
        closingParenthesisIndex = pattern.index(')')
        pattern_used = pattern[:closingParenthesisIndex + 1]
        or_patterns = pattern_used[1:-1].split('|')
        # Not the most efficient but we "fork" until the end of the full pattern for each of them
        end_pattern = pattern[len(pattern_used):]
        for p in or_patterns:
            if match_pattern(input_line, p + end_pattern):
                return True
        return False
    else:
        # We perform direct match
        pattern_used, matched = pattern[0], current_char == pattern[0]
    if must_match_now and not matched:
        return False

    # Check for modifier
    if len(pattern) > len(pattern_used):
        if matched and pattern[len(pattern_used)] == '+':
            while match_pattern(input_line_next, pattern_used):
                input_line_next = input_line_next[1:]
            pattern_used = pattern[:len(pattern_used) + 1]  # We also matched the + modifier
        if pattern[len(pattern_used)] == '?':  # regardless of pattern matched or not => it is a match for ?
            if not matched:  # we should not move to the next character as this pattern was optional
                input_line_next = input_line
            pattern_used, matched = pattern[:len(pattern_used) + 1], True

    pattern_next = pattern
    if matched:
        pattern_next = pattern[len(pattern_used):]
    if pattern_next == '$':
        return input_line_next == ''
    return match_pattern(input_line_next, pattern_next)


def match_digit(input_line):
    # return any([str(d) in input_line for d in range(10)])
    return match_positive_character_group(input_line, '0123456789')


def match_alphanumeric(input_line):
    # return any([w in input_line for w in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'])
    return match_positive_character_group(input_line, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789')


def match_positive_character_group(input_line, character_group):
    # Ref.: https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-classes-in-regular-expressions#positive-character-group--
    return any([c in character_group for c in input_line])


def match_negative_character_group(input_line, character_group):
    # Ref.: https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-classes-in-regular-expressions#negative-character-group-
    return any([c not in character_group for c in input_line])


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if len(pattern) == 0:
        return True

    must_match_now = False
    if pattern[0] == '^':
        pattern = pattern[1:]
        must_match_now = True

    if match_pattern(input_line, pattern, must_match_now):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()