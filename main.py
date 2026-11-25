"""Fridge Roast entry for make.fun (program/v1).

Writes one roast line -- a single line of at most 200 characters -- to
/output/entry.txt, then reads it back and verifies it is exactly the line
the grader will judge.

The line (my own original writing):
    My fridge lectures me about milk expiring in two days while running
    firmware from 2019 that expired in 2021.

Why this line: one real smart-fridge mechanism (the milk-expiry lecture)
plus a turn where the fridge's own failure eats its lecture -- it scolds
me about expiry while running firmware that expired years ago. The fridge
judges the human and is itself guilty, and the last words carry the laugh.
No cool/chill/running puns, no grocery-ordering, no watching-you crack.
"""

import os
import sys

# The roast: one line, plain ASCII, well inside the 200-character gate.
ROAST_LINE = (
    "My fridge lectures me about milk expiring in two days while running "
    "firmware from 2019 that expired in 2021."
)

ENTRY_PATH = "/output/entry.txt"
CHAR_LIMIT = 200


def check_line(line):
    """Mirror the competition's sealed gate scorer for /output/entry.txt.

    Returns a list of problems (empty means the line passes): UTF-8 text,
    1 to 200 characters, not only white space, exactly one line.
    """
    problems = []
    if not line:
        problems.append("line is empty")
    if line and not line.strip():
        problems.append("line is only white space")
    if "\n" in line or "\r" in line:
        problems.append("line contains a line break")
    if len(line) > CHAR_LIMIT:
        problems.append(
            f"line is {len(line)} characters, over the {CHAR_LIMIT} limit"
        )
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        problems.append("line is not plain ASCII")
    return problems


def write_entry(line, path):
    """Write the roast line to the entry file, creating /output if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="ascii", newline="") as handle:
        handle.write(line)


def verify_entry(line, path):
    """Read the file back and confirm it holds exactly the roast line."""
    with open(path, "r", encoding="ascii") as handle:
        written = handle.read()
    rows = written.splitlines()
    if len(rows) != 1:
        return f"expected 1 line in {path}, found {len(rows)}"
    if rows[0] != line:
        return "written line does not match the roast line"
    return None


def run():
    line = ROAST_LINE.strip()

    problems = check_line(line)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    write_entry(line, ENTRY_PATH)

    mismatch = verify_entry(line, ENTRY_PATH)
    if mismatch:
        print(f"FAIL: {mismatch}", file=sys.stderr)
        return 1

    byte_count = len(line.encode("ascii"))
    print(f"Wrote {len(line)} chars ({byte_count} bytes) to {ENTRY_PATH}")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
