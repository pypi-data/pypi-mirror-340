"""EZ Encoder encoder module."""


from typing import Generator, Union
from . import maps


__all__ = ['Encoder']
def __dir__() -> list[str]:
    return sorted(__all__)


class Encoder(object):
    """Translate data to its corresponding EZ Encoder code point."""
    __slots__ = frozenset({})

    def __new__(cls: type['Encoder'], data: Union[str, bytes], /) -> 'Encoder':
        """Returns a new Encoder object."""
        match data:
            case str(): cls.__data = data.encode()
            case bytes(): cls.__data = data
            case _: raise TypeError("data must be of type 'str' or 'bytes'")

        if len(data) == 0: raise SystemExit(1)
        cls.__self__ = cls
        cls.__ascii_layer1,  cls.__layer1_layer2 = maps.Maps.generate_encoder_maps()
        return super(Encoder, cls).__new__(cls)

    @classmethod
    def symbol_stream(cls: type['Encoder'], /) -> Generator[str]:
        """A generator that yields a pair of layer 2 encoding symbols."""
        for ascii_character in cls.__data:
            try:
                layer_1 = cls.__ascii_layer1[ascii_character]
                layer_2 = cls.__layer1_layer2[layer_1]
                yield layer_2
            except KeyError:
                raise Exception(f"Cannot encode character; '{ascii_character!r}'")

    @classmethod
    def encode(cls: type['Encoder'], /) -> str:
        """Encodes and returns the encoded string."""
        encoded = ''.join([ symbol for symbol in cls.symbol_stream() ])
        return encoded
