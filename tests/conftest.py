import dataclasses
import json
import pathlib
from collections.abc import Iterable
from types import SimpleNamespace

import pytest

# Pytest suggests defining all fixtures within a single conftest.py file:
#   gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68


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


def _parse_hex(x: str) -> str:
    # All input should be hex values
    if isinstance(x, str):
        # Type remark: this is unsafe in a sense as we assume that the string
        # given is parseable into a hex integer!  E.g., looks like 0x...  This
        # should be true for all test data.
        return int(x, 16)

    # Fallback: I don't know what to do with this!
    raise TypeError(f"Cannot parse hex from {type(x).__name__!r}")


@dataclasses.dataclass(frozen=True)
class CharInfo:
    character: str
    integer: int
    trailing_zeros: int
    leading_zeros: int
    leading_ones: int
    uint32: int
    is_malformed: bool
    category_code: int


def _char_info_from_json(c: str, i: int, d: dict) -> CharInfo:
    return CharInfo(
        character=c,
        integer=i,
        trailing_zeros=d["tz"],
        leading_zeros=d["lz"],
        leading_ones=d["lo"],
        uint32=d["ri"],
        is_malformed=bool(d["im"]),
        category_code=d["cc"],
    )


def _load_data(f: str) -> list[int | tuple[int, int]]:
    data = json.loads(f.read_text())

    # Simple list like ["0x100", "0x101", ...]
    if isinstance(data, list):
        return [chr(_parse_hex(i)) for i in data]

    # Dictionary structured with char information
    if isinstance(data, dict):
        parsed_data = {}

        for key, value in data.items():
            i = _parse_hex(key)
            c = chr(i)
            parsed_data[c] = _char_info_from_json(c, i, value)

        return parsed_data


@pytest.fixture(scope="session")
def data():
    # Specify the data directory
    data_dir = pathlib.Path(__file__).parent / "data"

    # Iterate over data directory and construct a namespace for all data
    data = {}
    for f in data_dir.iterdir():
        # We only want to deal with JSON data files
        if not (f.is_file() and f.suffix == ".json"):
            continue

        data[f.stem] = _load_data(f)

    return SimpleNamespace(**data)
