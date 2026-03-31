#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge

b = Bridge()
rows = b._read_sheet('requests!A:I')
for row in rows:
    print(row)
