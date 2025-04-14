"""
Base model classes for neural networks with flexible architectures
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as L
from typing import List, Dict, Any, Optional, Union, Callable


class FlexibleModule(L.LightningModule):
    """
    A flexible neural network module that can be initialized with various architectures.
    
    This base class provides a standard implementation for common deep learning tasks
    while allowing for architectural flexibility.
    
    Args:
        architecture (List[int]): List of integers defining the layer sizes
        learning_rate (float, optional): Learning rate for optimization. Defaults to 0.001.
        activation (Callable, optional): Activation function to use between layers. Defaults to nn.ReLU().
        loss_fn (Callable, optional): Loss function. Defaults to F.cross_entropy.
        optimizer_class (type, optional): Optimizer class. Defaults to torch.optim.Adam.
        optimizer_kwargs (Dict[str, Any], optional): Additional optimizer arguments. Defaults to {}.
    """
    def __init__(
        self,
        architecture: List[int],
        learning_rate: float = 0.001,
        activation: Callable = nn.ReLU,
        loss_fn: Callable = F.cross_entropy,
        optimizer_class: type = torch.optim.Adam,
        optimizer_kwargs: Dict[str, Any] = None,
    ):
        super().__init__()
        self.save_hyperparameters(ignore=['architecture', 'activation', 'loss_fn', 'optimizer_class', 'optimizer_kwargs'])
        self.architecture = architecture
        self.learning_rate = learning_rate
        self.loss_fn = loss_fn
        self.optimizer_class = optimizer_class
        self.optimizer_kwargs = optimizer_kwargs or {}
        
        # Build dynamic architecture
        layers = []
        for i in range(len(architecture) - 1):
            layers.append(nn.Linear(architecture[i], architecture[i+1]))
            # No activation after the final layer
            if i < len(architecture) - 2:
                layers.append(activation())
        
        self.model = nn.Sequential(*layers)
    
    def forward(self, x):
        """Forward pass"""
        # Handle different input shapes based on the expected input dimension
        if len(x.shape) > 2 and self.architecture[0] == x.shape[1] * x.shape[2] * x.shape[3]:
            x = x.view(x.size(0), -1)
        return self.model(x)
    
    def training_step(self, batch, batch_idx):
        """Training step"""
        x, y = batch
        # Reshape if needed (e.g., for image data)
        if len(x.shape) > 2 and self.architecture[0] == x.shape[1] * x.shape[2] * x.shape[3]:
            x = x.view(x.size(0), -1)
            
        logits = self(x)
        loss = self.loss_fn(logits, y)
        self.log('train_loss', loss, prog_bar=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        """Validation step"""
        x, y = batch
        # Reshape if needed (e.g., for image data)
        if len(x.shape) > 2 and self.architecture[0] == x.shape[1] * x.shape[2] * x.shape[3]:
            x = x.view(x.size(0), -1)
            
        logits = self(x)
        loss = self.loss_fn(logits, y)
        
        # For classification tasks
        if hasattr(logits, 'argmax'):
            acc = (logits.argmax(dim=1) == y).float().mean()
            self.log('val_acc', acc, prog_bar=True)
        
        self.log('val_loss', loss, prog_bar=True)
        return {'val_loss': loss}
    
    def test_step(self, batch, batch_idx):
        """Test step"""
        x, y = batch
        # Reshape if needed (e.g., for image data)
        if len(x.shape) > 2 and self.architecture[0] == x.shape[1] * x.shape[2] * x.shape[3]:
            x = x.view(x.size(0), -1)
            
        logits = self(x)
        loss = self.loss_fn(logits, y)
        
        # For classification tasks
        if hasattr(logits, 'argmax'):
            acc = (logits.argmax(dim=1) == y).float().mean()
            self.log('test_acc', acc)
        
        self.log('test_loss', loss)
        return {'test_loss': loss}
    
    def configure_optimizers(self):
        """Configure optimizers"""
        return self.optimizer_class(
            self.parameters(),
            lr=self.learning_rate,
            **self.optimizer_kwargs
        )


class CNNModule(FlexibleModule):
    """
    A convolutional neural network with flexible architecture.
    
    This class extends FlexibleModule to handle convolutional architectures.
    
    Args:
        conv_architecture (List[Dict]): List of dicts defining conv layers
        fc_architecture (List[int]): List of integers defining fully connected layer sizes
        input_shape (tuple): Shape of input tensor (channels, height, width)
        learning_rate (float, optional): Learning rate for optimization. Defaults to 0.001.
        activation (Callable, optional): Activation function. Defaults to nn.ReLU.
        loss_fn (Callable, optional): Loss function. Defaults to F.cross_entropy.
        optimizer_class (type, optional): Optimizer class. Defaults to torch.optim.Adam.
        optimizer_kwargs (Dict[str, Any], optional): Additional optimizer arguments. Defaults to {}.
    """
    def __init__(
        self,
        conv_architecture: List[Dict[str, Any]],
        fc_architecture: List[int],
        input_shape: tuple,
        learning_rate: float = 0.001,
        activation: Callable = nn.ReLU,
        loss_fn: Callable = F.cross_entropy,
        optimizer_class: type = torch.optim.Adam,
        optimizer_kwargs: Dict[str, Any] = None,
    ):
        super(FlexibleModule, self).__init__()  # Skip FlexibleModule's __init__
        self.save_hyperparameters(ignore=[
            'conv_architecture', 'fc_architecture', 'activation', 
            'loss_fn', 'optimizer_class', 'optimizer_kwargs'
        ])
        
        self.conv_architecture = conv_architecture
        self.fc_architecture = fc_architecture
        self.input_shape = input_shape
        self.learning_rate = learning_rate
        self.loss_fn = loss_fn
        self.optimizer_class = optimizer_class
        self.optimizer_kwargs = optimizer_kwargs or {}
        
        # Build convolutional layers
        conv_layers = []
        channels, height, width = input_shape
        
        in_channels = channels
        for conv_config in conv_architecture:
            # Extract parameters with defaults
            out_channels = conv_config['filters']
            kernel_size = conv_config.get('kernel_size', 3)
            stride = conv_config.get('stride', 1)
            padding = conv_config.get('padding', 1)
            pool_size = conv_config.get('pool_size', 2)
            
            # Add conv layer
            conv_layers.append(nn.Conv2d(
                in_channels, out_channels, kernel_size, stride, padding
            ))
            conv_layers.append(activation())
            
            # Update dimensions after conv
            height = (height - kernel_size + 2 * padding) // stride + 1
            width = (width - kernel_size + 2 * padding) // stride + 1
            
            # Add pooling if specified
            if pool_size > 1:
                conv_layers.append(nn.MaxPool2d(pool_size))
                height //= pool_size
                width //= pool_size
            
            # Update channels for next layer
            in_channels = out_channels
        
        self.conv_model = nn.Sequential(*conv_layers)
        
        # Calculate flattened size after convolutions
        flattened_size = in_channels * height * width
        
        # Build fully connected layers
        fc_layers = []
        fc_sizes = [flattened_size] + fc_architecture
        
        for i in range(len(fc_sizes) - 1):
            fc_layers.append(nn.Linear(fc_sizes[i], fc_sizes[i+1]))
            # No activation after final layer
            if i < len(fc_sizes) - 2:
                fc_layers.append(activation())
        
        self.fc_model = nn.Sequential(*fc_layers)
    
    def forward(self, x):
        """Forward pass through convolutional and fully connected layers"""
        # Pass through convolutional layers
        x = self.conv_model(x)
        # Flatten
        x = x.view(x.size(0), -1)
        # Pass through fully connected layers
        return self.fc_model(x)
