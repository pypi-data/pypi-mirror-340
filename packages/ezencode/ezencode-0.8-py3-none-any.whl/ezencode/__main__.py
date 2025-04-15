"""EZ Encode CLI entry point."""


from sys import argv, stdout, stderr
from .EZencode import ezencode

red = '\x1b[1;31m'
green = '\x1b[1;32m'
blue = '\x1b[1;34m'
cyan = '\x1b[1;36m'
b_white = '\x1b[1;37m'
i_white = '\x1b[3;37m'
reset = '\x1b[0m'

def output(*args) -> str:
    string = ''.join(args)
    return string


def ezhelp():
    usage = output(cyan, 'Usage', reset, b_white, ': ', reset, green, 'ezencode ', reset, b_white, '[-h] [-b] -d|-e ', reset)
    usage += output(i_white, '<DATA> ', reset, b_white, '[--write-out]', reset, '\n')
    desc = output(cyan, 'Description', reset, b_white, ': A CLI utility for encoding / decoding data to and from the EZ Encode encoding format', reset, '\n\n')
    flags_label = output(cyan, 'Flags', reset, '\n', b_white, '-----', reset, '\n')
    b_flag = output(blue, '  -b', reset, '             ', b_white, 'convert EZ Encoded data to bytes', reset, '\n\n')
    h_flag = output(blue, '  -h', reset, '             ', b_white, 'show ezencode help for flags and options', reset, '\n\n')
    w_flag = output(blue, '  -w', reset, '             ', b_white, 'write the encoded data to a file', reset, '\n\n')
    options_label = output(cyan, 'Options', reset, '\n', b_white, '-------', reset, '\n')
    d_option = output(blue, '  -d', reset, i_white, ' DATA', reset, '        ', b_white, 'decode previously EZ Encoded data', reset, '\n\n')
    e_option = output(blue, '  -e', reset, i_white, ' DATA', reset, '        ', b_white, 'encode data to EZ Encode format', reset, '\n')
    stdout.write(f'{usage}{desc}{flags_label}{b_flag}{h_flag}{w_flag}{options_label}{d_option}{e_option}')

def main(*args) -> None:
    if len(args) == 0:
        raise SystemExit(0)
    else:
        match args:
            case ('-h',):
                ezhelp()
                raise SystemExit(0)
            case ('-d', string):
                stdout.write(ezencode(string).decode())
                raise SystemExit(0)
            case ('-e', string):
                stdout.buffer.write(ezencode(string).encode())
                stdout.flush()
                raise SystemExit(0)
            case ('-e', string, '-w'):
                ezencode(string).encode(write_out=True)
                raise SystemExit(0)
            case ('-b', '-e', string):
                stdout.buffer.write(ezencode(string).encode(as_bytes=True))
                stdout.flush()
                raise SystemExit(0)
            case ('-e', string, '-b'):
                stdout.buffer.write(ezencode(string).encode(as_bytes=True))
                stdout.flush()
                raise SystemExit(0)
            case ('-b', '-e', string, '-w'):
                ezencode(string).encode(as_bytes=True, write_out=True)
                raise SystemExit(0)
            case ('-e', string, '-b', '-w'):
                ezencode(string).encode(as_bytes=True, write_out=True)
                raise SystemExit(0)
            case ('-w', '-b', '-e', string):
                ezencode(string).encode(as_bytes=True, write_out=True)
                raise SystemExit(0)
            case ('-w', '-e', string, '-b'):
                ezencode(string).encode(as_bytes=True, write_out=True)
                raise SystemExit(0)
            case ('-b', '-w', '-e', string):
                ezencode(string).encode(as_bytes=True, write_out=True)
                raise SystemExit(0)
            case _:
                stderr.write(output(red, 'Error', reset, b_white, ': ', 'invalid arguments or argument position'))
                raise SystemExit(1)

if __name__ == '__main__':
    main(*argv[1:])
