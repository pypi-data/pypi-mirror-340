"""
Example usage for CIFAR-10 classification with PyDeevo using CNNs
"""
import torch
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
import lightning as L

from pydeevo import PyDeevo
from pydeevo.models.base import CNNModule


def main():
    """Main function for CIFAR-10 example"""
    # Set up PyDeevo
    pydeevo = PyDeevo(base_dir="./cifar10_example")
    
    # Load CIFAR-10 dataset
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    
    train_dataset = torchvision.datasets.CIFAR10('./data', train=True, download=True, transform=transform_train)
    test_dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=transform_test)
    
    # Split training dataset into train and validation
    train_size = int(0.8 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(train_dataset, [train_size, val_size])
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64)
    test_loader = DataLoader(test_dataset, batch_size=64)
    
    # Define input shape and output size for CIFAR-10
    input_shape = (3, 32, 32)  # CIFAR-10 images (channels, height, width)
    output_size = 10  # 10 classes
    
    print("Starting architecture search...")
    
    # Evolve architecture
    result = pydeevo.evolve_architecture(
        input_shape=input_shape,
        output_size=output_size,
        train_loader=train_loader,
        val_loader=val_loader,
        network_type="cnn",
        population_size=5,  # Small population for example
        num_generations=3,  # Few generations for example
        hp_trials_per_arch=2,  # Few trials for example
        max_epochs=5  # Few epochs for example
    )
    
    best_architecture = result["best_architecture"]
    best_hyperparams = result["best_hyperparameters"]
    
    conv_architecture, fc_architecture = best_architecture
    
    print(f"Best convolutional layers: {conv_architecture}")
    print(f"Best fully connected layers: {fc_architecture}")
    print(f"Best hyperparameters: {best_hyperparams}")
    
    # Create a model with the best architecture and hyperparameters
    model = CNNModule(
        conv_architecture=conv_architecture,
        fc_architecture=fc_architecture,
        input_shape=input_shape,
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
