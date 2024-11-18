from typing import TypeVar, Iterable

T = TypeVar("T")


def only(x: Iterable[T]) -> T:
    """
    Helper method to return the one and only element of a collection `x`, and throws a `ValueError` if the collection
    has zero or multiple elements.

    Inspired by Julia's `only` function:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/iterators.jl#L1500-L1549>
    """
    itr = iter(x)
    i = next(itr, None)

    if i is None:
        raise ValueError("Collection is empty; must contain exactly  element")
    if next(itr, None) is not None:
        raise ValueError(
            "Collection has multiple elements; must contain exactly 1 element"
        )

    return i
