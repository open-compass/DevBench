import unittest
import os
import os.path
import re
import shutil

class TestTextCNN(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists('./outputs'):
            shutil.rmtree('./outputs')
        os.system('python main.py --train --num_epochs=4 --output_dir "./outputs" --gpu')
        os.system('python main.py --test --output_dir "./outputs" --gpu')

    def test_testing_metric(self) -> None:
        """
        Test if the testing accuracy is greater than 0.6.
        """
        # get testing accuracy from eval_res.txt
        with open('./outputs/eval_res.txt', 'r') as f:
            line = f.readline()
            m = re.match(r'Accuracy: (.*)', line)
            acc = float(m.group(1))
        f.close()

        self.assertTrue(acc > 0.6)