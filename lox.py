#!/usr/bin/env python

from pathlib import Path
import sys

from scanner import Scanner
from errors import had_error, reset_error


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    # For now, just print the tokens.
    for token in tokens:
        print(token)


def run_file(filename: str):
    script = Path(filename).read_text()
    run(script)
    if had_error():
        sys.exit(65)


def run_prompt():
    while True:
        try:
            line = input("> ")
            reset_error()
        except EOFError:
            break
        run(line)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: lox.py [script]")
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()
