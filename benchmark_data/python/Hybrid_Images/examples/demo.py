import sys

import cv2
import numpy as np

from src.hybrid import create_hybrid_image

def main():
    left_img = cv2.imread('resources/dog.jpg')
    right_img = cv2.imread('resources/cat.jpg')
    hybrid_image = create_hybrid_image(left_img, right_img, 7.0, 13, 'low', 4.1, 8, 'high', 0.65)
    cv2.imwrite('examples/hybrid.png', hybrid_image)


if __name__ == '__main__':
    main()