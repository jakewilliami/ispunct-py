import unicodedata

from ispunct.bits import clo, cttz
from ispunct.reinterpret import reinterpret_as_uint

CATEGORY_CODE_DATA = {
    "Cn": 0,
    "Lu": 1,
    "Ll": 2,
    "Lt": 3,
    "Lm": 4,
    "Lo": 5,
    "Mn": 6,
    "Mc": 7,
    "Me": 8,
    "Nd": 9,
    "Nl": 10,
    "No": 11,
    "Pc": 12,
    "Pd": 13,
    "Ps": 14,
    "Pe": 15,
    "Pi": 16,
    "Pf": 17,
    "Po": 18,
    "Sm": 19,
    "Sc": 20,
    "Sk": 21,
    "So": 22,
    "Zs": 23,
    "Zl": 24,
    "Zp": 25,
    "Cc": 26,
    "Cf": 27,
    "Cs": 28,
    "Co": 29,
}

UTF8PROC_CATEGORY_PC = 12
UTF8PROC_CATEGORY_PO = 18


def ismalformed(c: str) -> bool:
    """
    Determine if a character is malformed (non-Unicode).

    Inspired by Julia's `ismalformed` function:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/char.jl#L96-L102>
    """
    u = reinterpret_as_uint(c, bitwidth=32)
    l1 = clo(u, bitwidth=32) << 3
    t0 = cttz(u, bitwidth=32) & 56
    return (
        (l1 == 8)
        | (l1 + t0 > 32)
        | (((u & 0x00C0C0C0) ^ 0x00808080) >> t0 != 0)
    )


def category_code(c: str) -> int:
    """
    Get the Unicode category code for the given character.

    Inspired by Julia's `category_code` function:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/strings/unicode.jl#L356-L363>
    """
    if not ismalformed(c):
        category = unicodedata.category(c)
        code = CATEGORY_CODE_DATA.get(category, 31)
        return code if ord(c) <= 0x10FFF else 30

    return 31
