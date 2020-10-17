import re
import sys
import struct
import binascii
from functools import lru_cache
from elftools.elf.elffile import ELFFile


@lru_cache(maxsize=None)
def addr_to_sym(addr, elf):
    symtab = elf.get_section_by_name(".symtab")
    for sym in symtab.iter_symbols():
        if sym.entry.st_value <= addr < sym.entry.st_value + sym.entry.st_size:
            return sym.name
    # TODO possibly return "zephyr" if addr == 0, it seems like the "return adress" of z_thread_entry is 0.
    return "[unknown]"


def collapse(buf, elf):
    while buf:
        count, = struct.unpack_from(">Q", buf)
        assert count > 0
        addrs = struct.unpack_from(f">{count}Q", buf, 8)
        print(";".join(reversed(list(map(lambda a: addr_to_sym(a, elf), addrs)))), 1)
        buf = buf[8 + 8 * count:]


if __name__ == "__main__":
    elf = ELFFile(open(sys.argv[2], "rb"))
    with open(sys.argv[1], "r") as f:
        inp = f.read()

    lines = inp.splitlines()
    assert int(re.match(r"Perf buf length (\d+)", lines[0]).group(1)) == len(lines) - 1
    buf = binascii.unhexlify("".join(lines[1:]))
    collapse(buf, elf)
