#!/usr/bin/env/python
import binascii

ciphertext = open('ciphertext.txt','r').read()
binary = bin(int(ciphertext, 16))[2:]
first_letter_code =  ord('a') 					# Assuming first letter is 'a' (flag is actf{...})
key = first_letter_code ^ int(binary[:8],2)		# key = 'a' xor 1st 8 bits of ciphertext (in question, hinted that key is 1 byte)
plaintext = ""
for i in xrange(0,len(binary),8):
 	cipherBin = int(binary[i:i+8],2)			# for each block of ciphertext, calculate plaintext by xoring ciphertext with key
 	plaintextBin = cipherBin ^ key
 	plaintext += chr(plaintextBin)				# convert ascii code to plaintext

print(plaintext)
