#! /bin/bash
# Train TextCNN model

python main.py \
  --learning_rate 0.01 \
  --num_epochs 10 \
  --batch_size 16 \
  --train \
  --gpu \
  --output_dir './outputs'