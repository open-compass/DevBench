import unittest
import sys
import os

from pso.cost_functions import sphere


class TestCostFunctions(unittest.TestCase):

    def test_sphere(self):
        x = [1, 2, 3]
        result = sphere(x)
        self.assertEqual(result, 14)

        x = [0, 0, 0]
        result = sphere(x)
        self.assertEqual(result, 0)

        x = [-1, -2, -3]
        result = sphere(x)
        self.assertEqual(result, 14)


if __name__ == '__main__':
    unittest.main()