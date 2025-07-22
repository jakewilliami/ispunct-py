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


def test_ispunct_non_standard_punct_chars(non_standard_punct_chars: Iterable[str]):
    for c in non_standard_punct_chars:
        assert c not in string.punctuation
        assert ispunct.ispunct(c)


def test_ispunct_str_iterable_all():
    assert all(not ispunct.ispunct(c) for c in "  \t   \n   \r  ")
    assert all(not ispunct.ispunct(c) for c in "ΣβΣβ")
    assert all(ispunct.ispunct(c) for c in "‡؟჻")


def test_reinterpret():
    assert ispunct.reinterpret.reinterpret_as_uint(chr(18)) == 301989888
    assert ispunct.reinterpret.reinterpret_as_uint(chr(185)) == 3266904064


def test_is_malformed():
    assert not ispunct.unicode.ismalformed(chr(18))
    assert not ispunct.unicode.ismalformed(chr(185))
    assert not ispunct.unicode.ismalformed(chr(6969))
