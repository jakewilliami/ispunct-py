def only(x: str) -> str:
    """
    Helper method to verify that the input `x` has only one element, and throws
    a `TypeError` (albeit an inferred type error) if `x` has zero or multiple
    elements.

    This was previously written in a generalised form, inspired by Julia's
    `only` function:
      <https://github.com/jakewilliami/ispunct-py/blob/68e23c9/src/ispunct/utils.py>

    This function has since (as of v1.0.1) been specialised in the interest of
    more useful error messages.

    Error messages inspired by unicode error messages in CPython:
      <https://github.com/python/cpython/blob/9a21df7c/Python/bltinmodule.c#L2148-L2168>
      <https://github.com/python/cpython/blob/9a21df7c/Modules/clinic/unicodedata.c.h#L178-L184>
    """
    if not isinstance(x, str):
        raise TypeError(
            f"Expected string of length 1, but found {type(x).__name__}"
        )

    itr = iter(x)
    i = next(itr, None)

    if i is None:
        raise TypeError(
            "Expected a single unicode character, but found an empty string"
        )

    if next(itr, None) is not None:
        raise TypeError(
            f"Expected a single unicode character, but found a string of "
            f"length {len(x)}"
        )

    return i
