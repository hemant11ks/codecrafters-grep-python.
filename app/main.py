import string
import sys

def match_here(input_line, pattern):
    """
    Recursive function that checks whether the beginning of input_line
    matches the given regex pattern.
    """

    # Base case: empty pattern always matches
    if pattern == "":
        return True

    # If pattern ends with $, match only if input_line is empty
    if pattern == "$" and input_line == "":
        return True

    # If pattern remains but input string is empty => no match
    if input_line == "":
        return False

    # ------------------------
    # Handle '+' quantifier: one or more occurrences of preceding atom
    # Example: a+ matches "a", "aa", "aaa", etc.
    # ------------------------
    if len(pattern) >= 2 and pattern[1] == "+":
        atom = pattern[0]         # the character/atom before '+'
        rest = pattern[2:]        # remaining pattern after '+'

        # First character must match the atom at least once
        if not single_match(input_line[0], atom):
            return False

        # Consume as many repetitions as possible (greedy match)
        i = 1
        while i < len(input_line) and single_match(input_line[i], atom):
            # Recursive call: try matching the rest of the pattern
            if match_here(input_line[i + 1:], rest):
                return True
            i += 1

        # If loop ends, try matching remaining input with rest
        return match_here(input_line[i:], rest)

    # ------------------------
    # Handle '?' quantifier: zero or one occurrence of preceding atom
    # Example: a? matches "" or "a"
    # ------------------------
    if len(pattern) >= 2 and pattern[1] == "?":
        atom = pattern[0]
        rest = pattern[2:]

        # Case 1: Skip atom (zero occurrence)
        if match_here(input_line, rest):
            return True

        # Case 2: Consume one atom if it matches
        if single_match(input_line[0], atom):
            return match_here(input_line[1:], rest)

        return False

    # ------------------------
    # Handle escape sequences and character classes
    # ------------------------

    # \d => digit [0-9]
    if pattern.startswith(r"\d"):
        return (input_line[0] in string.digits) and match_here(
            input_line[1:], pattern[2:]
        )

    # \w => word character [0-9a-zA-Z_]
    if pattern.startswith(r"\w"):
        return (
            input_line[0] in string.digits + string.ascii_letters + "_"
        ) and match_here(input_line[1:], pattern[2:])

    # Character class [...]
    if pattern.startswith("["):
        pattern_end = pattern.find("]")  # find closing bracket
        if pattern_end == -1:
            raise ValueError("invalid pattern: missing ']'")

        # Case 1: Negated class [^...]
        if pattern[1] == "^":
            return (
                input_line[0] not in pattern[2:pattern_end]
            ) and match_here(input_line[1:], pattern[pattern_end + 1 :])

        # Case 2: Normal class [...]
        return (
            input_line[0] in pattern[1:pattern_end]
        ) and match_here(input_line[1:], pattern[pattern_end + 1 :])

    # ------------------------
    # Default case: literal match
    # ------------------------
    return (input_line[0] == pattern[0]) and match_here(
        input_line[1:], pattern[1:]
    )


def single_match(ch, atom):
    """
    Helper: check if a single character `ch` matches a regex atom.
    Supported atoms: literal, \d, \w
    """
    if atom == r"\d":
        return ch in string.digits
    if atom == r"\w":
        return ch in string.digits + string.ascii_letters + "_"
    return ch == atom


def match_pattern(input_line, pattern):
    """
    Wrapper function: checks whether the entire input matches the regex pattern.
    Supports '^' (start of string) anchor.
    """
    # If pattern starts with ^, must match from the beginning
    if pattern.startswith("^"):
        return match_here(input_line, pattern[1:])

    # Otherwise, search pattern anywhere in the string
    while len(input_line) > 0:
        if match_here(input_line, pattern):
            return True
        # Shift window: try next substring
        input_line = input_line[1:]

    return False


def main():
    """
    Entry point for CLI usage.
    Usage: ./your_program.sh -E "pattern"
    Reads input from stdin and matches against pattern.
    """
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    # Ensure correct flag is provided
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # Match and exit with proper code
    if match_pattern(input_line, pattern):
        exit(0)
    exit(1)


if __name__ == "__main__":
    main()
