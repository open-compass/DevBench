import argparse
import torch
import os.path
from data import DataManager
from modeling import TextCNN
from test import TestManager
from train import TrainManager

def get_args(argv=None) -> argparse.Namespace:
    """
    Get arguments from command line.

    Args:
        argv (list): command line arguments.
    
    Returns:
        argparse.Namespace: arguments.
    """
    # parse command line arguments
    parser = argparse.ArgumentParser()

    # define parameters for training
    parser.add_argument('--learning_rate', type=float, default=1e-3)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--num_epochs', type=int, default=10)
    # define the number of neurons
    parser.add_argument('--embedding_dim', type=int, default=500)
    # define the kernel size
    parser.add_argument('--kernel_sizes', nargs='+', type=int, default=[3, 4, 5])
    # define the max length of sentences
    parser.add_argument('--max_length', type=int, default=50)
    # define the number of epoch to save the model
    parser.add_argument('--save_every_n_epoch', type=int, default=1)
    # define whether to train or test
    parser.add_argument('--train', action='store_true', default=False)
    parser.add_argument('--test', action='store_true', default=False)
    # define the path to output dir
    parser.add_argument('--output_dir', required=True, type=str)
    # define whether to use gpu
    parser.add_argument('--gpu', action='store_true', default=False)
    # define the number of batch to log the training loss
    parser.add_argument('--train_log_per_k_batch', type=int, default=10)
    # define the random seed
    parser.add_argument('--random_seed', type=int, default=42)
    return parser.parse_args(argv)

def main():
    """
    Train and test the TextCNN model.
    """
    # get arguments
    args = get_args()
    # mkdir if necessary
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # instantiate DataManager and load data
    data_manager = DataManager(args)
    train_loader, validate_loader, test_loader = data_manager.get_data_loader()
    vocab_size = data_manager.get_vocab_size()
    num_classes = data_manager.get_num_classes()

    # instantiate TextCNN model
    model = TextCNN(args, vocab_size, num_classes)
    # move model to gpu if argument is specified
    if args.gpu and torch.cuda.is_available():
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        torch.cuda.set_device(device)
        model.cuda()

    # instantiate TrainManager and Train
    if args.train:
        train_manager = TrainManager(args, model, train_loader, validate_loader)
        train_manager.train()

    # instantiate TestManager and Test
    if args.test:
        checkpoint_path = os.path.join(args.output_dir, 'best_ckpt.bin')
        model.load_state_dict(torch.load(checkpoint_path)['model_state_dict'])
    test_manager = TestManager(args, model, test_loader)
    test_manager.test()

if __name__ == '__main__':
    main()
