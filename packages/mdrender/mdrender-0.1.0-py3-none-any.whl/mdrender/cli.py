#!/usr/bin/env python3
"""
mdrender - A streaming Markdown renderer for terminal using the rich library.

This script is intended to be invoked like:

    cat test.md | mdrender

It reads from stdin line-by-line (i.e. in a streaming fashion) and
renders Markdown using rich, but it buffers lines for “special blocks” such
as code fences, lists, tables, or blockquotes so that they are rendered properly.
Normal lines (including headers) are flushed immediately.
"""

import sys
import re
import argparse
from rich.console import Console
from rich.markdown import Markdown

def parse_args():
    parser = argparse.ArgumentParser(
        prog="mdrender",
        description="Stream Markdown input and render it beautifully in your terminal using Rich.",
        epilog="Usage example: cat test.md | mdrender"
    )
    parser.add_argument('--debug', required=False, action='store_true')
    return parser.parse_args()

console = Console()

# Global variable for code block tracking.
# Use a count to handle blocks inside blocks (like when rendering ```markdown blocks)
code_fence_count = 0

def render(text):
    """Render Markdown text."""
    md = Markdown(text, code_theme="monokai")
    console.print(md)

def flush_buffer(buffer):
    """Render the accumulated lines if there is any content."""
    if buffer:
        block = "".join(buffer)
        # Only render if there is non-empty content.
        if block.strip():
            render(block)
        buffer.clear()

def is_header(line):
    """Return True if the line is a Markdown header."""
    return line.lstrip().startswith("#")

def is_code_fence_start(line):
    """Return True if the line is a code fence start"""
    return True if re.match(r"^[`]{3,4}(\w+)$", line.strip()) else False

def is_code_fence_end(line):
    """Return True if the line is a code fence end"""
    return True if re.match(r"^[`]{3,4}$", line.strip()) else False

def in_code_block():
    """Return True if the line is currently inside a code block"""
    return code_fence_count > 0

def is_list_line(line):
    """Return True if the line starts with a common list marker."""
    # Remove leading whitespace.
    stripped = line.lstrip()
    # Unordered list markers.
    if stripped.startswith(("* ", "- ", "+ ")):
        return True
    # Ordered list: e.g., "1. " or "1) " (a simple heuristic)
    if re.match(r"\d+[\.\)]\s+", stripped):
        return True
    return False

def is_blockquote(line):
    """Return True if the line starts with a blockquote marker."""
    return line.lstrip().startswith(">")

def is_table_line(line):
    """Return True if the line looks like a table row (contains '|' with non-blank items)."""
    # This is a heuristic: if the line contains a pipe and some text around it.
    if "|" in line:
        # Also catch markdown table separator lines.
        if re.match(r"\s*[-:| ]+\s*$", line):
            return True
        # Or if there's text on each side.
        return True
    return False

def is_horizontal_rule(line):
    """Return True if the line is a horizontal rule."""
    stripped = line.strip()
    return stripped in ("---", "***", "___")

def is_special_line(line):
    """
    Determines if a line is considered part of a special block.
    For our purposes, if it’s a code fence, a list line, a blockquote,
    a table row, or a horizontal rule, we treat it as special.
    """
    if is_code_fence_start(line):
        return True
    if is_code_fence_end(line):
        return True
    if in_code_block():
        return True
    if is_list_line(line):
        return True
    if is_blockquote(line):
        return True
    if is_table_line(line):
        return True
    if is_horizontal_rule(line):
        return True
    return False

def is_normal_line(line):
    """
    A “normal” line is one that is not identified as a special line.
    (Headers are treated as normal, so they are rendered immediately.)
    Blank lines are considered normal.
    """
    return not is_special_line(line)

def run():
    args = parse_args()  # Automatically shows help if -h/--help is used
    buffer = []  # Buffer for accumulating special block lines.
    global code_fence_count

    for line in sys.stdin:
        if is_normal_line(line):
            if args.debug:
                print(f'[Normal Line] {repr(line)}')
            # Flush any existing buffer
            flush_buffer(buffer)
            # If line is simply newline just use normal print
            # (the renderer doesn't work properly for just newlines for some reason)
            if line == '\n':
                print()
            # If not, render it
            else:
                render(line)
        else:
            if args.debug:
                print(f'[Special Line] {repr(line)}')
            # For code fences, we use a state tracker
            if is_code_fence_start(line):
                # If not inside a code block already,
                # change code fence delimiter to four backsticks instead of three
                if not in_code_block():
                    line = line.replace('```', '````')
                code_fence_count += 1 # Increase global count
            elif is_code_fence_end(line):
                code_fence_count -= 1 # Decrease global count
                # If not inside a code block anymore,
                # change code fence delimiter to four backsticks instead of three
                if not in_code_block():
                    line = line.replace('```', '````')
            # Add line to buffer
            buffer.append(line)

    # End of input; flush any remaining buffer.
    flush_buffer(buffer)
