from sage.all import *
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint_finite_field
from sage.schemes.elliptic_curves.ell_generic import EllipticCurve_generic
from sage.rings.finite_rings.finite_field_prime_modn import FiniteField_prime_modn
from sage.rings.finite_rings.integer_mod import IntegerMod_abstract

def no_hash[E: EllipticCurvePoint_finite_field](G: E, Q: E, n: int | None = None) -> tuple[IntegerMod_abstract, IntegerMod_abstract, IntegerMod_abstract]:
    '''
    Creates a random valid message and (r, s) signature.
    '''
    E: EllipticCurve_generic = G.curve()
    F: FiniteField_prime_modn = E.base_field()
    n = n or G.order()
    R = Zmod(n)

    u = R.random_element()
    v = R.random_element()
    P = u*G + v*Q
    r = R(P.x())
    s = r / v
    m = (u * r) / v

    return (m, r, s)
