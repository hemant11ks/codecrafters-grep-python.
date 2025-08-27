import string
import sys


def match_here(input_line, pattern):
    if pattern == "":
        return True
    if pattern == "$" and input_line == "":
        return True
    if input_line == "":
        return False

    # Handle alternation ( ... | ... )
    if pattern.startswith("("):
        depth, closing = 0, -1
        for i, ch in enumerate(pattern):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    closing = i
                    break
        if closing == -1:
            raise ValueError("Unmatched ( in pattern")

        inside = pattern[1:closing]
        rest = pattern[closing + 1:]

        # split on top-level |
        parts, buf, d = [], "", 0
        for c in inside:
            if c == "(":
                d += 1
                buf += c
            elif c == ")":
                d -= 1
                buf += c
            elif c == "|" and d == 0:
                parts.append(buf)
                buf = ""
            else:
                buf += c
        parts.append(buf)

        for option in parts:
            if match_here(input_line, option + rest):
                return True
        return False

    # Handle + quantifier (one or more)
    if len(pattern) >= 2 and pattern[1] == "+":
        atom = pattern[0]
        rest = pattern[2:]
        if not single_match(input_line[0], atom):
            return False
        i = 1
        while i < len(input_line) and single_match(input_line[i], atom):
            if match_here(input_line[i + 1:], rest):
                return True
            i += 1
        return match_here(input_line[i:], rest)

    # Handle ? quantifier (zero or one)
    if len(pattern) >= 2 and pattern[1] == "?":
        atom = pattern[0]
        rest = pattern[2:]
        if match_here(input_line, rest):
            return True
        if single_match(input_line[0], atom):
            return match_here(input_line[1:], rest)
        return False

    # Handle escapes and classes
    if pattern.startswith("\\d"):
        return (input_line[0] in string.digits) and match_here(input_line[1:], pattern[2:])
    if pattern.startswith("\\w"):
        return (input_line[0] in string.digits + string.ascii_letters + "_") and match_here(input_line[1:], pattern[2:])
    if pattern.startswith("["):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        if pattern[1] == "^":
            return (input_line[0] not in pattern[2:pattern_end]) and match_here(
                input_line[1:], pattern[pattern_end + 1:]
            )
        return (input_line[0] in pattern[1:pattern_end]) and match_here(
            input_line[1:], pattern[pattern_end + 1:]
        )

    # Literal match
    return (input_line[0] == pattern[0]) and match_here(input_line[1:], pattern[1:])


def single_match(ch, atom):
    if atom == "\\d":
        return ch in string.digits
    if atom == "\\w":
        return ch in string.digits + string.ascii_letters + "_"
    return ch == atom


def match_pattern(input_line, pattern):
    if pattern.startswith("^"):
        return match_here(input_line, pattern[1:])
    while len(input_line) > 0:
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

    if match_pattern(input_line, pattern):
        exit(0)
    exit(1)


if __name__ == "__main__":
    main()
