#! /bin/bash
# Test the trained TextCNN model

python main.py \
  --test \
  --gpu \
  --output_dir './outputs'
