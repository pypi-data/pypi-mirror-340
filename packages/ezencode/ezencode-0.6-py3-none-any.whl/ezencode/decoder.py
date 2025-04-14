"""EZ Encode decoder module."""


from typing import Generator, Union
from . import maps


__all__ = ['Decoder']
def __dir__() -> list[str]:
    return sorted(__all__)


class Decoder(object):
    """Translate encoded data to its corresponding ASCII and Extended ASCII representations."""
    __slots__ = frozenset({})

    def __new__(cls: type['Decoder'], data: Union[str, bytes], /) -> 'Decoder':
        """Returns a new Decoder object."""
        match data:
            case str(): cls.__data = data
            case bytes(): cls.__data = data.decode()
            case _: raise TypeError("data must be of type 'str' or 'bytes'")

        if len(data) == 0: raise SystemExit(1)
        cls.__layer1_ascii, cls.__layer2_layer1 = maps.Maps.generate_decoder_maps()
        return super(Decoder, cls).__new__(cls)

    @classmethod
    def symbol_stream(cls: type['Decoder'], /) -> Generator[str]:
        """A generator that yields a pair of layer 1 encoding symbols."""
        start, size, length = 0, 2, len(cls.__data)
        while start < length:
            symbols = cls.__data[start: size]
            yield cls.__layer2_layer1[symbols]
            start += 2
            size += 2

    @classmethod
    def ascii_stream(cls: type['Decoder'], /) -> Generator[int]:
        """A generator that yields an ASCII code from 0 to 256."""
        for symbols in cls.symbol_stream():
            try:
                yield cls.__layer1_ascii[symbols]
            except KeyError:
                raise Exception(f"Cannot encode character; '{symbols!r}'")

    @classmethod
    def decode(cls: type['Decoder'], /) -> str:
        """Decodes and returns the decoded string."""
        decoded = ''.join([ chr(number) for number in cls.ascii_stream() ])
        return decoded
