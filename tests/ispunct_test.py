import string
from collections.abc import Iterable

import pytest

import ispunct


def test_ispunct_basic():
    assert ispunct.ispunct("?")
    assert not ispunct.ispunct("a")
    assert ispunct.ispunct("‽")


def test_ispunct_extended_non_punct_chars(non_punct_chars: Iterable[str]):
    for c in non_punct_chars:
        assert not ispunct.ispunct(c)


def test_ispunct_extended_punct_chars(punct_chars: Iterable[str]):
    for c in punct_chars:
        assert ispunct.ispunct(c)


def test_ispunct_non_standard_punct_chars(
    non_standard_punct_chars: Iterable[str],
):
    for c in non_standard_punct_chars:
        assert c not in string.punctuation
        assert ispunct.ispunct(c)


def test_ispunct_str_iterable_all():
    assert all(not ispunct.ispunct(c) for c in "  \t   \n   \r  ")
    assert all(not ispunct.ispunct(c) for c in "ΣβΣβ")
    assert all(ispunct.ispunct(c) for c in "‡؟჻")


def test_is_punct_comprehensive(data):
    for c in data.is_punct:
        assert ispunct.ispunct(c)


def test_is_not_punct_comprehensive(data):
    for c in data.not_punct:
        # Explicilty skip characters defined in string.punctuation that are
        # not technically punctuation characters
        if c in "$+<=>^`|~":
            continue

        assert not ispunct.ispunct(c)


def test_bitmask():
    assert ispunct.bits.bitmask(0) == 0
    assert ispunct.bits.bitmask(1) == 1
    assert ispunct.bits.bitmask(3) == 0b111
    assert ispunct.bits.bitmask(8) == 0xFF
    assert ispunct.bits.bitmask(32) == 0xFFFFFFFF


def test_cttz():
    assert ispunct.bits.cttz(0, 32) == 32
    assert ispunct.bits.cttz(1, 32) == 0
    assert ispunct.bits.cttz(2, 32) == 1
    assert ispunct.bits.cttz(0b1000, 32) == 3
    assert ispunct.bits.cttz(0b101000, 32) == 3
    assert ispunct.bits.cttz(0x80000000, 32) == 31


def test_ctlz():
    assert ispunct.bits.ctlz(0, 32) == 32
    assert ispunct.bits.ctlz(1, 32) == 31
    assert ispunct.bits.ctlz(2, 32) == 30
    assert ispunct.bits.ctlz(0b1000, 32) == 28
    assert ispunct.bits.ctlz(0xFFFFFFFF, 32) == 0
    assert ispunct.bits.ctlz(0x80000000, 32) == 0


def test_clo():
    assert ispunct.bits.clo(0, 32) == 0
    assert ispunct.bits.clo(0xFFFFFFFF, 32) == 32
    assert ispunct.bits.clo(0xF0000000, 32) == 4
    assert ispunct.bits.clo(0b11110000, 8) == 4
    assert ispunct.bits.clo(0b01111111, 8) == 0
    assert ispunct.bits.clo(0b11000000, 8) == 2


def test_reinterpret():
    assert ispunct.reinterpret.reinterpret_as_uint(chr(18)) == 301989888
    assert ispunct.reinterpret.reinterpret_as_uint(chr(185)) == 3266904064


def test_is_malformed():
    assert not ispunct.unicode.ismalformed(chr(18))
    assert not ispunct.unicode.ismalformed(chr(185))
    assert not ispunct.unicode.ismalformed(chr(6969))


def test_category_code():
    assert ispunct.unicode.category_code(chr(18)) == 26
    assert ispunct.unicode.category_code(chr(185)) == 11
    assert ispunct.unicode.category_code(chr(6969)) == 6
    assert ispunct.unicode.category_code(chr(69703)) == 18


def test_errors_on_str():
    with pytest.raises(TypeError):
        # A multi-character string cannot be interpreted as a character literal
        ispunct.ispunct("This is a str, not a character")

    with pytest.raises(TypeError):
        # Empty string is not allowed
        ispunct.ispunct("")


def test_errors_on_other_types():
    with pytest.raises(TypeError):
        ispunct.ispunct(420)

    with pytest.raises(TypeError):
        ispunct.ispunct(object())

    with pytest.raises(TypeError):
        ispunct.ispunct([])
