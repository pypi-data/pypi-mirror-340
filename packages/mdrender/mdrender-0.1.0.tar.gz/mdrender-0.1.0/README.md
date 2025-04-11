# mdrender

A streaming Markdown renderer for your terminal, great to render the output of LLM tools.
It reads from stdin and prints formatted Markdown in real time, buffering blocks (like code fences, tables, lists) so they render properly.

## Features

- Handles streamed input line-by-line
- Supports headers, lists, nested lists
- Syntax-highlighted code fences
- Tables, blockquotes, inline styles

## Installation

```bash
pip install mdrender
```

## Usage

Send markdown content via stdin

```bash
cat file.md | mdrender
```

Of course, the main goal is to able to render streaming input.
For example, to render the live output produced by a [LLM](https://github.com/simonw/llm) chat:

```bash
llm 'generate a dummy markdown' | mdrender
```

You can simulate streaming with the following bash one-liner:

```bash
cat test.md | while IFS= read -r line; do for (( i=0; i<${#line}; i++ )); do echo -n "${line:$i:1}" && sleep 0.001; done; echo; done | mdrender
```

> I actually use that to test the tool while developing
> (with the [test file](mdrender/test.md) at `mdrender/test.md`)
