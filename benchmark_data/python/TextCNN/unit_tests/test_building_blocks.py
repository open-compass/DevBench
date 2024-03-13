from modeling import TextCNN

import unittest
import torch.nn as nn
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
    
    def test_layers(self) -> None:
        """
        Test the existence of the specified layers
        - Embedding
        - Conv2d
        - Linear
        """
        model = TextCNN(self.model_tester.prepare_config_args(), 1000, 2)
        # flatten out nested sub-modules.
        all_layers = list(model.modules())

        # check for the existence of the specified layers.
        self.assertTrue(any(isinstance(layer, nn.Embedding) for layer in all_layers))
        self.assertTrue(any(isinstance(layer, nn.Conv2d) for layer in all_layers))
        self.assertTrue(any(isinstance(layer, nn.Linear) for layer in all_layers))


    def test_ordering(self) -> None:
        """
        Check for the partial ordering of the specified layers
        - Embedding
        - Conv2d
        - MaxPool1d (if exists)
        - Linear
        """
        model = TextCNN(self.model_tester.prepare_config_args(), 1000, 2)
        all_layers = list(model.modules())

        # extract indices of specific layers
        indices = {
            'embedding': next(i for i, layer in enumerate(all_layers) if isinstance(layer, nn.Embedding)),
            'conv2d': next(i for i, layer in enumerate(all_layers) if isinstance(layer, nn.Conv2d)),
            'linear': next(i for i, layer in enumerate(all_layers) if isinstance(layer, nn.Linear))
        }

        # check for MaxPool1d layer
        if any(isinstance(layer, nn.MaxPool1d) for layer in all_layers):
            indices['maxpool1d'] = next(i for i, layer in enumerate(all_layers) if isinstance(layer, nn.MaxPool1d))

        # verify partial ordering
        self.assertTrue(indices['embedding'] < indices['conv2d'])
        if 'maxpool1d' in indices:
            self.assertTrue(indices['conv2d'] < indices['maxpool1d'])
            self.assertTrue(indices['maxpool1d'] < indices['linear'])
        else:
            self.assertTrue(indices['conv2d'] < indices['linear'])