"""SEA (Simple Encoding Algorithm) decoder module."""

from typing import Generator
from . import conversion_map


class Decode(object):
    """Translate SEA (Simple Encoding Algorithm) text to its corresponding binary and ascii representations."""
    __slots__ = frozenset({})

    def __new__(cls: type['Decode'], text: str, /) -> 'Decode':
        assert isinstance(text, str), f"'{text}' must be of type 'str'"
        if len(text) == 0: raise SystemExit(1)
        cls.__text = text
        cls.__sea_text = cls.__text.split(':')
        return super(Decode, cls).__new__(cls)

    @classmethod
    def validate(cls: type['Decode'], /) -> None:
        sea_characters = '~!@#$%^&*()-_=+?abcdefghijklmnop'
        for character in cls.__text:
            if character != ':' and character not in sea_characters:
                raise Exception(f"'{character}' are not SEA encoded")
            else:
                continue
        else:
            return None

    @classmethod
    def character_stream(cls: type['Decode'], /) -> Generator[str]:
        for characters in cls.__sea_text:
            yield characters

    @classmethod
    def binary_stream(cls: type['Decode'], /) -> Generator[str]:
        for characters in cls.character_stream():
            try:
                yield conversion_map.sea_decode_map[characters]
            except KeyError:
                raise Exception(f"'{characters}' are not SEA encoded")

    @classmethod
    def symbol_stream(cls: type['Decode'], /) -> Generator[str]:
        for binary_string in cls.binary_stream():
            try:
                yield conversion_map.binary_ascii_map[binary_string]
            except KeyError:
                raise Exception(f"Cannot encode character; '{binary_string[0]}'")

    @classmethod
    def decoded_text(cls: type['Decode'], /) -> str:
        cls.validate()
        decoded = ''.join([ symbol for symbol in cls.symbol_stream() ])
        return decoded
