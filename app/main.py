import string
import sys

def find_matching_paren(pattern):
    """Find the index of the matching closing parenthesis for the first '('."""
    depth = 0
    for i, ch in enumerate(pattern):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def split_alternatives(pattern):
    """Split a pattern inside (...) by top-level | (not inside nested groups)."""
    parts, buf, depth = [], "", 0
    for ch in pattern:
        if ch == "(":
            depth += 1
            buf += ch
        elif ch == ")":
            depth -= 1
            buf += ch
        elif ch == "|" and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    return parts


def match_here(input_line, pattern):
    """Recursive function that checks whether input_line matches pattern."""
    if pattern == "":
        return True

    if pattern == "$" and input_line == "":
        return True

    if input_line == "":
        return False

    # ------------------------
    # Handle '+' quantifier
    # ------------------------
    if len(pattern) >= 2 and pattern[1] == "+":
        atom = pattern[0]
        # Case: group repetition
        if atom == "(":
            close_index = find_matching_paren(pattern)
            if close_index == -1:
                raise ValueError("invalid pattern: missing ')'")
            group = pattern[:close_index + 1]   # "(...)" including )
            rest = pattern[close_index + 2:]    # skip over )+
            # Must match the group at least once
            if not match_here(input_line, group):
                return False
            pos = 0
            while pos <= len(input_line):
                if match_here(input_line[pos:], rest):
                    return True
                if not match_here(input_line[pos:], group):
                    break
                pos += 1
            return False
        else:
            rest = pattern[2:]
            if not single_match(input_line[0], atom):
                return False
            i = 1
            while i < len(input_line) and single_match(input_line[i], atom):
                if match_here(input_line[i + 1:], rest):
                    return True
                i += 1
            return match_here(input_line[i:], rest)

    # ------------------------
    # Handle '?' quantifier
    # ------------------------
    if len(pattern) >= 2 and pattern[1] == "?":
        atom = pattern[0]
        rest = pattern[2:]
        if match_here(input_line, rest):
            return True
        if single_match(input_line[0], atom):
            return match_here(input_line[1:], rest)
        return False

    # ------------------------
    # Handle groups with alternation ( ... | ... )
    # ------------------------
    if pattern.startswith("("):
        close_index = find_matching_paren(pattern)
        if close_index == -1:
            raise ValueError("invalid pattern: missing ')'")
        inside = pattern[1:close_index]
        rest = pattern[close_index + 1:]
        for alt in split_alternatives(inside):
            if match_here(input_line, alt + rest):
                return True
        return False

    # ------------------------
    # Escape sequences
    # ------------------------
    if pattern.startswith(r"\d"):
        return (input_line[0] in string.digits) and match_here(input_line[1:], pattern[2:])
    if pattern.startswith(r"\w"):
        return (input_line[0] in string.digits + string.ascii_letters + "_") and match_here(input_line[1:], pattern[2:])

    # ------------------------
    # Character class
    # ------------------------
    if pattern.startswith("["):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern: missing ']'")
        if pattern[1] == "^":
            return (input_line[0] not in pattern[2:pattern_end]) and match_here(input_line[1:], pattern[pattern_end + 1:])
        return (input_line[0] in pattern[1:pattern_end]) and match_here(input_line[1:], pattern[pattern_end + 1:])

    # ------------------------
    # Default: literal match
    # ------------------------
    return (input_line[0] == pattern[0]) and match_here(input_line[1:], pattern[1:])


def single_match(ch, atom):
    """Helper: check if one character matches a regex atom."""
    if atom == r"\d":
        return ch in string.digits
    if atom == r"\w":
        return ch in string.digits + string.ascii_letters + "_"
    return ch == atom


def match_pattern(input_line, pattern):
    """Wrapper: match full line with anchors or anywhere else."""
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
