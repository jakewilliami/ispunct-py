import string

from ispunct.unicode import (
    UTF8PROC_CATEGORY_PC,
    UTF8PROC_CATEGORY_PO,
    category_code,
)
from ispunct.utils import only


def ispunct(c: str) -> int:
    """
    Check whether a given character is a punctuation character.

    Input string must be of length 1.

    Inspired by Julia's `ispunct` function:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/strings/unicode.jl#L531-L549>

    !!! note
        This function should return true wherever the `ispunct` function from C
        returns true.  However, we extend this beyond the cases handled in the
        C function by checking the input character's category code.
    """
    c = only(c)

    # Case 1: efficient check for most common cases
    # https://stackoverflow.com/a/266162/
    if c in string.punctuation:
        return True

    # Case 2: check whether the character's UTF-8 category is part of the
    # punctuation range (categories Po–Pc)
    #
    # NOTE: this case alone does not cover $+<=>^`|~ --- these are in the
    # symbol category.  The base case currently allows our `ispunct` function
    # to be a superset of C's `ispunct`
    return UTF8PROC_CATEGORY_PC <= category_code(c) <= UTF8PROC_CATEGORY_PO
