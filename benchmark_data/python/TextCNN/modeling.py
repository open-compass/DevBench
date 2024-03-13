import torch
import torch.nn as nn
import torch.nn.functional as F
import argparse

class TextCNN(nn.Module):
    """
    TextCNN model for text classification
    
    Args:
        args (argparse.Namespace): arguments
        vocab_size (int): vocabulary size
        num_classes (int): number of classes
    """
    def __init__(self, args: argparse.Namespace, vocab_size: int, num_classes: int):
        super().__init__()
        self.args = args

        # Specify the model layers
        self.embedding = nn.Embedding(vocab_size, args.embedding_dim)
        self.convs = nn.ModuleList([
           nn.Conv2d(1, 1, (kernel_size, args.embedding_dim))
           for kernel_size in args.kernel_sizes
        ])
        self.fc = nn.Linear(len(args.kernel_sizes), num_classes)

        # Initialize weights and biases
        torch.manual_seed(self.args.random_seed)
        if self.args.gpu:
            torch.cuda.manual_seed(self.args.random_seed)
        nn.init.xavier_normal_(self.embedding.weight)
        for i in range(len(self.convs)):
            nn.init.xavier_normal_(self.convs[i].weight)
            self.convs[i].bias.data.zero_()
        nn.init.xavier_normal_(self.fc.weight)
        self.fc.bias.data.zero_()


    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        # embedding layer
        x = self.embedding(inputs)
        x = x.view(-1, 1, self.args.max_length, self.args.embedding_dim)
        # convolution layers
        x = [conv(x) for conv in self.convs]
        x = [i.squeeze(3) for i in x]
        x = [F.relu(i) for i in x]
        # max pooling layers
        x = [F.max_pool1d(i,i.size(2)) for i in x]
        # flatten
        x = torch.cat(x, dim=1)
        x = x.reshape(x.size(0), -1)
        # fully-connected layers
        x = self.fc(x)
        return x
