from sage.all import *
from Crypto.Util.number import *

def franklin_reiter(n,e,c1,c2,f):
    """
    two messages m1 and m2 such that m2 = a*m1 + b
    Solves for m1 and m2 given ciphertexts of both under the same modulus and exponent

    Args:
        n: modulus
        e: rsa exponent
        c1: m1^e mod n
        c2: m2^e mod n
        f: function of the form ax+b

    Returns:
        m1: message 1
        m2: message 2(linearly related to m1)
    """

    P = PolynomialRing(Zmod(n), 't')
    x = P.gen()
    p_gcd = (f(x)**e -c2).gcd(x**e-c1)
    m1 = -p_gcd.coefficients()[0]
    return m1,f(m1)

def test():
    p,q = getPrime(1024),getPrime(1024)
    n = p*q
    e = 65537
    m1,a,b = randint(0,n-1),randint(0,n-1),randint(0,n-1)
    
    def f(x):
        return a*x+b
    
    m2 = f(m1)
    c1,c2 = pow(m1,e,n),pow(m2,e,n)
    assert m1,m2 == franklin_reiter(n,e,c1,c2,f)

if __name__ == '__main__':
    test()