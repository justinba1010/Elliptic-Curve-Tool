#! /usr/bin/python3
"""
Justin Baum
21 October 2020
driver.py
Driver code for using the Elliptic Curve
"""
import argparse
from sys import exit

from curve import Curve
from point import Point
from utils import factors

def main():
    """
    Driver code
    """
    # Parser Routine
    parser = argparse.ArgumentParser(description=
    """
    Elliptic Curves in Jacobian Coordinates
    """
    )
    # pylint: disable=line-too-long,invalid-name
    parser.add_argument("-a", action="store", type=int, help="This is the value a in y^2 = x^3 + ax + b mod m", required=False)
    parser.add_argument("-b", action="store", type=int, help="This is the value b in y^2 = x^3 + ax + b mod m", required=False)
    parser.add_argument("-m", action="store", type=int, help="This is the value m in y^2 = x^3 + ax + b mod m", required=False)
    parser.add_argument("-i", action="store", type=str, help="Input curve, space delimitted a,b,m in a file. File name", required=False)
    parser.add_argument("-px", action="store", type=int, help="This is the point value x for the generator", required=False)
    parser.add_argument("-py", action="store", type=int, help="This is the point value y for the generator", required=False)
    parser.add_argument("-pz", action="store", type=int, help="This is the point value z for the generator", required=False)
    parser.add_argument("-o", action="store", type=str, help="This is the path of the output file; stdout is default", required=False)
    parser.add_argument("--bv", action="store_true", help="This is verbose brute force", required=False)
    parser.add_argument("--brute", action="store_true", help="If the curve does not have order p where p is prime, the shortcut\
    is rendered useless, and exhaustive search can be done", required=False)
    parser.add_argument("--affine", action="store_true", help="For point generation, this converts all the points to affine(very slow)")
    args = parser.parse_args()

    x = args.px
    y = args.py
    z = args.pz
    bv = args.bv
    brute = args.brute or bv
    affine = args.affine
    inputfile = args.i
    o = args.o if args.o else "/dev/tty"
    with open(o, "w") as f:
        a = None
        b = None
        m = None
        # Parse Arguments
        if inputfile:
            try:
                with open(inputfile, "r") as inputty:
                    try:
                        (a,b,m) = [int(i) for i in inputty.readline().split()]
                    except _:
                        f.write("Curve was unparseable\n")
                        exit(1)
            except _:
                f.write("File {} is unreadable\n".format(inputfile))
                exit(1)
        else:
            a = args.a
            b = args.b
            m = args.m
        if not(a and b and m):
            f.write("No curve selected\n")
            exit(1)
        curve = Curve(a,b,m)
        # Point Routine
        # Go through order of point
        if x is not None:
            # we have a point
            z = z if z else 1
            point = Point(x,y,z,curve) if y else curve.point_from_x(x)
            if isinstance(point, list):
                if len(point) == 0:
                    f.write("This curve {} does not have a point at x = {}\n".format(curve, x))
                    exit(1)
                else:
                    point = point[0]
            if point not in curve:
                f.write("This point {} is not on the curve {}\n".format(point, curve))
                exit(1)
            for (i, kpoint) in enumerate(point.order_multiplication_generator()):
                if affine:
                    kpoint.convert_to_affine()
                s = "{}p = {}\n".format(i, kpoint)
                f.write(s)
        # Curve Routine
        else:
            count_of_max_points = 0
            for (i, point) in enumerate(curve.all_points()):
                f.write("{}\n".format(point))
            count_of_points = len(curve.points)
            f.write("{}\nThe curve\n{}\nhas {} affine points:\n".format("-"*80, curve, count_of_points))
            if not brute:
                f.write("The points with order {}(assuming {} is prime, this is the maximum order of the group) are: \n{}\n".format(count_of_points, count_of_points, "-"*80))
                # Lots of redundancy here
                for point in curve.all_points():
                    if not point.infinity:
                        opposite_point = point * (count_of_points - 1)
                        if not opposite_point.infinity:
                            opposite_point.convert_to_affine()
                            if opposite_point.x == point.x:
                                if (opposite_point + point).infinity:
                                    count_of_max_points += 1
                                    f.write("{}\n".format(point, count_of_points))
                f.write("{}\nThere are {} points with order {}\n".format("-"*80, count_of_max_points, count_of_points))
            else:
                # Brute force
                max_order = 0
                max_points = []
                for point in curve.all_points():
                    if point.infinity:
                        continue
                    if bv:
                        f.write("The order for the point {} on curve {}\n{}\n".format(point, curve, "-"*80))
                    exponentiation = point.copy()
                    i = 0
                    if bv:
                        f.write("{}p = {}\n".format(i, Point.infinity()))
                    while not exponentiation.infinity:
                        i += 1
                        if bv:
                            f.write("{}p = {}\n".format(i, exponentiation))
                        exponentiation += point
                    if bv:
                            f.write("{}p = {}\n".format(i+1, exponentiation))
                    if i > max_order:
                        max_points = [point]
                        max_order = i
                    elif i == max_order:
                        max_points.append(point)
                f.write("The points with max order {} are\n{}\n".format(max_order, "-"*80))
                total_count = 0
                for point in max_points:
                    f.write("{}\n".format(point))
                    total_count += 1
                f.write("In total there are {} points with max order {}\n".format(total_count, count_of_points))


if __name__ == "__main__":
    main()
