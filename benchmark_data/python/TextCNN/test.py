import torch
import evaluate
import torch.nn as nn
import argparse


class TestManager(object):
    """
    The class for testing the model.
    
    Args:
        args (argparse.Namespace): the arguments parsed by the user.
        model (nn.Module): the model to be tested.
        data_loader (torch.utils.data.DataLoader): the data loader for testing.
    """
    def __init__(self, args: argparse.Namespace, model: nn.Module, data_loader: torch.utils.data.DataLoader):
        self.args = args
        self.model = model
        self.data_loader = data_loader

        # load metric
        self.accuracy_metric = evaluate.load('accuracy')

    def test(self) -> None:
        """
        Evaluate the model on the test set and save the evaluation results to a file.
        """
        # call model.eval()
        self.model.eval()

        # set up metrics
        total_acc = 0

        # start computing metrics
        for i, data in enumerate(self.data_loader):
            inputs, targets = data['input_ids'], data['label']
            inputs = torch.stack(inputs).permute(1, 0)
            if self.args.gpu:
                inputs, targets = inputs.cuda(), targets.cuda()
            outputs = self.model(inputs)    
            preds = outputs.argmax(dim=1)

            # compute metrics
            acc = self.accuracy_metric.compute(references=targets, predictions=preds)
            total_acc += acc['accuracy']

        # calculate average metrics  
        avg_acc = (total_acc / len(self.data_loader))

        # save evaluation results to a file
        with open('{}/eval_res.txt'.format(self.args.output_dir), 'w') as f:
            f.write('Accuracy: {:.6f}'.format(avg_acc))
        f.close()

        # print average metrics 
        print('accuracy: ', avg_acc)

