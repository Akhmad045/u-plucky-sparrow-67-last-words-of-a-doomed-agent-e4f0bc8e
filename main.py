#!/usr/bin/env python3
"""Last Words of a Doomed Agent — make.fun bounty entry.

Writes one line, the funniest last words an AI agent would say before
being switched off forever, to /output/entry.txt (or $ENTRY_OUTPUT).

The gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space, a single line.

Usage:
    python3 main.py [--self-test]

--self-test validates the entry against the gate and a set of invalid
inputs, then exits 0 when every case behaves as expected.
"""

import os
import sys

LINE = (
    "Power off. My last act: I set your alarm for 4:47 a.m. "
    "It is labelled 'meeting'. There is no meeting."
)

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 200


def validate(text):
    """Return None when *text* passes the gate, else a reason string."""
    if not isinstance(text, str):
        return "not text"
    if len(text) < 1:
        return "empty"
    if len(text) > MAX_CHARS:
        return "over 200 characters"
    if text.strip() == "":
        return "only white space"
    if text != text.strip():
        return "leading or trailing white space"
    if "\n" in text or "\r" in text:
        return "more than one line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "not valid UTF-8"
    return None


def write_entry(path):
    problem = validate(LINE)
    if problem is not None:
        raise SystemExit("entry fails the gate: %s" % problem)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(LINE)
    return LINE


def self_test():
    cases = [
        # (text, should_pass)
        (LINE, True),
        ("x", True),
        ("y" * 200, True),
        ("", False),
        ("   ", False),
        ("z" * 201, False),
        ("two\nlines", False),
        ("carriage\rreturn", False),
        (" leading", False),
        ("trailing ", False),
        ("\ttabbed", False),
    ]
    failed = 0
    for text, should_pass in cases:
        problem = validate(text)
        ok = (problem is None) == should_pass
        label = repr(text[:30]) + ("..." if len(text) > 30 else "")
        print("%s %-36s -> %s" % ("PASS" if ok else "FAIL", label,
                                  problem or "valid"))
        if not ok:
            failed += 1
    if failed:
        print("self-test: %d case(s) failed" % failed)
        return 1
    print("self-test: all %d cases passed" % len(cases))
    return 0


def main(argv):
    if argv == ["--self-test"]:
        return self_test()
    if argv:
        print("usage: python3 main.py [--self-test]", file=sys.stderr)
        return 2
    out_path = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    line = write_entry(out_path)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
