import random
from math import gcd
from Crypto.Util.number import *

def factorn_given_d(n,e,d):
    """
    Given n and both the public and private exponents, it factors n
    Args:
        n : rsa modulus
        e : public exponent
        d : private exponent

    Returns:
        p, q : prime factors of n
    """
    k = d*e - 1

    while True:
        g = random.randint(2,n-1)
        t = k

        while t%2 == 0:
            t//=2
            x = pow(g,t,n)

            if x > 1:
                y = gcd(x-1,n)
                if y > 1:
                    assert n%y == 0
                    return y, n//y
