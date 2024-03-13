# UML class
`Global_functions` is a fake class to host global functions.

```mermaid
classDiagram
    class Global_functions {
        +get_args()
    }
    class DataManager {
        +__init__(args)
        +get_data_loader()
        +get_vocab_size()
        +get_num_classes()
    }
    class TextCNN {
        +__init__(args, vocab_size, num_classes)
        +forward()
    }
    class TrainManager {
        +__init__(args, model, train_loader, validate_loader)
        +train()
        +_save_checkpoint()
    }
    class TestManager {
        +__init__(args, model, test_loader)
        +test()
    }
    DataManager --> TextCNN
    TextCNN --> TrainManager
    TextCNN --> TestManager
```