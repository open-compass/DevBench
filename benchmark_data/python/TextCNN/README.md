train+eval
```
$ python main.py --learning_rate=0.01 --num_epochs=4 --batch_size=16 --train --gpu --output_dir ./outputs
```

eval
```
$ python main.py --test --gpu --output_dir ./outputs
```

Run acceptance tests
```
export PYTHONPATH="/cpfs01/shared/public/libowen/Projects/DevBench/proj_data/yuxuan:$PYTHONPATH"
pytest tests/test_acceptance.py
```