import unittest
from main import get_args
import sys

class TestGetArgs(unittest.TestCase):

    def setUp(self):
        self.original_argv = sys.argv

    def tearDown(self):
        sys.argv = self.original_argv

    def test_missing_required_arguments(self) -> None:
        """
        Missing required arguments should result in SystemExit(2).
        """
        sys.argv = ['main.py']
        with self.assertRaises(SystemExit) as cm:
            get_args()
        self.assertEqual(cm.exception.code, 2)
    
    
    
    def test_all_required_arguments_present(self) -> None:
        """
        Test whether all required arguments are present.
        """
        sys.argv = ['main.py', '--output_dir', '/path/to/output']
        args = get_args()
        self.assertEqual(args.output_dir, '/path/to/output')
    
    
    def test_override_args(self) -> None:
        """
        Test whether args are overriden correctly. 
        """
        sys.argv = [
            'main.py',
            '--learning_rate', '0.001',
            '--batch_size', '64',
            '--num_epochs', '20',
            '--embedding_dim', '1000',
            '--kernel_sizes', '2', '3', '4',
            '--max_length', '100',
            '--save_every_n_epoch', '2',
            '--train',
            '--test',
            '--output_dir', '/path/to/output',
            '--gpu',
            '--train_log_per_k_batch', '20',
            '--random_seed', '42'
        ]
        args = get_args()
        self.assertEqual(args.learning_rate, 0.001)
        self.assertEqual(args.batch_size, 64)
        self.assertEqual(args.num_epochs, 20)
        self.assertEqual(args.embedding_dim, 1000)
        self.assertEqual(args.kernel_sizes, [2,3,4])
        self.assertEqual(args.max_length, 100)
        self.assertEqual(args.save_every_n_epoch, 2)
        self.assertTrue(args.train)
        self.assertTrue(args.test)
        self.assertEqual(args.output_dir, '/path/to/output')
        self.assertTrue(args.gpu)
        self.assertEqual(args.train_log_per_k_batch, 20)
        self.assertEqual(args.random_seed, 42)

