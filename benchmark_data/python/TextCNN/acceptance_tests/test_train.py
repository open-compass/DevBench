import unittest
import os
import os.path
import shutil
import re

class TestTextCNN(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists('./outputs'):
            shutil.rmtree('./outputs')
        os.system('python main.py --train --num_epochs=4 --output_dir "./outputs" --gpu')

    def test_training_metric(self) -> None:
        """
        Test if the training loss and accuracy decrease after each epoch.
        """
        with open('./outputs/training_log.txt', 'r') as f:
            # read metrics from training_log.txt
            lines = f.readlines()
            epoch_metric = {}
            for line in lines:
                # get epoch, batch, loss, accuracy from training_log.txt
                m = re.match(r'\[Epoch (\d+)\] Training Loss: (.*), Accuracy: (.*)', line)
                if m:
                    epoch = int(m.group(1))
                    loss = float(m.group(2))
                    accuracy = float(m.group(3))
                    epoch_metric[epoch] = {'train_loss': loss, 'train_acc': accuracy}
                else:
                    m = re.match(r'          Validation Loss: (.*), Accuracy: (.*)', line)
                    if m:
                        loss = float(m.group(1))
                        accuracy = float(m.group(2))
                        epoch_metric[epoch].update({'eval_loss': loss, 'eval_acc': accuracy})
        f.close()

        self.assertTrue(epoch_metric[1]['train_loss'] > epoch_metric[epoch]['train_loss'])
        self.assertTrue(epoch_metric[1]['train_acc'] < epoch_metric[epoch]['train_acc'])

    def test_testing_metric(self) -> None:
        """
        Test if the testing accuracy is greater than 0.6.
        """
        # get testing accuracy from eval_res.txt
        with open('./outputs/eval_res.txt', 'r') as f:
            line = f.readline()
            print(line)
            m = re.match(r'Accuracy: (.*)', line)
            acc = float(m.group(1))
        f.close()

        self.assertTrue(acc > 0.6)