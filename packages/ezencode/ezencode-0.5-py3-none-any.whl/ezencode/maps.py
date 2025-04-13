"""EZ Encode mapping module."""

from typing import Generator


class Maps(object):
    """Map text to symbols and vice versa."""
    __slots__ = frozenset({})

    def __new__(cls: type['Maps'], /) -> 'Maps':
        return super(Maps, cls).__new__(cls)

    @classmethod
    def ascii_stream(cls: type['Maps'], /) -> Generator[int]:
        for character in range(0, 256):
            yield character

    @classmethod
    def binary_stream(cls: type['Maps'], /) -> Generator[str]:
        for number in range(0, 256):
            yield bin(number)[2:].zfill(8)

    @classmethod
    def symbol_stream(cls: type['Maps'], /) -> Generator[str]:
        left_symbols =  "0123456789~!@#^?"
        right_symbols = "ZYXWVUTSRQPONMLK"
        for left in left_symbols:
            for right in right_symbols:
                yield left+right

    @classmethod
    def layer2_stream(cls: type['Maps'], /) -> Generator[str]:
        layer2_left = 'zyxwvutsrqponmlk'
        layer2_right = 'jihgfedcba-+|$%&'
        for left in layer2_left:
            for right in layer2_right:
                yield left+right

    @classmethod
    def generate_map(cls: type['Maps'], map_type: int, /) -> dict[str | int, str | int]:
        assert isinstance(map_type, int), f"'{map_type}' must be of type 'int'"
        match map_type:
            # ascii to binary
            case 0: return dict({key: value for key, value in zip(cls.ascii_stream(), cls.binary_stream(), strict=True)})
            # binary to ascii
            case 1: return dict({key: value for key, value in zip(cls.binary_stream(), cls.ascii_stream(), strict=True)})
            # symbol to binary
            case 2: return dict({key: value for key, value in zip(cls.symbol_stream(), cls.binary_stream(), strict=True)})
            # binary to symbol
            case 3: return dict({key: value for key, value in zip(cls.binary_stream(), cls.symbol_stream(), strict=True)})
            # layer1 to layer2
            case 4: return dict({key: value for key, value in zip(cls.symbol_stream(), cls.layer2_stream(), strict=True)})
            # layer2 to layer1
            case 5: return dict({key: value for key, value in zip(cls.layer2_stream(), cls.symbol_stream(), strict=True)})
            # invalid map type
            case _: raise Exception(f"'{map_type}' is not a valid map type")
