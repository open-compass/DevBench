# UML sequence
`Global_functions` is a fake class to host global functions.

```mermaid
sequenceDiagram
    participant DataManager
    participant TextCNN
    participant TrainManager
    participant TestManager
    participant Global_functions
    participant main
    main->>Global_functions: get_args()
    Global_functions->>main: args
    main->>DataManager: __init__(args)
    DataManager->>main: data_manager
    main->>data_manager: get_data_loader()
    data_manager->>main: train_loader, validate_loader, test_loader
    main->>data_manager: get_vocab_size()
    data_manager->>main: vocab_size
    main->>data_manager: get_num_classes()
    data_manager->>main: num_classes
    main->>TextCNN: __init__(args, vocab_size, num_classes)
    TextCNN->>main: model
    main->>TrainManager: __init__(args, model, train_loader, validate_loader)
    TrainManager->>main: train_manager
    main->>TestManager: __init__(args, model, test_loader)
    TestManager->>main: test_manager
    main->>main: if args.train
    main->>train_manager: train()
    main->>main: if args.test
    main->>test_manager: test()
```