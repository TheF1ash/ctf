#!/bin/sh

python -c 'print "nan"' | nc misc.2018.chall.actf.co 18004 | grep actf | cut -d ':' -f 2 | tr -d ' '
