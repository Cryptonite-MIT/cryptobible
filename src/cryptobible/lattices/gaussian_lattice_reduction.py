from sage.all import *

def gausian_lattice_reduction(basis : int[][]):
    """
    reduces a bad basis to retrieve good basis, algo off of cryptohack
    Args:
        basis : 2 x 2 Matrix containing rowwise basis vectors

    Returns:
        basis : 2 x 2 Matrix with reduced basis vectors
    """
    v1 = basis[0]
    v2 = basis[1]
    if basis[1] > basis[0]:
        v1 = basis[1]
        v2 = basis[0]
    while True:
        if v1.norm() < v2.norm():
            v1, v2 = v2, v1 # obviously should swap if this is the case
        p = round(v1.dot_product(v2)/v2.dot_product(v2)) # projecting the taller vector onto the shorter & round to the spanned lattice
        if p == 0:
            break
        v1 -= p*v2 # reduce the taller vector
    
    return [v2, v1]

def test():
    while True:
        A = random_matrix(ZZ, 2, 2)
        if A.determinant() != 0:
            break
    # print(A)
    G = gausian_lattice_reduction(A)
    L = A.LLL()
    assert matrix(G) == L

if __name__ == "__main__":
    test()
