import unittest
import torch
from modeling import TextCNN
from data import DataManager
from train import TrainManager
from types import SimpleNamespace


class TextCNNTester:

    def prepare_config_args(self) -> SimpleNamespace:
        """
        Create mock arguments object that mimic the output of parser.parse_args().
        """
        default_args = SimpleNamespace(
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
            random_seed=42
        )
        alternate_args = SimpleNamespace(
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
            random_seed=100
        )
        return default_args, alternate_args

class TestTextCNN(unittest.TestCase):
    def setUp(self) -> None:
        self.model_tester = TextCNNTester()
        # train the default model
        self.default_args, self.alternate_args = self.model_tester.prepare_config_args()
        data_manager = DataManager(self.default_args)
        self.train_loader, self.validate_loader, _ = data_manager.get_data_loader()
        self.vocab_size = data_manager.get_vocab_size()
        self.num_classes = data_manager.get_num_classes()
        self.default_trained_model = TextCNN(self.default_args, self.vocab_size, self.num_classes)

        if torch.cuda.is_available():
            self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            torch.cuda.set_device(self.device)
        self.default_trained_model.to(self.device)

        train_manager = TrainManager(self.default_args, self.default_trained_model, self.train_loader,
                                     self.validate_loader)
        train_manager.train()
        
    def test_same_parameter(self) -> None:
        """
        Test whether the trained model is the same as the default trained model while the random seed remains.
        This test is performed by comparing the weights of the trained models with the same random seed.
        """
        # train the model with the same random seed
        model_same = TextCNN(self.default_args, self.vocab_size, self.num_classes)
        model_same.to(self.device)
        train_manager = TrainManager(self.default_args, model_same, self.train_loader, self.validate_loader)
        train_manager.train()

        # compare the weights of the trained model
        self.assertTrue(
            torch.allclose(self.default_trained_model.embedding.weight.data, model_same.embedding.weight.data))
        self.assertTrue(torch.allclose(self.default_trained_model.fc.weight.data, model_same.fc.weight.data))
        self.assertTrue(torch.allclose(self.default_trained_model.fc.bias.data, model_same.fc.bias.data))
        for i in range(len(self.default_args.kernel_sizes)):
            self.assertTrue(
                torch.allclose(self.default_trained_model.convs[i].weight.data, model_same.convs[i].weight.data))
            self.assertTrue(
                torch.allclose(self.default_trained_model.convs[i].bias.data, model_same.convs[i].bias.data))

    def test_different_parameter(self) -> None:
        """
        Test whether the trained model is different from the default trained model while the random seed changes.
        This test is performed by comparing the weights of the trained models with the different random seed.
        """
        # train the model with the different random seed
        model_different = TextCNN(self.alternate_args, self.vocab_size, self.num_classes)
        model_different.to(self.device)
        train_manager = TrainManager(self.alternate_args, model_different, self.train_loader, self.validate_loader)
        train_manager.train()

        # compare the weights of the trained model
        self.assertFalse(
            torch.allclose(self.default_trained_model.embedding.weight.data, model_different.embedding.weight.data))
        self.assertFalse(torch.allclose(self.default_trained_model.fc.weight.data, model_different.fc.weight.data))
        self.assertFalse(torch.allclose(self.default_trained_model.fc.bias.data, model_different.fc.bias.data))
        for i in range(len(self.alternate_args.kernel_sizes)):
            self.assertFalse(
                torch.allclose(self.default_trained_model.convs[i].weight.data, model_different.convs[i].weight.data))
            self.assertFalse(
                torch.allclose(self.default_trained_model.convs[i].bias.data, model_different.convs[i].bias.data))
