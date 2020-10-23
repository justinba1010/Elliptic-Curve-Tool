"""
Justin Baum
20 October 2020
test.py
Sanity Check
"""

import unittest
from curve import Curve
from point import Point
from random import randint
class PointOperations(unittest.TestCase):
    @staticmethod
    def transform_points_to_Points(points, curve):
        return [Point(x,y,1,curve) for (x,y) in points]
    # def test_example74(self):
    #     curve = Curve(-36, 0, 10*10)
    #     p = Point(-3, 9, 1, curve)
    #     q = Point(-2, 8, 1, curve)
    #     expected = Point(6, 0, 1, curve)
    #     actual = p + q
    #     actual.convert_to_affine
    #     self.assertTrue(actual == expected)
    def test_addition(self):
        curve = Curve(1, 1, 31)
        p1 = Point(0, 1, 1, curve)
        p2 = Point(0, 1, 1, curve)
        expected = Point(8, 26, 1, curve)
        actual = p1 + p2
        actual.convert_to_affine()
        self.assertEqual(actual, expected)
    # def test_multiplication(self):
    #     curve = Curve(1,1,31)
    #     p1 = Point(0, 1, curve)
    #     expected = Point(28, 8, curve)
    #     k = 10
    #     self.assertEqual(p1 * k, expected)
    def test_curve_1_1_31(self):
        curve = Curve(1,1,31)
        p1 = Point(0,1,1,curve)
        expected = [
            (0,1),
            (8, 26),
            (10,22),
            (22,21),
            (17,23),
            (19,20),
            (13,17),
            (23,16),
            (12,6),
            (28,8),
            (5,21),
            (11,17),
            (7,17),
            (21,13),
            (4,10),
            (3,0),
            (4,21),
            (21,18),
            (7,14),
            (11,14),
            (5,10),
            (28,23),
            (12,25),
            (23,15),
            (13,14),
            (19,11),
            (17,8),
            (22,10),
            (10,9),
            (8,5),
            (0,30)
        ]
        expected = [Point.infinity()] + PointOperations.transform_points_to_Points(expected, curve) + [Point.infinity()]
        actual = [p1 * k for k in range(0,34)]
        for actuality in actual:
            actuality.convert_to_affine()
        #print("\n".join("{} vs {}".format(p1, p2) for (p1, p2) in zip(actual, expected)))
        self.assertTrue(all([actuali == expectedi for (actuali, expectedi) in zip(actual, expected)]))
    # def test_points(self):
    #     curve = Curve(1,6,11)
    #     points = [
    #             (2,4),
    #             (2,7),
    #             (3,5),
    #             (3,6),
    #             (5,2),
    #             (5,9),
    #             (7,2),
    #             (7,9),
    #             (8,3),
    #             (8,8),
    #             (10,2),
    #             (10,9)
    #             ]
    #     points = PointOperations.transform_points_to_Points(points, curve)
    #     self.assertTrue(all([point in curve for point in points]))
    # def test_points_all_11593(self):
    #     curve = Curve(101,13,11593)
    #     points = curve.all_points()
    #     self.assertTrue(all([point in curve for point in points]))
    # def test_points_all_100003(self):
    #     curve = Curve(1234,8413,100003)
    #     points = curve.all_points()
    #     self.assertTrue(all([point in curve for point in points]))
    # def test_order(self):
    #     curve = Curve(24323,34324,100003)
    #     point = None
    #     while not point:
    #         point = curve.point_from_x(randint(0,100000))
    #     point = point[0]
    #     order = point.order_multiplication()
    #     self.assertTrue(len(order) > 0)
    # def test_order_on_curve(self):
    #     """
    #     Testing speed
    #     """
    #     curve = Curve(13,17,1009)
    #     point = None
    #     while not point:
    #         point = curve.point_from_x(randint(0,1000000))
    #     point = point[0]
    #     order = point.order_multiplication()
    #     orders = [(p * i) and (p * i) in curve for (i, p) in enumerate(order)]
    #     self.assertTrue(all(orders))


if __name__ == "__main__":
    unittest.main()
