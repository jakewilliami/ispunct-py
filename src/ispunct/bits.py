def bitmask(bitwidth: int) -> int:
    """
    Convenience function to generate a bitmask that can be applied to a value to clamp it within the bitwidth.
    """
    return (1 << bitwidth) - 1


def cttz(x: int, bitwidth=32) -> int:
    """
    Count the number of trailing ones in the binary representation of the given input, given a bitwidth (default: 32).

    Inspired by Julia's `trailing_zeros` function:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/int.jl#L441>
    """
    if x == 0:
        return bitwidth
    return (x & -x).bit_length() - 1


def ctlz(x: int, bitwidth=32) -> int:
    """
    Count the number of leading zeros in the binary representation of the given input, given a bitwidth (default: 32).

    Inspired by Julia's `leading_zeros` function:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/int.jl#L428>
    """
    if x == 0:
        return bitwidth
    return bitwidth - x.bit_length()


def clo(x: int, bitwidth=32) -> int:
    """
    Count the number of leading ones in the binary representation of the given input, given a bitwidth (default: 32).

    Inspired by Julia's `leading_ones` function:
      <https://github.com/JuliaLang/julia/blob/7fa26f01/base/int.jl#L470>
    """
    return ctlz(~x & bitmask(bitwidth), bitwidth=bitwidth)
