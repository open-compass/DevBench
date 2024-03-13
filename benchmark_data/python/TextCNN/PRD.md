# Introduction
The purpose of this project is to develop a code repository that implements the TextCNN model for movie review sentiment classification using the PyTorch library. This repository should include all the necessary components and features to support the development of the model.
# Goals
The objective of this project is to construct and evaluate a TextCNN model using the PyTorch library for text classification. This includes the data pre-processing, the training of the model and evaluation of the model performance via accuracy.
# Features and Functionalities
The following features and functionalities are expected in the project:
- Modeling: 
    - ability to define and manage model-related settings such as kernel sizes, dimension of embedding, maximum length of sequence;
    - ability to configure model training settings such as learning rate, batch size, number of epochs;
    - ability to define the custom parameter during training such as number of epoch to save model and number of batch to log training loss;
    - ability to save the model checkpoint with the highest evaluation accuracy during training;
    - ability to reproduce the training and testing results when random seeds are fixed.
    - ability to log training loss and accuracy for every k batches;
    - ability to log loss and accuracy for both train and validation sets for each epoch;
    - ability to calculate the accuracy of model output on test dataset;
    - ability to construct the TextCNN model using PyTorch, where the structure of a TextCNN model consists of an embedding layer, a series of convolutional layers, a maximum pooling layer, relu activation function, and a fully connected layer in a fixed order.
- Data:
    - ability to load and pre-process the IMDb dataset from HuggingFace datasets;
    - ability to load `bert-base-uncased` tokenizer from HuggingFace transformers to convert text into vectors;
    - ability to split the train dataset into train and validation sets, specify the split ratio to 0.1.
- Examples:
    - example scripts to run the code for both training and testing.
# Technical Constraints
- The repository should support building modeling frameworks using pytorch. 
- The repository should support training model using pytorch instead of the trainer api of transformers.
# Requirements
## Dependencies
- transformers library
- datasets library
- evaluate library
- PyTorch library
# Usage
To train a model, run the following script
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
To test a trained checkpoint in a specified `output_dir`, run the following script. 
```bash
python main.py \
  --test \
  --gpu \
  --output_dir './outputs'
```
## Command Line configuration arguments
 - learning_rate (float, optional) - A value representing the learning rate for training, with a default value of 1e-3.
 - batch_size (int, optional) - A value representing the batch size for training, with a default value of 32.
 - num_epochs (int, optional) - A value representing the number of epochs for training, with a default value of 10.
 - embedding_dim (int, optional) - A value representing the number of neurons in the layer, with a default value of 500.
 - kernel_sizes (lis, optional) - A list of values representing the kernel sizes, with a default value of [3, 4, 5].
 - max_length (int, optional) - A value representing the maximum length of sentences, with a default value of 50.
 - save_every_n_epoch (int, optional) - A value representing the number of epochs to save the model, with a default value of 1.
 - train (Boolean, optional) - A boolean value representing whether to train the model, with a default value of FALSE.
 - test (Boolean, optional) - A boolean value representing whether to test the model, with a default value of FALSE.
 - output_dir (str, required) - A string value representing the path to output directory.
 - gpu (Boolean, optional) - A boolean value representing whether to use GPU, with a default value of FALSE.
 - train_log_per_k_batch (int, optional) - A value representing the number of batch to log the training loss, with a default value of 10.
 - random_seed (int, optional) - A value representing the random seed, with a default value of 42.
# Acceptance Criteria
The repository should cover acceptance testing for both training and testing modes, by setting command line parameter to `--train` and `--test`.
- For the training mode, the model training logs will be tested if the training loss decreases between the first epoch and the last epoch, and if the accuracy of the model evaluation results is above 0.6.
- For the testing mode, the terminal output will be tested whether the accuracy of the given trained model on the test dataset is above 0.6.
# Terms/Concepts Explanation
TextCNN (Convolutional Neural Networks for Text Classification) is a convolutional neural network model introduced by Yoon Kim in 2014. It works by constructing and training a convolutional neural network (CNN) model to classify text into predefined labels. The model performs well and is considered one of the widely applicable architectures for text classification. The IMDb dataset is a collection of over 25000 movie reviews from users on the Internet Movie Database website. The dataset is typically used to train or test machine learning models for movie sentiment analysis.