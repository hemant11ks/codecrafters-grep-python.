import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match(original_input_line, input_line, pattern):
    if pattern[0] == "^":
        return match_pattern(original_input_line, input_line, pattern[1:])
    for i in range(len(input_line)):
        if match_pattern(original_input_line, input_line[i:], pattern):
            return True
    return False


def match_plus(original_input_line, input_line, pattern, pattern_idx):
    # if pattern[0] != "." and input_line[0] != pattern[0]:
    #     return False

    return match_pattern(original_input_line, input_line[1:], pattern) or match_pattern(
        original_input_line,
        input_line[1:],
        pattern[pattern_idx:],
    )


group_str = {}
groups = []


def match_pattern(original_input_line, input_line, pattern):
    if not pattern:
        return True

    if not input_line:
        return pattern in ["$", ")"]

    if pattern[0] == ")":
        if not groups:
            return False
        group_end_idx = len(original_input_line) - len(input_line)
        group_number, group_start_idx = groups.pop()
        group_str[group_number] = original_input_line[group_start_idx:group_end_idx]
        return match_pattern(
            original_input_line,
            input_line,
            pattern[1:],
        )

    if pattern[0] == "(":
        right_paren_idx = 1
        for i in range(1, len(pattern)):
            right_paren_idx = i
            if pattern[i] == ")":
                break

        group_number = len(group_str) + 1
        group_str.setdefault(group_number, "")
        group_start_idx = len(original_input_line) - len(input_line)
        groups.append((group_number, group_start_idx))

        if "|" in pattern[1:right_paren_idx]:
            for group_pattern in pattern[1:right_paren_idx].split("|"):
                if match_pattern(
                    original_input_line,
                    input_line,
                    group_pattern + pattern[right_paren_idx:],
                ):
                    return True
        else:
            if match_pattern(
                original_input_line,
                input_line,
                pattern[1:],
            ):
                return True

        return False

    if pattern[0] == "\\" and pattern[1].isdigit():
        group_pattern = group_str[int(pattern[1])]
        return match_pattern(
            original_input_line,
            input_line,
            group_pattern + pattern[2:],
        )

    if len(pattern) > 1 and pattern[1] == "+":
        if pattern[0] != "." and input_line[0] != pattern[0]:
            return False
        return match_plus(original_input_line, input_line, pattern, 2)

    if len(pattern) > 1 and pattern[1] == "?":
        if input_line[0] == pattern[0]:
            return match_pattern(
                original_input_line,
                input_line[1:],
                pattern[2:],
            )

        return match_pattern(original_input_line, input_line, pattern[2:])

    if pattern[0] == "." or pattern[0] == input_line[0]:
        return match_pattern(
            original_input_line,
            input_line[1:],
            pattern[1:],
        )

    if pattern[:2] == "\\d" and input_line[0].isdigit():
        if len(pattern) > 2 and pattern[2] == "+":
            return match_plus(
                original_input_line,
                input_line,
                pattern,
                3,
            )
        return match_pattern(
            original_input_line,
            input_line[1:],
            pattern[2:],
        )

    if pattern[:2] == "\\w" and (input_line[0].isalnum() or input_line[0] == "_"):
        if len(pattern) > 2 and pattern[2] == "+":
            return match_plus(
                original_input_line,
                input_line,
                pattern,
                3,
            )
        return match_pattern(
            original_input_line,
            input_line[1:],
            pattern[2:],
        )

    if pattern[0] == "[":
        right_bracket_idx = 1
        for i in range(1, len(pattern)):
            right_bracket_idx = i
            if pattern[i] == "]":
                break
        if pattern[1] == "^":
            if (
                input_line[0].isalnum()
                and input_line[0] not in pattern[2:right_bracket_idx]
            ):
                if (
                    right_bracket_idx < len(pattern) - 1
                    and pattern[right_bracket_idx + 1] == "+"
                ):
                    return match_plus(
                        original_input_line,
                        input_line,
                        pattern,
                        right_bracket_idx + 2,
                    )
                return match_pattern(
                    original_input_line,
                    input_line[1:],
                    pattern[right_bracket_idx + 1 :],
                )
        else:
            if input_line[0] in pattern[1:right_bracket_idx]:
                if (
                    right_bracket_idx < len(pattern) - 1
                    and pattern[right_bracket_idx + 1] == "+"
                ):
                    return match_plus(
                        original_input_line,
                        input_line,
                        pattern,
                        right_bracket_idx + 2,
                    )
                return match_pattern(
                    original_input_line,
                    input_line[1:],
                    pattern[right_bracket_idx + 1 :],
                )
    return False


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    # echo -n "abc-def is abc-def, not efg, abc, or def" | ./your_program.sh -E "(([abc]+)-([def]+)) is \1, not ([^xyz]+), \2, or \3"
    # input_line = "abc-def is abc-def, not efg, abc, or def"
    # pattern = "(([abc]+)-([def]+)) is \\1, not ([^xyz]+), \\2, or \\3"
    # Uncomment this block to pass the first stage
    if match(input_line, input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()