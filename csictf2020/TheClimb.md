
My writeup for 'The Climb' from Crypto:
```On analyzing the code using the sample plaintext and given key we see that the encryption takes place in the following steps:
1. Get the square root of the length of the key (9 here), say key_matrix_size = 3 and construct a square matrix of that size 
2. In the square matrix, going row-wise, add the numerical equivalent ('a'=0, 'b'=1 and so on) of the key character starting from the 1st character.
    So for the key 'gybnqkurp', the key matrix will be
            [[6, 24, 1],
    K_M =    [13, 16, 10],
             [20, 17, 15]]
3. Now we do the actual encryption, as part of which we divide the plaintext into blocks of key_matrix_size, and for each of them again, get the numerical equivalent and store them in a column matrix, and we do a matrix multiplication with the key matrix. Then take modulo 26 for the result and get its ASCII value, and print it as ciphertext.
    So for the plaintext of 'fakeflag', the encryption is done for 'fak' first as follows:
    P_M = [5, -> 'f'
           0, -> 'a'
          10] -> 'k'
    Then the result column matrix, R_M = K_M x P_M followed by taking a modulo 26 and then converting to numerical equivalent
    For example for 'fak'
            [[6, 24, 1],    [5,            [6 * 5 + 24 * 0 + 1*10,            [40,                        [14,
     R_M =  [13, 16, 10], x  0,        =    13 * 5 + 16 * 0 + 10 * 10,  =      165, . Taking mod 26 gives  9, which is equivalent to 'ojq'
            [20, 17, 15]]    10]            20 * 5 + 17 * 0 + 15 * 10]         250]                        16]
             when converting to numerical equivalents from top.
             Similarly we can do this for other plaintext blocks.
    So in general for a plaintext block p1p2p3, for key k1k2k3k4k5k6k7k8k9,taking their numerical equivalents,
    ciphertext c1 = (p1 * k1 + p2 * k2 + p3 * k3) % 26
               c2 = (p1 * k4 + p2 * k5 + p3 * k6) % 26
               c3 = (p1 * k7 + p2 * k8 + p3 * k9) % 26
    4. Based on this I tried to see whether we can decrypt the ciphertext one block at at time, but I didnt know that the key in the code was the actual key to be used, I thought we had to find the key, but the challenge admin clarified that the actual key was the same one that was in the code. After that it was simple, we had to solve the system of congruences in 3 variables for each ciphertext block of size 3. I found that this can be done in dcode.fr.
So our first set of congruences to solve becomes
    (p1 * 6 + p2 * 24 + p3) = 11 mod 26 ('l')
    (p1 * 13 + p2 * 16 + p3 * 10) = 17 mod 26 ('r')
    (p1 * 20 + p2 * 17 + p3 * 15) = 25 mod 26 ('z')
Solving this using dcode.fr we get p1 = 'h', p2 = 'i', p3 = 'l'
And continuing like this we get the plaintext which is hillshaveeyes
So the flag is csictf{hillshaveeyes}
```
