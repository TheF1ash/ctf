#!/usr/bin/env/python
import binascii

#getting lines which are key-value pairs from input file and returning values
def getVal(line):
	val = line.split('=')[1]
	return int(val)
cipherFile = open('intro_rsa.txt','r')
values = map(getVal,cipherFile.readlines())
p = values[0]
q = values[1]
e = values[2]
c = values[3]

#phi(n) = (p-1) * (q-1)
phi = (p - 1) * (q - 1)

# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def mulinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = xgcd(a, b)
    if g == 1:
        return x % b

#decryption key, d = multiplicative inverse of e mod (phi(n))
d = mulinv(e,phi)

#decryption
p = pow(c,d,p * q)

#convert long to hex
hex_p = hex(p)

#decode hex value, ignoring 0x and last L
ascii_p = str(hex_p[2:-1]).decode('hex')

print ascii_p