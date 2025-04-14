"""EZ Encode mapping module."""


from typing import Generator


__all__ = ['Maps']
def __dir__() -> list[str]:
    return sorted(__all__)


class Maps(object):
    """Map text to symbols and vice versa."""
    __slots__ = frozenset({})

    def __new__(cls: type['Maps'], /) -> 'Maps':
        """Return a new Maps object."""
        return super(Maps, cls).__new__(cls)

    @classmethod
    def ascii_stream(cls: type['Maps'], /) -> Generator[int]:
        """A generator that yields an ASCII code from 0 to 256."""
        for character in range(0, 256):
            yield character


    @classmethod
    def layer1_stream(cls: type['Maps'], /) -> Generator[str]:
        """A generator that yields a pair of symbols for the layer 1 encoding."""
        left_symbols =  "0123456789~!@#^?"
        right_symbols = "ZYXWVUTSRQPONMLK"
        for left in left_symbols:
            for right in right_symbols:
                yield left+right

    @classmethod
    def layer2_stream(cls: type['Maps'], /) -> Generator[str]:
        """A generator that yields a pair of symbols for the layer 2 encoding."""
        layer2_left = 'zyxwvutsrqponmlk'
        layer2_right = 'jihgfedcba-+|$%&'
        for left in layer2_left:
            for right in layer2_right:
                yield left+right

    @classmethod
    def generate_encoder_maps(cls: type['Maps'], /) -> tuple[dict, ...]:
        """Generates the mappings for the encode / decode translations."""
        __ascii_layer1 = dict({key: value for key, value in zip(cls.ascii_stream(), cls.layer1_stream(), strict=True)})
        __layer1_layer2 = dict({key: value for key, value in zip(cls.layer1_stream(), cls.layer2_stream(), strict=True)})
        return (__ascii_layer1, __layer1_layer2)

    @classmethod
    def generate_decoder_maps(cls: type['Maps'], /) -> tuple[dict, ...]:
        __layer1_ascii = dict({key: value for key, value in zip(cls.layer1_stream(), cls.ascii_stream(), strict=True)})
        __layer2_layer1 = dict({key: value for key, value in zip(cls.layer2_stream(), cls.layer1_stream(), strict=True)})
        return (__layer1_ascii, __layer2_layer1)

