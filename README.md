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

This package is published on PyPI.  You can install it with PIP:

```commandline
$ pip add ispunct
```

Or, if using [UV](https://github.com/astral-sh/uv/) for dependency management:

```commandline
$ uv add ispunct
```

## History

The origin of this project comes from an equivalent function to [Julia](https://julialang.org/)'s [`ispunct`](https://github.com/JuliaLang/julia/blob/7fa26f01/base/strings/unicode.jl#L531-L549), which is itself derived from the [C](https://www.c-language.org/) implementation for obtaining a Unicode character's category code.  This is a more complete solution than checking against [`string.punctuation`](https://docs.python.org/3/library/string.html#string.punctuation) or [`curses.ascii.ispunct`](https://docs.python.org/3/library/curses.ascii.html#curses.ascii.ispunct).  There is also [a StackOverflow question for this functionality](https://stackoverflow.com/q/46355466) which [I have answered](https://stackoverflow.com/a/79709763).

## Notes on Internal Functionality

This library also implements (and uses internally) bitwise functions to calculate the number of leading/trailing zeros/ones in the bitwise representation of a Python integer.  We also compute a Python integer that has the same bitpattern as a given character (i.e., simulating Julia's `bitcast`).  These are required in order to determine a character's category code.

## Alternative Libraries

This was written mostly as a proof of concept using bitwise operations on character codes.  You could derive similar functionality from the standard library [`unicodedata`](https://docs.python.org/3/library/unicodedata.html), or matching on character category with [`regex`](https://pypi.org/project/regex/) (see examples [here](https://github.com/jakewilliami/ispunct-py/issues/1#issuecomment-3717021835)).

A spiritual sister package and successor to `ispunct` is [`strip-marks`](https://github.com/jakewilliami/strip-marks-py/), in which we further explore unicode operations in Python.

## Citation

If your research depends on `ispunct`, please consider giving us a formal citation: [`citation.bib`](./citation.bib).
