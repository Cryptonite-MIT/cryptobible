from sage.all import *
from math import prod

def arora_ge(A,b,p,e):
    """
    A * s + e = b (mod p)
    where A is a m x n matrix, s is a n degree secret vector and e is n degree error vector
    Here e is constrained to be fixed to a certain set of values. 
    The attack forms a polynomial of the form f(x) = prod(b_i - sum(A_ij*x_j - e_k)) where e_k is each possible error value.
    It then uses the groebner basis to reduce the polynomial and solve for the x values.
    Args:
        A : m x n matrix of n eqns with m unkowns
        b : n degree vector
        p : modulus
        e : list of possible error values

    Returns:
        s : n degree secret vector
    """
    P = PolynomialRing(GF(p),A.ncols(),'x')
    x = vector(P.gens())

    poly = [prod(b[i] - (A[i]*x) - y for y in e) for i in range(A.nrows())]

    gb = P.ideal(poly).groebner_basis()
    secret = vector(GF(p),([int(-s.constant_coefficient()) for s in gb]))
    return secret