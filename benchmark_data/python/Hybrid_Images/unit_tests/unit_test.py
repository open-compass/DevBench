import sys

import unittest

import cv2
import numpy as np

from src import hybrid

class TestCrossCorrelation2D(unittest.TestCase):
    def setUp(self):
        self.small_height = 10
        self.small_width = 8
        self.big_height = 50
        self.big_width = 40
        self.big_img_grey = np.random.rand(self.big_height,self.big_width)
        self.small_img_grey = np.random.rand(self.small_height,self.small_width)
        self.img_rgb = np.random.rand(self.big_height,self.big_width,3)

    def test_identity_filter_grey(self):
        '''
        Tests whether the cross-correlation identity returns the original image
        '''
        identity = np.zeros((3,3))
        identity[1,1] = 1
        img_dup = hybrid.cross_correlation_2d(self.small_img_grey, identity)
        self.assertTrue(np.allclose(img_dup, self.small_img_grey, atol=1e-08), \
            msg="Failed to return original image under identity cross-correlation")

    def test_mean_filter_grey(self):
        '''
        Tests cross-correlation of greyscale image using mean filter
        '''
        mean = np.ones((3,3))
        student = hybrid.cross_correlation_2d(self.small_img_grey, mean)
        solution = cv2.filter2D(self.small_img_grey, -1, mean, borderType=cv2.BORDER_CONSTANT)

        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect cross-correlation of greyscale image using mean filter")

    def test_mean_filter_rect_grey(self):
        '''
        Tests cross-correlation of greyscale image using a rectangular mean filter
        '''
        mean = np.ones((3,5))
        student = hybrid.cross_correlation_2d(self.small_img_grey, mean)
        solution = cv2.filter2D(self.small_img_grey, -1, mean, borderType=cv2.BORDER_CONSTANT)

        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect cross-correlation of greyscale image using rectangular mean filter")

    def test_mean_filter_RGB(self):
        '''
        Tests cross-correlation of RGB image using a rectangular filter
        '''
        mean = np.ones((3,3))
        student = hybrid.cross_correlation_2d(self.img_rgb, mean)
        solution = cv2.filter2D(self.img_rgb, -1, mean, borderType=cv2.BORDER_CONSTANT)

        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect cross-correlation of RGB image using mean filter")

    def test_rand_rect_filter_RGB(self):
        '''
        Tests cross-correlation of RGB image using a random rectangular filter
        '''
        rand_filt = np.random.rand(5,7)
        student = hybrid.cross_correlation_2d(self.img_rgb, rand_filt)
        solution = cv2.filter2D(self.img_rgb, -1, rand_filt, borderType=cv2.BORDER_CONSTANT)

        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect cross-correlation of RGB image using random rectangular filter")

    def test_big_filter_grey(self):
        '''
        Tests cross-correlation of greyscale image using a filter bigger than image
        '''
        filter_height = self.small_height % 2 + self.small_height + 1
        filter_width = self.small_width % 2 + self.small_width + 1
        rand_filter = np.random.rand(filter_height, filter_width)
        student = hybrid.cross_correlation_2d(self.small_img_grey, rand_filter)
        solution = cv2.filter2D(self.small_img_grey, -1, rand_filter, borderType=cv2.BORDER_CONSTANT)

        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect cross-correlation of greyscale image using filter bigger than image")

class TestConvolve2D(unittest.TestCase):
    def setUp(self):
        self.small_height = 10
        self.small_width = 8
        self.big_height = 50
        self.big_width = 40
        self.big_img_grey = np.random.rand(self.big_height,self.big_width)
        self.small_img_grey = np.random.rand(self.small_height,self.small_width)
        self.img_rgb = np.random.rand(self.big_height,self.big_width,3)

    def test_identity_filter_grey(self):
        '''
        Tests whether the convolution identity returns the original image
        '''
        identity = np.zeros((3,3))
        identity[1,1] = 1
        img_dup = hybrid.convolve_2d(self.small_img_grey, identity)
        self.assertTrue(np.allclose(img_dup, self.small_img_grey, atol=1e-08), \
            msg="Failed to return original image under identity convolution")

    def test_mean_filter_grey(self):
        '''
        Tests convolution of greyscale image using mean filter
        '''
        mean = np.ones((3,3))
        student = hybrid.convolve_2d(self.small_img_grey, mean)
        solution = cv2.filter2D(self.small_img_grey, -1, mean, borderType=cv2.BORDER_CONSTANT)
    
        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect result convolving greyscale image using mean filter")
    
    def test_mean_filter_rect_grey(self):
        '''
        Tests convolution of greyscale image using a rectangular mean filter
        '''
        mean = np.ones((3,5))
        mean_trans = np.fliplr(np.flipud(mean))
        student = hybrid.convolve_2d(self.small_img_grey, mean)
        solution = cv2.filter2D(self.small_img_grey, -1, mean_trans, borderType=cv2.BORDER_CONSTANT)
    
        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect result convolving greyscale image using rectangular mean filter")

    def test_mean_filter_RGB(self):
        '''
        Tests convolution of RGB image using a rectangular filter
        '''
        mean = np.ones((3,3))
        student = hybrid.convolve_2d(self.img_rgb, mean)
        solution = cv2.filter2D(self.img_rgb, -1, mean, borderType=cv2.BORDER_CONSTANT)
    
        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect result convolving RGB image using mean filter")

    def test_rand_rect_filter_RGB(self):
        '''
        Tests convolution of RGB image using a random rectangular filter
        '''
        rand_filt = np.random.rand(5,7)
        rand_filt_trans = np.fliplr(np.flipud(rand_filt))
        student = hybrid.convolve_2d(self.img_rgb, rand_filt)
        solution = cv2.filter2D(self.img_rgb, -1, rand_filt_trans, borderType=cv2.BORDER_CONSTANT)
    
        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect result convolving RGB image using random rectangular filter")

    def test_big_filter_grey(self):
        '''
        Tests convolution of greyscale image using a filter bigger than image
        '''
        filter_height = self.small_height % 2 + self.small_height + 1
        filter_width = self.small_width % 2 + self.small_width + 1
        rand_filt = np.random.rand(filter_height, filter_width)
        rand_filt_trans = np.fliplr(np.flipud(rand_filt))
        student = hybrid.convolve_2d(self.small_img_grey, rand_filt)
        solution = cv2.filter2D(self.small_img_grey, -1, rand_filt_trans, borderType=cv2.BORDER_CONSTANT)
    
        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect result convolving greyscale image using filter bigger than image")

