from datasets import load_dataset
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
import argparse
from typing import Tuple

class DataManager(object):
    """
    Load dataset from huggingface.
    
    Args:
        args: arguments
    """

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.dataset = load_dataset('imdb')
        self.num_classes = len(set(self.dataset['train']['label']))

    def get_data_loader(self) -> Tuple[DataLoader, DataLoader, DataLoader]:
        """
        Load dataset from huggingface.
        
        Returns:
            train_loader (DataLoader): train dataset
            validate_loader (DataLoader): validation dataset
            test_loader (DataLoader): test dataset
        """
     
        # tokenize dataset
        def tokenize_function(example):
            return self.tokenizer(example['text'], truncation=True, max_length=self.args.max_length, padding='max_length', return_tensors='pt')
        tokenized_datasets = self.dataset.map(tokenize_function, batched=True)
        # split training and evaluation dataset from the original train dataset
        train_validate_dataset = tokenized_datasets['train'].train_test_split(test_size=0.1, seed=self.args.random_seed)
        tokenized_datasets['train'], tokenized_datasets['validate'] = train_validate_dataset['train'], train_validate_dataset['test']
        
        # load data loader from tokenized dataset
        train_loader = DataLoader(tokenized_datasets['train'], batch_size=self.args.batch_size, shuffle=True)
        validate_loader = DataLoader(tokenized_datasets['validate'], batch_size=self.args.batch_size, shuffle=True)
        test_loader = DataLoader(tokenized_datasets['test'], batch_size=self.args.batch_size, shuffle=True)
        return train_loader, validate_loader, test_loader

    def get_vocab_size(self) -> int:
        """
        Get vocab size.
        """
        return self.tokenizer.vocab_size

    def get_num_classes(self) -> int:
        """
        Get number of classes.
        """
        return self.num_classes
