import unittest
import torch
from modeling import TextCNN
from data import DataManager
from train import TrainManager
import unittest
import re
from types import SimpleNamespace
import os

class TextCNNTester:

    def prepare_config_args(self) -> SimpleNamespace:
        """
        Create a mock argument object that mimics the output of parser.parse_args().
        """
        args = SimpleNamespace(
            learning_rate=1e-3,
            batch_size=32,
            num_epochs=10,
            embedding_dim=500,
            kernel_sizes=[3,4,5],
            max_length=50,
            save_every_n_epoch=1,
            train=False,
            test=False,
            output_dir='./outputs',
            gpu=True,
            train_log_per_k_batch=10,
            random_seed=1024
        )

        return args
class TestTextCNN(unittest.TestCase):
    def setUp(self) -> None:
        """
        Train a model and save the best checkpoint.
        """
        self.model_tester = TextCNNTester()
        # train a TextCNN model
        self.args = self.model_tester.prepare_config_args()
        data_manager = DataManager(self.args)
        self.train_loader, self.validate_loader, _ = data_manager.get_data_loader()
        self.vocab_size = data_manager.get_vocab_size()
        self.num_classes = data_manager.get_num_classes()
        self.model = TextCNN(self.args, self.vocab_size, self.num_classes)
    
        if torch.cuda.is_available():
            self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            torch.cuda.set_device(self.device)
            self.model.cuda()
    
        train_manager = TrainManager(self.args, self.model, self.train_loader, self.validate_loader)
        train_manager.train()

    def test_save_best_checkpoints(self) -> None:
        """
        Test whether the best checkpoint is saved.
        """
        # test whether the best checkpoint is saved
        self.assertTrue(os.path.exists('./outputs/best_ckpt.bin'))

        # test whether the best checkpoint is the best checkpoint in the training log
        with open('./outputs/training_log.txt', 'r') as f:
            lines = f.readlines()
            best_loss = float('inf')
            for line in lines:
                m = re.match(r'          Validation Loss: (.*), Accuracy: (.*)', line)
                if m:
                    loss = float(m.group(1))
                    if loss < best_loss:
                        best_loss = loss
        f.close()
        saved_loss = torch.load('./outputs/best_ckpt.bin')['validation_loss']
        self.assertTrue(abs(best_loss-saved_loss)<10**-2)