class TestGaussianKernel2D(unittest.TestCase):
    def test_5_5_5(self):
        a = np.array([[ 0.03688345,  0.03916419,  0.03995536,  0.03916419,  0.03688345],
            [ 0.03916419,  0.04158597,  0.04242606,  0.04158597,  0.03916419],
            [ 0.03995536,  0.04242606,  0.04328312,  0.04242606,  0.03995536],
            [ 0.03916419,  0.04158597,  0.04242606,  0.04158597,  0.03916419],
            [ 0.03688345,  0.03916419,  0.03995536,  0.03916419,  0.03688345]])
        self.assertTrue(np.allclose(hybrid.gaussian_blur_kernel_2d(5, 5, 5), a,
            atol=1e-08))
    
    def test_1_7_3(self):
        a = np.array([[ 0.00121496,  0.00200313,  0.00121496],
            [ 0.01480124,  0.02440311,  0.01480124],
            [ 0.06633454,  0.10936716,  0.06633454],
            [ 0.10936716,  0.18031596,  0.10936716],
            [ 0.06633454,  0.10936716,  0.06633454],
            [ 0.01480124,  0.02440311,  0.01480124],
            [ 0.00121496,  0.00200313,  0.00121496]])
        self.assertTrue(np.allclose(hybrid.gaussian_blur_kernel_2d(1, 7, 3), a,
            atol=1e-08))
    
    def test_1079_3_5(self):
        a = np.array([[ 0.06600011,  0.06685595,  0.06714369,  0.06685595,  0.06600011],
            [ 0.06628417,  0.06714369,  0.06743267,  0.06714369,  0.06628417],
            [ 0.06600011,  0.06685595,  0.06714369,  0.06685595,  0.06600011]])
        self.assertTrue(np.allclose(hybrid.gaussian_blur_kernel_2d(10.79, 3, 5),
            a, atol=1e-08))

