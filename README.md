# `ispunct`

A small Python library for checking whether a character is a punctuation character.

---

## Quick Start

```python
from ispunct import ispunct

assert ispunct('?')
assert not ispunct('a')
assert ispunct('‽')
```

## Notes on Internal Functionality

This library also implements (and uses internally) bitwise functions to calculate the number of leading/trailing zeros/ones in the bitwise representation of a Python integer.  We also compute a Python integer that has the same bitpattern as a given character (i.e., simulating Julia's `bitcast`).
