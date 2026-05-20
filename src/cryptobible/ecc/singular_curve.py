from sage.all import *
from Crypto.Util.number import *
from common.scalar_multiplication import scalar_multiplication

def singular_curve_attack(Gx,Gy,Px,Py,a,b,p):
    """
    A singular curve has a discriment equal to 0 and it has either one or two roots. 
    The points on a singular curve can be mapped to points on a finite field to reduce the ecdlp to a standard finite field dlp.

    For single root singular curves the mapping is P(x,y) -> (x-root)/y
    and for double root singular curves the mapping is P(x,y) -> (y+ t*(x-double_root))/(y- t*(x-double_root)) where t is sqrt(double_root-single_root)

    Args:
        Gx: x coordinate of Generator point
        Gy: y coordinate of Generator point
        Px: x coordinate of Public key
        Py: y coordinate of Public key
        a,b: curve parameters
        p: curve prime modulus
    
    Returns:
        d: private secret such that P = dG
    """

    assert (4*a**3 + 27*b**2)%p == 0

    F = GF(p)
    Gx,Gy,Px,Py = F(Gx),F(Gy),F(Px),F(Py)
    x = F['x'].gen()
    roots = (x**3 + a*x + b).roots()

    # single root singular curve
    if len(roots) == 1:
        g, p_ = (Gx - roots[0][0])/Gy, (Px-roots[0][0])/Py
        return int(p_/g)

    if roots[0][1] == 2:
        double = roots[0][0]
        t = (double - roots[1][0])
    else:
        double = roots[1][0]
        t = (double - roots[0][0])
    
    tsq = t.sqrt()
    Gx_,Px_ = Gx-double,Px-double
    g = (Gy+tsq*Gx_)/(Gy-tsq*Gx_)
    p_ = (Py+tsq*Px_)/(Py-tsq*Px_)
    return int(p_.log(g))
        
def test():
    p, a, b = getPrime(64), 0, 0
    F = GF(p)
    
    while True:
        Gx = F.random_element()
        y = Gx**3 + a*Gx + b
        if Gx != 0 and y.is_square():
            Gy = y.sqrt()
            break
            
    d = randint(2, p - 1)
    Px, Py = scalar_multiplication((Gx, Gy), d, a, p)
    assert d == singular_curve_attack(Gx, Gy, Px, Py, a, b, p)
    
    a, b = -3, 2
    while True:
        Gx = F.random_element()
        y = Gx**3 + a*Gx + b
        if Gx != 1 and y.is_square():
            Gy = y.sqrt()
            break
            
    d = randint(2, p)
    Px,Py = scalar_multiplication((Gx,Gy),d,a,p)
    assert d == singular_curve_attack(Gx, Gy, Px, Py, a, b, p)

if __name__ == "__main__":
    test()