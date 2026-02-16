#!/usr/bin/env python3
import dis, marshal, struct, types

PYC_FILE = "serizawa_extracted/serizawa.pyc"

with open(PYC_FILE, "rb") as f:
    f.read(16)  # magic + flags + timestamp + size
    code = marshal.load(f)

def dump_code(co, indent=0):
    pfx = "  " * indent
    print(f"{pfx}=== Code: {co.co_name} ===")
    print(f"{pfx}  File: {co.co_filename}")
    print(f"{pfx}  Varnames: {co.co_varnames}")
    print(f"{pfx}  Names: {co.co_names}")
    print(f"{pfx}  Consts:")
    for i, c in enumerate(co.co_consts):
        if isinstance(c, types.CodeType):
            print(f"{pfx}    {i}: <code {c.co_name}>")
        else:
            print(f"{pfx}    {i}: {c!r}")
    print(f"{pfx}  --- Disassembly ---")
    dis.dis(co)
    print()
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            dump_code(c, indent + 1)

dump_code(code)
