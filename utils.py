"""
Justin Baum
20 October 2020
utils.py
Utilities
"""

# pylint: disable=invalid-name
def general_linear_congruence(a : int, modulus : int, k : int) -> int:
    """
    Linear Congruence Solver
    Extended Euclidean Algorithm
    a*x === (cong) k mod m
    """
    original_modulus = modulus
    y = 0
    x = k
    if modulus <= 1:
        return 0
    while a > 1:
        # I have never run into this being run
        # But because pypy compiles this, it gets upset
        if modulus == 0: return
        quotient = a // modulus
        (a, modulus) = (modulus, a % modulus)
        (x,y) = (y, x - quotient * y)
    return x % original_modulus

def multiplicative_inverse(a : int, modulus : int) -> int:
    """
    Multiplicative inverse
    a*x === (congruent) 1 mod modulus
    """
    return general_linear_congruence(a, modulus, 1)

def eulers_criterion(a: int, p : int):
    """
    https://en.wikipedia.org/wiki/Euler%27s_criterion
    Does a solution exist for x^2 = a mod p?
    Only when p is prime
    """
    if a == 0:
        return True
    return pow(a, (p-1)//2, p) == 1

def factors(n):
    """
    Generate factors
    """
    for i in range(2, n//2 + 1):
        if n % i == 0:
            yield i
