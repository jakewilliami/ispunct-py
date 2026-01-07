import string
from collections.abc import Iterable

import pytest

import ispunct


@pytest.fixture
def non_punct_chars() -> Iterable[str]:
    def genchars() -> Iterable[str]:
        yield from ("א", "ﺵ")
        yield from ("a", "d", "j", "y", "z")
        yield from ("α", "β", "γ", "δ", "ф", "я")
        yield from ("A", "D", "J", "Y", "Z")
        yield from ("Δ", "Γ", "Π", "Ψ", "Ж", "Д")
        yield "ǅ"
        yield from ("0", "1", "5", "9")
        yield from ("∪", "∩", "⊂", "⊃", "√", "€", "¥", "↰", "△")
        yield from ("٣", "٥", "٨", "¹", "ⅳ")

    yield genchars()


def _non_standard_punct_chars() -> Iterable[str]:
    yield from ("‡", "؟", "჻", "§")


@pytest.fixture
def punct_chars() -> Iterable[str]:
    def genchars() -> Iterable[str]:
        yield from ("(", ")", "~", "$")
        yield from (".", ",", ";", ":", "&")
        yield from _non_standard_punct_chars()

    yield genchars()


@pytest.fixture
def non_standard_punct_chars() -> Iterable[str]:
    yield _non_standard_punct_chars()


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
