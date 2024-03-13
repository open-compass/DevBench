import unittest

import sys
import cv2
import numpy as np
from src.hybrid import create_hybrid_image

class TestHybridImage(unittest.TestCase):
    def test(self):
        left_img = cv2.imread('resources/dog.jpg')
        right_img = cv2.imread('resources/cat.jpg')
        hybrid_image_ref = cv2.imread('resources/hybrid.png')
        hybrid_image_test = create_hybrid_image(left_img, right_img, 7.0, 13, 'low', 4.1, 8, 'high', 0.65)
        self.assertTrue(np.allclose(hybrid_image_ref, hybrid_image_test, atol=1.0))

if __name__ == '__main__':
    unittest.main()