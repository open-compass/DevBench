# Architecture Design
Below is a text-based representation of the file tree. 
```bash
├── .gitignore
├── examples
│   ├── run_test.sh
│   └── run_train.sh
├── data.py
├── main.py
├── modeling.py
├── test.py
├── train.py
├── outputs
│   ├── training_log.txt
│   ├── best_ckpt.bin
│   └── eval_res.txt
```

Output:
- trianing_log.txt: for every batch, record the training CE-loss and accuracy in the log; for every epoch record the training and evaluation loss and accuracy in the log.
- best_ckpt.bin: save the model checkpoint with the highest evaluation accuracy during training.
- eval_res.txt: print the average accuracy of a trained model checkpoint on the test sets.
The outputs folder should be ignored in git.

Examples:
- To train a model, run `sh ./examples/run_train.sh` to train and evaluate the model. An example of the script `run_train.sh` is shown as follows.
```bash
python main.py \
  --learning_rate 0.01 \
  --num_epochs 10 \
  --batch_size 16 \
  --embedding_dim 300\
  --kernel_sizes 3 4 5\
  --max_length 50\
  --save_every_n_epoch 2\
  --train \
  --gpu \
  --output_dir './outputs'\
  --train_log_per_k_batch 20\
  --random_seed 20
``` 
- To test a trained checkpoint, run `sh ./examples/run_test.sh` to evaluate. An example of the script `run_test.sh` is shown as follows.
```bash
python main.py \
  --test \
  --gpu \
  --output_dir './outputs'
```

`main.py`:
- get_args(): parse arguments from command line.
- main(): instantiates TextCNN and Train/Test managers, and controls the training and testing process for the model. By setting arguments, it loads the necessary data, moves the model to a GPU if specified, and saves or loads appropriate checkpoints.
The standalone functions are all placed in the main.py file.

`data.py`:
- class DataManager(args): load and preprocess IMDb dataset from HuggingFace datasets.
    - get_data_loader(): load and preprocess IMDb dataset from HuggingFace datasets using `bert-base-uncased` tokenizer.
    - get_vocab_size(): get vocab size of tokenizer.
    - get_num_classes(): get number of classes of datasets.

`modeling.py`:
- class TextCNN(args, vocab_size, num_classes): initialize the model structure and parameters.
    - forward(): input data forward to get logits.

`train.py`:
- class TrainManager(args, model, train_loader, validate_loader): handling the model training process.
    - train(): train the model on training dataset and log accuracy and loss.
    - _save_checkpoint(): save the best checkpoint.

`test.py`:
- class TestManager(args, model, test_loader): handling the trained model testing process.
    - test(): test the trained model on testing dataset and print accuracy to output file.

