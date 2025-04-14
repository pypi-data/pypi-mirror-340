# PyDeevo Cheat Sheet

## Core Components

### Initialization

```python
from pydeevo import PyDeevo

# Initialize PyDeevo with output directory
pydeevo = PyDeevo(base_dir="./my_project")
```

### Hyperparameter Optimization

```python
# Define model parameters
model_kwargs = {
    'architecture': [784, 256, 128, 10],  # For MLP
}

# Define hyperparameter spaces
param_spaces = {
    'learning_rate': lambda trial: trial.suggest_float('learning_rate', 1e-4, 1e-1, log=True),
    'optimizer_class': lambda trial: trial.suggest_categorical('optimizer_class', [
        torch.optim.SGD,
        torch.optim.Adam,
        torch.optim.RMSprop
    ]),
    'optimizer_kwargs': lambda trial: {
        'weight_decay': trial.suggest_float('weight_decay', 1e-6, 1e-3, log=True)
    }
}

# Run optimization
best_params = pydeevo.optimize_hyperparameters(
    model_class=FlexibleModule,
    model_kwargs=model_kwargs,
    train_loader=train_loader,
    val_loader=val_loader,
    param_spaces=param_spaces,
    metric_name="val_loss",  # Metric to optimize
    direction="minimize",    # Direction to optimize
    n_trials=20,             # Number of trials
    max_epochs=10            # Epochs per trial
)
```

### Architecture Search

```python
# For MLP architecture
result = pydeevo.evolve_architecture(
    input_shape=784,           # Flattened input size
    output_size=10,            # Output size (e.g., number of classes)
    train_loader=train_loader,
    val_loader=val_loader,
    network_type="mlp",        # "mlp" or "cnn"
    population_size=10,        # GA population size
    num_generations=10,        # Number of generations
    hp_trials_per_arch=5,      # HP trials per architecture
    max_epochs=10,             # Epochs per HP trial
    metric_name="val_acc",     # Metric to optimize
    direction="maximize"       # Direction to optimize
)

# For CNN architecture
result = pydeevo.evolve_architecture(
    input_shape=(3, 32, 32),   # (channels, height, width)
    output_size=10,            # Number of classes
    train_loader=train_loader,
    val_loader=val_loader,
    network_type="cnn",
    # Other parameters same as above
)

# Access results
best_architecture = result["best_architecture"]
best_hyperparams = result["best_hyperparameters"]
summary = result["summary"]    # Full search history
```

### Model Training

```python
# Create a model with best architecture/hyperparameters
model = FlexibleModule(
    architecture=best_architecture,
    **best_hyperparams
)

# Train the model
trainer, metrics = pydeevo.train_model(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    test_loader=test_loader,
    max_epochs=100,
    patience=10,               # Early stopping patience
    monitor="val_loss",        # Metric to monitor
    mode="min"                 # Min or max the metric
)

# Access test metrics
print(f"Test metrics: {metrics}")
```

### Loading Models

```python
# Load model from checkpoint
model = pydeevo.load_best_model(
    model_class=FlexibleModule,
    checkpoint_path="./path/to/checkpoint.ckpt",  # Optional - will find latest if not provided
    # Model parameters needed for reconstruction
    architecture=[784, 256, 128, 10]
)
```

## Model Classes

### FlexibleModule (MLP)

```python
from pydeevo.models.base import FlexibleModule

# Create MLP
model = FlexibleModule(
    architecture=[784, 256, 128, 10],  # Layer sizes
    learning_rate=0.001,
    activation=torch.nn.ReLU,
    loss_fn=torch.nn.functional.cross_entropy,
    optimizer_class=torch.optim.Adam,
    optimizer_kwargs={'weight_decay': 1e-5}
)
```

### CNNModule

```python
from pydeevo.models.base import CNNModule

# Create CNN
model = CNNModule(
    conv_architecture=[
        {'filters': 32, 'kernel_size': 3, 'pool_size': 2},
        {'filters': 64, 'kernel_size': 3, 'pool_size': 2},
    ],
    fc_architecture=[128, 10],  # FC layer sizes (output 10 for 10 classes)
    input_shape=(3, 32, 32),    # (channels, height, width)
    learning_rate=0.001,
    optimizer_class=torch.optim.Adam
)
```

## Common Workflows

### Full Architecture Search Workflow

```python
# 1. Initialize PyDeevo
pydeevo = PyDeevo(base_dir="./search_project")

# 2. Prepare data
train_loader, val_loader, test_loader = prepare_data()

# 3. Evolve architecture
result = pydeevo.evolve_architecture(
    input_shape=input_shape,
    output_size=num_classes,
    train_loader=train_loader,
    val_loader=val_loader,
    network_type="mlp",  # or "cnn"
    population_size=10,
    num_generations=10
)

# 4. Get best architecture and hyperparameters
best_architecture = result["best_architecture"]
best_hyperparams = result["best_hyperparameters"]

# 5. Create final model
model = FlexibleModule(
    architecture=best_architecture,
    **best_hyperparams
)

# 6. Train model
trainer, metrics = pydeevo.train_model(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    test_loader=test_loader,
    max_epochs=100
)
```

### Hyperparameter Optimization Workflow

```python
# 1. Initialize PyDeevo
pydeevo = PyDeevo(base_dir="./hyperopt_project")

# 2. Prepare data
train_loader, val_loader, test_loader = prepare_data()

# 3. Define fixed architecture
architecture = [784, 256, 128, 10]  # For MNIST example

# 4. Define hyperparameter spaces
param_spaces = {
    'learning_rate': lambda trial: trial.suggest_float('learning_rate', 1e-4, 1e-1, log=True),
    'optimizer_kwargs': lambda trial: {
        'weight_decay': trial.suggest_float('weight_decay', 1e-6, 1e-3, log=True)
    }
}

# 5. Optimize hyperparameters
best_params = pydeevo.optimize_hyperparameters(
    model_class=FlexibleModule,
    model_kwargs={'architecture': architecture},
    train_loader=train_loader,
    val_loader=val_loader,
    param_spaces=param_spaces
)

# 6. Create and train final model
model = FlexibleModule(
    architecture=architecture,
    **best_params
)

trainer, metrics = pydeevo.train_model(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    test_loader=test_loader
)
```

## Tips

- **Hyperparameter Spaces**: Optuna supports many distribution types:
  - `suggest_float`: Floating point values (use `log=True` for log scale)
  - `suggest_int`: Integer values
  - `suggest_categorical`: Select from a list of options
  - `suggest_uniform`: Uniform distribution

- **Architecture Search**: For faster results, use smaller:
  - `population_size`: 5-10 for quick searches
  - `num_generations`: 3-5 for initial tests
  - `hp_trials_per_arch`: 2-3 for preliminary results

- **Training**: Use early stopping to avoid overfitting:
  - Set `patience=10` to stop if no improvement for 10 epochs
  - Set appropriate `max_epochs` based on dataset complexity

- **Monitoring**: Results are stored in the `base_dir`:
  - Checkpoints in `base_dir/checkpoints/`
  - Results in `base_dir/results/`
  - Logs in `base_dir/logs/`

- **Custom Models**: Extend `FlexibleModule` or `CNNModule` for custom architectures
