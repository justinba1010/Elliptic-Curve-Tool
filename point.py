"""
Justin Baum
21 October 2020
point.py
Points on an elliptic curve
Jacobian Coordinates
"""

from utils import multiplicative_inverse as m_inv

AFFINE_EQ = False
class Point:
    """
    Point Module
    Represents points in affine form on some curve
    """
    def __init__(self, x, y, z, curve):
        """
        Construct a point on some curve
        """
        # pylint: disable=invalid-name
        self.x = x
        self.y = y
        self.z = z
        self.curve = curve
        self.infinity = False

    @staticmethod
    def infinity(): # pylint: disable=method-hidden
        """
        Return point at infinity
        """
        point = Point(0,0,1,None)
        point.infinity = True
        return point
    def copy(self):
        """
        Return a deep copy
        """
        return Point(self.x, self.y, self.z, self.curve)
    def convert_to_affine(self):
        """
        Converts point to affine coordinates
        """
        if self.infinity:
            return
        modulus = self.curve.modulus
        self.x *= m_inv(pow(self.z, 2, modulus), modulus)
        self.x %= modulus
        self.y *= m_inv(pow(self.z, 3, modulus), modulus)
        self.y %= modulus
        self.z = 1
        return
    def double(self):
        """
        Returns a new point that is:
        p + p
        """
        if self.infinity:
            return Point.infinity()
        modulus = self.curve.modulus
        # pylint: disable=invalid-name
        A = pow(self.y, 2, modulus)
        B = (4 * self.x) * A
        B %= modulus
        C = 8 * pow(A, 2, modulus)
        C %= modulus
        D = (
            3 * pow(self.x, 2, modulus)
            +
            self.curve.a * pow(self.z, 4, modulus)
        )
        D %= modulus
        x_3 = pow(D, 2, modulus) - (2 * B)
        x_3 %= modulus
        y_3 = D * (B - x_3) - C
        y_3 %= modulus
        z_3 = 2 * self.y * self.z
        if z_3 == 0:
            return Point.infinity()
        z_3 %= modulus
        return Point(x_3, y_3, z_3, self.curve)
    def multiply(self, k):
        """
        Returns new point using
        p1 * k
        p199 textbook
        """
        # pylint: disable=invalid-name
        P = Point.infinity()
        p = self.copy()
        while k > 0:
            if k & 1:
                P = P + p
            k >>= 1
            p = p.double()
        return P
    def add(self, other):
        """
        Last try
        https://www.cs.uaf.edu/2015/spring/cs463/lecture/02_27_ECC_jacobi.html
        Also more general as in z2 doesn't have to be 1
        """
        # pylint: disable=invalid-name,too-many-locals,pointless-string-statement

        """
        Point at infinity is the identity element of elliptic curve arithmetic.
        Adding it to any point results in that other point,
        including adding point at infinity to itself. That is:
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        ---------------------------------------------------------
        O + O = O
        O + P = P
        P + O = P
        """

        if self.infinity and other.infinity:
            return Point.infinity()
        if self.infinity:
            return other.copy()
        if other.infinity:
            return self.copy()

        p = self.curve.modulus
        zz1 = (self.z * self.z) % p
        zzz1 = (zz1 * self.z) % p
        zz2 = (other.z * other.z) % p
        zzz2 = (zz2 * other.z) % p
        a = (self.x * zz2) % p
        b = (other.x * zz1 - a) % p
        c = (self.y * zzz2) % p
        d = (other.y * zzz1 - c) % p
        if b == 0:
            if d == 0:
                return self.double()
            return Point.infinity()
        e = (b * b) % p
        f = (b * e) % p
        g = (a * e) % p
        h = (self.z * other.z) % p
        f2g = 2 * g + f
        x_3 = (d * d - f2g) % p
        z_3 = (b * h) % p
        gx = g - x_3
        y_3 = (d * gx - c * f) % p
        return Point(x_3, y_3, z_3, self.curve)
    def add_text(self, other):
        """
        Returns a new point that is:
        p1 + p2
        """
        # pylint: disable=too-many-locals
        if self == other:
            return self.double()
        if self.x == other.x:
            return Point.infinity()
        # pylint: disable=invalid-name
        x_1 = self.x
        y_1 = self.y
        z_1 = self.z
        x_2 = other.x
        y_2 = other.y
        # z_2 = other.z
        m = self.curve.modulus
        # z_1^2
        A = pow(z_1, 2, m)
        # z_1A
        B = z_1 * A
        B %= m
        # x_2 A
        C = x_2 * A
        C %= m
        # y_2 B
        D = y_2 * B
        D %= m
        # C - x_1
        E = C - x_1
        E %= m
        # D - y_1
        F = D - y_1
        F %= m
        # E^2
        G = pow(E, 2, m)
        # GE
        H = G * E
        H %= m
        # x_1G
        I = x_1 * G
        I %= m
        # F^2 - B - 2I
        x_3 = pow(F, 2, m) - B - (2*I)
        x_3 %= m
        # F(I - x_3) - y_1H
        y_3 = F * (I - x_3) - (y_1 * H)
        y_3 %= m
        # z_1E
        z_3 = z_1 * E
        z_3 %= m
        return Point(x_3, y_3, z_3, self.curve)
    def add_alternative(self, other):
        # pylint: disable=invalid-name
        # pylint: disable=too-many-locals
        """
        https://en.wikibooks.org/wiki/Cryptography/Prime_Curve/Jacobian_Coordinates#J_+_J_-%3E_J_(_12M,_2S)_(secp256k1_has_12M,_4S)
        """
        x_1 = self.x
        y_1 = self.y
        z_1 = self.z
        x_2 = other.x
        y_2 = other.y
        z_2 = other.z
        m = self.curve.modulus
        u1 = y_2 * z_1
        u1 %= m
        u2 = y_1 * z_2
        u2 %= m
        v1 = x_2 * z_1
        v1 %= m
        v2 = x_1 * z_2
        v2 %= m
        if v1 == v2:
            if u1 != u2:
                return Point.infinity()
            return self.double()
        u = u1 - u2
        u %= m
        v = v1 - v2
        v %= m
        v_to_3 = pow(v, 3, m)
        v_to_2 = pow(v, 2, m)
        w = z_1 * z_2
        a = (
            pow(u, 2, m) * w
            -
            v_to_3
            -
            2 * v_to_2 * v2
        )
        a %= m
        x_3 = v * a
        x_3 %= m
        y_3 = (
            u
            *
            (v_to_2 * v2 - a)
            -
            v_to_3 * u2
        )
        y_3 %= m
        z_3 = v_to_3 * w
        z_3 %= m
        return Point(x_3, y_3, z_3, self.curve)
    def order_multiplication_generator(self):
        "Generates the order as a generator"
        point = self.copy()
        yield Point.infinity()
        while True:
            yield point.copy() if not point.infinity else Point.infinity()
            if point.infinity:
                break
            point += self
    def __add__(self, other):
        """
        Allows the use of +
        """
        return self.add(other)
    def __iadd__(self, other):
        """
        Allows the use of +=
        """
        return self + other
    def __mul__(self, k):
        """
        Allows the use of *
        """
        return self.multiply(k)
    def __imul__(self, k):
        """
        Allows the use of *=
        """
        return self * k
    def __eq__(self, other):
        """
        Allows the use of ==
        """
        selfcopy = self.copy()
        othercopy = other.copy()
        if AFFINE_EQ:
            selfcopy.convert_to_affine()
            othercopy.convert_to_affine()
        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z and
            self.curve == other.curve
            or
            (self.infinity and other.infinity)
            or
            AFFINE_EQ and
            selfcopy.x == othercopy.x and
            selfcopy.y == othercopy.y and
            selfcopy.curve == othercopy.curve
        )
    def __str__(self):
        """
        Returns a pretty print of the point
        """
        if self.infinity:
            return "<O>"
        return "<{}, {}, {}>".format(self.x, self.y, self.z)
    def __hash__(self):
        """
        Allows the use of sets
        """
        return hash(0) if self.infinity else hash((self.x, self.y, self.curve.__str__()))