class TestHighLowPass(unittest.TestCase):
    def setUp(self):
        self.img1 = np.array([[[ 0.98722069,  0.67420573,  0.9598271 ],
            [ 0.26670152,  0.21624121,  0.65188739],
            [ 0.00162782,  0.93263815,  0.7822223 ],
            [ 0.33158517,  0.08778013,  0.45635313]],
    
           [[ 0.74268035,  0.38774182,  0.92426742],
            [ 0.62008793,  0.88991631,  0.87039188],
            [ 0.3807554 ,  0.0592103 ,  0.77255413],
            [ 0.44321465,  0.96987623,  0.52741498]]])
        self.img2 = np.  array([[[ 0.46584548,  0.12828543,  0.41726697],
            [ 0.68833349,  0.64108587,  0.28157041],
            [ 0.29749772,  0.55255637,  0.50586397],
            [ 0.96066347,  0.66325414,  0.11909561],
            [ 0.94567935,  0.73698286,  0.29758754]],
    
           [[ 0.10567786,  0.79558737,  0.1429793 ],
            [ 0.59973743,  0.25666802,  0.66848768],
            [ 0.34788779,  0.87168821,  0.25935364],
            [ 0.96653567,  0.76967792,  0.5172395 ],
            [ 0.18750987,  0.28459867,  0.1343435 ]],
    
           [[ 0.71034047,  0.39766304,  0.34671752],
            [ 0.31162219,  0.620282  ,  0.44339969],
            [ 0.51328585,  0.36719659,  0.38316949],
            [ 0.87880974,  0.5767783 ,  0.14694409],
            [ 0.38323359,  0.06082468,  0.95484321]],
    
           [[ 0.23667426,  0.39500498,  0.28444366],
            [ 0.61267593,  0.13346715,  0.10208556],
            [ 0.47921816,  0.96659492,  0.64855224],
            [ 0.61750117,  0.20452611,  0.70070412],
            [ 0.32938294,  0.62096525,  0.50342395]]])
    
    
    def test_low_pass_2_3(self):
        r = np.array([[[ 0.3088114 ,  0.24855971,  0.39614979],
            [ 0.33504927,  0.36201988,  0.55967795],
            [ 0.22154193,  0.35337206,  0.46181069],
            [ 0.13350745,  0.23712374,  0.2895637 ]],
    
           [[ 0.30984611,  0.25329434,  0.39856696],
            [ 0.34230614,  0.35664168,  0.56242281],
            [ 0.23367623,  0.3610497 ,  0.46558965],
            [ 0.14036547,  0.23883435,  0.29052476]]])
    
        self.assertTrue(np.allclose(hybrid.low_pass(self.img1, 2, 3),
            r, atol=1e-08))
    
    def test_high_pass_2_3(self):
        r = np.array([[[ 0.67840929,  0.42564602,  0.56367731],
            [-0.06834775, -0.14577867,  0.09220944],
            [-0.21991411,  0.57926609,  0.32041161],
            [ 0.19807773, -0.14934361,  0.16678943]],
    
           [[ 0.43283425,  0.13444749,  0.52570046],
            [ 0.27778178,  0.53327464,  0.30796907],
            [ 0.14707917, -0.3018394 ,  0.30696447],
            [ 0.30284919,  0.73104188,  0.23689022]]])
        self.assertTrue(np.allclose(hybrid.high_pass(self.img1, 2, 3),
            r, atol=1e-08))
    
    def test_low_pass_9_7(self):
        r = np.array([[[ 0.17963478,  0.17124501,  0.12221388],
            [ 0.21933258,  0.20746511,  0.16113371],
            [ 0.22114507,  0.20886138,  0.16244521],
            [ 0.22029549,  0.20774176,  0.16180487],
            [ 0.18792763,  0.17151596,  0.13658299]],
    
           [[ 0.18170777,  0.17314406,  0.12382304],
            [ 0.22168257,  0.20972768,  0.1634043 ],
            [ 0.2235093 ,  0.21113553,  0.1647422 ],
            [ 0.22264545,  0.2100001 ,  0.16410069],
            [ 0.18989056,  0.17328373,  0.13859635]],
    
           [[ 0.18158356,  0.17294561,  0.12393794],
            [ 0.22135196,  0.20945285,  0.1637038 ],
            [ 0.22317083,  0.21085531,  0.16505207],
            [ 0.22230311,  0.20971788,  0.16441722],
            [ 0.18955739,  0.17295608,  0.13893827]],
    
           [[ 0.17926668,  0.17065694,  0.12255439],
            [ 0.2183528 ,  0.20665068,  0.16202127],
            [ 0.22014196,  0.20803099,  0.16336348],
            [ 0.21928093,  0.20690543,  0.16274287],
            [ 0.18694027,  0.17054497,  0.13759625]]])
        self.assertTrue(np.allclose(hybrid.low_pass(self.img2, 9, 7), r,
            atol=1e-08))
    
    def test_high_pass_9_7(self):
        r = np.array([[[ 0.2862107 , -0.04295958,  0.29505309],
            [ 0.46900091,  0.43362076,  0.12043671],
            [ 0.07635266,  0.34369499,  0.34341876],
            [ 0.74036798,  0.45551239, -0.04270926],
            [ 0.75775172,  0.5654669 ,  0.16100456]],
    
           [[-0.07602991,  0.62244331,  0.01915625],
            [ 0.37805486,  0.04694034,  0.50508338],
            [ 0.12437849,  0.66055268,  0.09461144],
            [ 0.74389022,  0.55967782,  0.35313881],
            [-0.00238069,  0.11131494, -0.00425285]],
    
           [[ 0.52875691,  0.22471744,  0.22277958],
            [ 0.09027023,  0.41082914,  0.27969589],
            [ 0.29011503,  0.15634128,  0.21811742],
            [ 0.65650664,  0.36706042, -0.01747312],
            [ 0.1936762 , -0.1121314 ,  0.81590494]],
    
           [[ 0.05740758,  0.22434804,  0.16188927],
            [ 0.39432313, -0.07318352, -0.05993572],
            [ 0.2590762 ,  0.75856393,  0.48518876],
            [ 0.39822023, -0.00237932,  0.53796125],
            [ 0.14244267,  0.45042029,  0.36582769]]])
        self.assertTrue(np.allclose(hybrid.high_pass(self.img2, 9, 7), r,
            atol=1e-08))
    
if __name__ == '__main__':
    np.random.seed(4670)
    unittest.main()
