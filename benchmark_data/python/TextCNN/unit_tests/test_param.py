import unittest
import torch
from modeling import TextCNN
from data import DataManager
from train import TrainManager
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
            num_epochs=1,
            embedding_dim=500,
            kernel_sizes=[3, 4, 5],
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
        self.model_tester = TextCNNTester()
        self.args = self.model_tester.prepare_config_args()
        # Set device to GPU if available
        if torch.cuda.is_available():
            self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            torch.cuda.set_device(self.device)

    def test_param_update(self) -> None:
        """
        Test whether the parameter of model are updated after training.
        """
        # initialize model and data manager
        data_manager = DataManager(self.args)
        train_loader, validate_loader, _ = data_manager.get_data_loader()
        vocab_size = data_manager.get_vocab_size()
        num_classes = data_manager.get_num_classes()
        model = TextCNN(self.args, vocab_size, num_classes)
        model.to(self.device)
        # get the initial parameter of model
        embedding_base = model.embedding.weight.data.clone()
        fc_base = model.fc.weight.data.clone()
        convs_base = [model.convs[i].weight.data.clone() for i in range(len(self.args.kernel_sizes))]
        
        # train model
        train_manager = TrainManager(self.args, model, train_loader, validate_loader)
        train_manager.train()
        
        # check whether the parameter of model are updated
        self.assertFalse(torch.allclose(embedding_base, model.embedding.weight.data))
        self.assertFalse(torch.allclose(fc_base, model.fc.weight.data))
        for i in range(len(self.args.kernel_sizes)):
            self.assertFalse(torch.allclose(convs_base[i], model.convs[i].weight.data))
