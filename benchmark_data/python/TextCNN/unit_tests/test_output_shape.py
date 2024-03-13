import unittest
import torch
from modeling import TextCNN
from data import DataManager
import unittest
from types import SimpleNamespace

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
            gpu=False,
            train_log_per_k_batch=10,
            random_seed=1024
        )
        return args

class TestTextCNN(unittest.TestCase):
    def setUp(self) -> None:
        self.model_tester = TextCNNTester()

    def test_forward_shape(self) -> None:
        """
        The test function that tests the output shape of TextCNN.
        """
        # prepare data and model
        data_manager = DataManager(self.model_tester.prepare_config_args())
        data_loader, _, _ = data_manager.get_data_loader()
        num_classes = data_manager.get_num_classes()
        vocab_size = data_manager.get_vocab_size()
        # get the first batch of data
        data = next(iter(data_loader))
        model = TextCNN(self.model_tester.prepare_config_args(), vocab_size, num_classes)
        inputs, targets = data['input_ids'], data['label']
        inputs = torch.stack(inputs).permute(1, 0)
        # forward pass
        output = model(inputs)
        self.assertEqual(output.shape[0], 32)
        self.assertEqual(output.shape[1], 2)