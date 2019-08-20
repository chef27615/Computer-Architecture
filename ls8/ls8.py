#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

print(f'{sys.argv[0]}: {sys.argv[1] not found}')
# sys.exit()

if len(sys.argv) != 2:
    print('Usage: using file <filename>', file=sys.stderr)
    sys.exit(1)
cpu.load()




cpu.run()