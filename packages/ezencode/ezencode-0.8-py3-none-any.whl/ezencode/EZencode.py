"""A module that contains a decorator for easy encoding function arguments."""


from os import getcwd
import time
from typing import Union
from . import decoder
from . import encoder


__all__ = ['ezencode']
def __dir__() -> list[str]:
    return sorted(__all__)


class ezencode(object):
    """Encode or decode data to or from the EZ Encode format."""
    __slots__ = frozenset({})

    def __new__(cls: type['ezencode'], data: Union[str, bytes] = '', /) -> 'ezencode':
        """Return a new 'ezencode' object."""
        if not data:
            raise Exception("no data provided")
        else:
            cls.__data = data
        return super(ezencode, cls).__new__(cls)

    @classmethod
    def decode(cls: type['ezencode'], /) -> str:
        """Decode data from the EZ Encode format to its original form."""
        return decoder.Decoder(cls.__data).decode()

    @classmethod
    def encode(cls: type['ezencode'], /, *, as_bytes: bool = False, write_out: bool = False) -> Union[str, bytes]:
        """Encode data to the EZ Encode format."""
        match (as_bytes, write_out):
            case (True, True):
                seconds = time.localtime().tm_sec + time.localtime().tm_min
                filepath = getcwd() + f"/ezencode-{seconds}.bin"
                with open(filepath, 'wb') as ezencode_bin_file:
                    encoded = encoder.Encoder(cls.__data).encode()
                    ezencode_bin_file.write(encoded.encode())
                return encoded
            case (True, False):
                encoded = encoder.Encoder(cls.__data).encode()
                return encoded.encode()
            case (False, True):
                seconds = time.localtime().tm_sec + time.localtime().tm_min
                filepath = getcwd() + f"/ezencode-{seconds}.bin"
                with open(filepath, "w") as ezencode_bin_file:
                    encoded = encoder.Encoder(cls.__data).encode() 
                    ezencode_bin_file.write(encoded)
                return encoded
            case _:
                return encoder.Encoder(cls.__data).encode()
