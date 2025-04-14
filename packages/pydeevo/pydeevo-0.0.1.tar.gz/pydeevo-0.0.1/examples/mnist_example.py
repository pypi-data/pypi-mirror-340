"""
Example usage for MNIST classification with PyDeevo
"""
import torch
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
import lightning as L

from pydeevo import PyDeevo
from pydeevo.models.base import FlexibleModule


def main():
    """Main function for MNIST example"""
    # Set up PyDeevo
    pydeevo = PyDeevo(base_dir="./mnist_example")
    
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
    
    # Define input shape and output size for MNIST
    input_shape = 28 * 28  # Flattened MNIST image
    output_size = 10  # 10 classes
    
    print("Starting architecture search...")
    
    # Evolve architecture
    result = pydeevo.evolve_architecture(
        input_shape=input_shape,
        output_size=output_size,
        train_loader=train_loader,
        val_loader=val_loader,
        network_type="mlp",
        population_size=5,  # Small population for example
        num_generations=3,  # Few generations for example
        hp_trials_per_arch=2,  # Few trials for example
        max_epochs=5  # Few epochs for example
    )
    
    best_architecture = result["best_architecture"]
    best_hyperparams = result["best_hyperparameters"]
    
    print(f"Best architecture: {best_architecture}")
    print(f"Best hyperparameters: {best_hyperparams}")
    
    # Create a model with the best architecture and hyperparameters
    model = FlexibleModule(
        architecture=best_architecture,
        **best_hyperparams
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
