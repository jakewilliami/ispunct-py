# `ispunct`

A small Python library for checking whether a character is a punctuation character.

---

## Quick Start

```python
from ispunct import ispunct

assert ispunct("?")
assert not ispunct("a")
assert ispunct("‽")
```

## Using `ispunct` as a Library

This package is not published on PyPI, but you can use it from Git.  For example, if using [UV](https://github.com/astral-sh/uv/) for dependency management, you could write:

```commandline
$ uv add "ispunct @ git+https://github.com/jakewilliami/ispunct-py"
```

## Notes on Internal Functionality

This library also implements (and uses internally) bitwise functions to calculate the number of leading/trailing zeros/ones in the bitwise representation of a Python integer.  We also compute a Python integer that has the same bitpattern as a given character (i.e., simulating Julia's `bitcast`).

## Citation

If your research depends on `ispunct`, please consider giving us a formal citation: [`citation.bib`](./citation.bib).
