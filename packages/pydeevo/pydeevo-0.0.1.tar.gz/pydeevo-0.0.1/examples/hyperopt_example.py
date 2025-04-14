"""
Example of hyperparameter optimization with PyDeevo using a fixed architecture
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
import lightning as L
import optuna

from pydeevo import PyDeevo
from pydeevo.models.base import FlexibleModule


def main():
    """Main function for hyperparameter optimization example"""
    # Set up PyDeevo
    pydeevo = PyDeevo(base_dir="./hyperopt_example")
    
    # Load MNIST dataset
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_dataset = torchvision.datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.MNIST('./data', train=False, transform=transform)
    
    # Split training dataset into train and validation
    train_size = int(0.8 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(train_dataset, [train_size, val_size])
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64)
    test_loader = DataLoader(test_dataset, batch_size=64)
    
    # Fixed architecture for MNIST
    architecture = [784, 256, 128, 10]
    
    # Define model class and fixed arguments
    model_kwargs = {
        'architecture': architecture,
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
    
    print("Starting hyperparameter optimization...")
    
    # Optimize hyperparameters
    best_params = pydeevo.optimize_hyperparameters(
        model_class=FlexibleModule,
        model_kwargs=model_kwargs,
        train_loader=train_loader,
        val_loader=val_loader,
        param_spaces=param_spaces,
        metric_name="val_loss",
        direction="minimize",
        n_trials=20,
        max_epochs=10
    )
    
    print(f"Best hyperparameters: {best_params}")
    
    # Create a model with the fixed architecture and best hyperparameters
    model = FlexibleModule(
        architecture=architecture,
        **best_params
    )
    
    print("Training final model...")
    
    # Train the model
    trainer, metrics = pydeevo.train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        test_loader=test_loader,
        max_epochs=20
    )
    
    print(f"Test metrics: {metrics}")


if __name__ == "__main__":
    main()
