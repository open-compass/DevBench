import torch
import logging
import os.path
import argparse

class TrainManager(object):
    """
    The TrainManager class is used to train the model.

    Args:
        args: the arguments
        model: the model to be trained
        train_loader: the data loader for training
        validate_loader: the data loader for validation
    """
    
    def __init__(self, args: argparse.Namespace, model: torch.nn.Module, train_loader: torch.utils.data.DataLoader,
                 validate_loader: torch.utils.data.DataLoader):
        self.args = args
        self.model = model
        self.train_loader = train_loader
        self.validate_loader = validate_loader

    def train(self) -> None:
        """
        Train a TextCNN model on the given dataset.
        The training process involves setting up the optimizer, defining the training loop, and saving the best model checkpoint based on validation loss.
        """
        # set up optimizer
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.args.learning_rate)

        # create basic configuration
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)
        logging_file_path = os.path.join(self.args.output_dir, 'training_log.txt')
        os.makedirs(self.args.output_dir, exist_ok=True)
        file_handler = logging.FileHandler(logging_file_path, mode='w')
        logger.addHandler(file_handler)
        # store training info in log
        logging.info('Training started for TextCNN')

        # for reproducibility
        torch.manual_seed(self.args.random_seed)
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True

        # initialize best validation loss
        best_val_loss = float('inf')
        for epoch in range(self.args.num_epochs):
            # set model to train mode
            self.model.train()
            # reset running loss for this epoch
            train_loss = 0.0
            train_acc = 0.0
            k_batch_loss = 0.0
            k_batch_acc =0.0

            # loop through data
            for i, data in enumerate(self.train_loader):
                inputs, targets = data['input_ids'], data['label']
                inputs = torch.stack(inputs).permute(1, 0)
                if self.args.gpu:
                    inputs, targets = inputs.cuda(), targets.cuda()
                # clear gradients
                optimizer.zero_grad()
                # forward pass
                outputs = self.model(inputs)
                preds = outputs.argmax(dim=1)
                # calculate loss
                loss = torch.nn.CrossEntropyLoss()(outputs, targets)
                # backward pass
                loss.backward()
                # optimizer step
                optimizer.step()
                # track running loss
                train_loss += loss.item()
                k_batch_loss += loss.item()
                # compute metrics
                accuracy = torch.sum(preds == targets).float()
                train_acc += accuracy
                k_batch_acc += accuracy
                # log metrics
                if (i+1) % self.args.train_log_per_k_batch == 0:
                    logging.info('[Epoch {} batch {}] Training Loss: {:.6f}, Accuracy: {:.6f}'.\
                                 format(epoch+1, i+1, k_batch_loss/self.args.train_log_per_k_batch,
                                        k_batch_acc/((self.args.train_log_per_k_batch-1)*self.args.batch_size+len(preds))))
                    k_batch_loss = 0.0
                    k_batch_acc = 0.0
            training_loss = train_loss / (i+1)
            training_acc = train_acc / self.train_loader.dataset.num_rows
            
            # set model to eval mode
            self.model.eval()
            # initialize evaluation loss
            val_loss = 0.0
            val_acc = 0.0

            # loop through data
            with torch.no_grad():
                for i, data in enumerate(self.validate_loader):
                    inputs, targets = data['input_ids'], data['label']
                    inputs = torch.stack(inputs).permute(1, 0)
                    if self.args.gpu:
                        inputs, targets = inputs.cuda(), targets.cuda()
                    outputs = self.model(inputs)
                    preds = outputs.argmax(dim=1)
                    # calculate metrics
                    loss = torch.nn.CrossEntropyLoss()(outputs, targets)
                    val_loss += loss.item()
                    accuracy = torch.sum(preds == targets).float()
                    val_acc += accuracy
            validation_loss = val_loss / (i+1)
            validation_acc = val_acc / self.validate_loader.dataset.num_rows
            # log metrics
            logging.info('[Epoch {}] Training Loss: {:.6f}, Accuracy: {:.6f}\n          Validation Loss: {:.6f}, Accuracy: {:.6f}'.\
                         format(epoch + 1, training_loss, training_acc, validation_loss, validation_acc))
            # save the model checkpoints with the smallest loss
            if epoch % self.args.save_every_n_epoch == 0 and best_val_loss > validation_loss:
                best_val_loss = validation_loss
                self._save_checkpoint(epoch, self.model, optimizer, training_loss, validation_loss)
                logging.info('[Epoch {}] Save checkpoint'.format(epoch + 1))
        logging.info('Training completed for TextCNN')


    def _save_checkpoint(self, epoch: int, model: torch.nn.Module, optimizer: torch.optim.Optimizer,
                         training_loss: float, validation_loss: float) -> None:
        """
        To save the model checkpoint.
        Args:
            epoch: the epoch number
            model: the model
            optimizer: the optimizer
            training_loss: the training loss
            validation_loss: the validation loss
        Returns:
            None
        """
        checkpoint_dict = {
          'epoch': epoch,
          'model_state_dict': model.state_dict(),
          'optimizer_state_dict': optimizer.state_dict(),
          'train_loss': training_loss,
          'validation_loss': validation_loss,
        }

        # save model checkpoint
        checkpoint_path = os.path.join(self.args.output_dir, 'best_ckpt.bin')
        torch.save(checkpoint_dict, checkpoint_path)