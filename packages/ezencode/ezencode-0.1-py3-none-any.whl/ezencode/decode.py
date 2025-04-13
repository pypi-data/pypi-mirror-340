"""EZ Encode decoder module."""

from typing import Generator
import maps


class Decode(object):
    """Translate encoded text to its corresponding ASCII and Extended ASCII representations."""
    __slots__ = frozenset({})

    def __new__(cls: type['Decode'], text: str, /) -> 'Decode':
        assert isinstance(text, str), f"'{text}' must be of type 'str'"
        if len(text) == 0: raise SystemExit(1)
        cls.__text = text
        return super(Decode, cls).__new__(cls)

    @classmethod
    def character_stream(cls: type['Decode'], /) -> Generator[str]:
        start, size, length = 0, 2, len(cls.__text)
        while start < length:
            symbols = cls.__text[start: size]
            yield maps.Maps.generate_map(5)[symbols]
            start += 2
            size += 2

    @classmethod
    def binary_stream(cls: type['Decode'], /) -> Generator[str]:
        for characters in cls.character_stream():
            try:
                yield maps.Maps.generate_map(2)[characters]
            except KeyError:
                raise Exception(f"'{characters}' are not SEA encoded")

    @classmethod
    def symbol_stream(cls: type['Decode'], /) -> Generator[str]:
        for binary_string in cls.binary_stream():
            try:
                yield maps.Maps.generate_map(1)[binary_string]
            except KeyError:
                raise Exception(f"Cannot encode character; '{binary_string[0]}'")

    @classmethod
    def decoded_text(cls: type['Decode'], /) -> str:
        decoded = ''.join([ symbol for symbol in cls.symbol_stream() ])
        return decoded
