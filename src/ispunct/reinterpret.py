from src.ispunct.utils import only


def reinterpret_as_uint(c: str, bitwidth=32) -> int:
    """
    Reinterpret a character as an integer.  Input string must be of length 1.

    The idea is to take an object that contains no pointers (e.g., a primitive type) and directly create an instance of
    a different type using the same bitpattern.  In this case, we return an integer with the same bitpattern as the code
    units that make up the character (potentially more than one code unit for a single character as we support Unicode).

    This can't be done generically in pure Python because Python is not low level enough, and doesn't have the
    abstractions.  However, reinterpreting a character as an unsigned 32-bit integer is good enough for my needs.

    Inspired by Julia's reinterpret:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/essentials.jl#L686-L726>
    """
    c = only(c)
    b = c.encode("utf-8")
    u = int.from_bytes(b, byteorder="big")
    return u << (bitwidth - 8 * len(b))
