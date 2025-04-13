"""SEA (Simple Encoding Algorithm) encoder module."""

from typing import Generator
from . import conversion_map


class Encode(object):
    """Translate text using the SEA (Simple Encoding Algorithm) to its corresponding code point."""
    __slots__ = frozenset({})

    def __new__(cls: type['Encode'], text: str, /) -> 'Encode':
        assert isinstance(text, str), f"'{text}' must be of type 'str'"
        if len(text) == 0: raise SystemExit(1)
        cls.__text = text
        return super(Encode, cls).__new__(cls)

    @classmethod
    def character_stream(cls: type['Encode'], /) -> Generator[str]:
        for character in cls.__text:
            yield character

    @classmethod
    def binary_stream(cls: type['Encode'], /) -> Generator[str]:
        for character in cls.character_stream():
            try:
                yield conversion_map.ascii_binary_map[character]
            except KeyError:
                raise Exception(f"Cannot encode character; '{character}'")

    @classmethod
    def symbol_stream(cls: type['Encode'], /) -> Generator[str]:
        for binary_string in cls.binary_stream():
            try:
                yield conversion_map.sea_encode_map[binary_string]
            except KeyError:
                raise Exception(f"Cannot encode character; '{binary_string}'")

    @classmethod
    def encoded_text(cls: type['Encode'], /) -> str:
        encoded = ':'.join([ symbol for symbol in cls.symbol_stream() ])
        return encoded
