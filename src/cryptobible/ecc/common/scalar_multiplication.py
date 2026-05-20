# DO NOT import this file into __init__.py as sage already has Elliptic Curves built-in

from .point_addition import point_addition

def scalar_multiplication(P, n, a=497, p=9739):
    O = (None, None)
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q, a, p)
        Q = point_addition(Q, Q, a, p)  
        n = n // 2
    return R
