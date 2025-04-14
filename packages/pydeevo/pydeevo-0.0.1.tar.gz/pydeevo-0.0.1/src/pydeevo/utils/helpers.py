"""
Utility functions and helpers
"""
import os
import json
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

import torch
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def setup_logging(
    log_dir: str = "logs",
    log_level: int = logging.INFO,
    console_level: int = logging.INFO,
    filename: str = "pydeevo.log"
) -> logging.Logger:
    """
    Set up logging configuration
    
    Args:
        log_dir (str, optional): Directory for log files. Defaults to "logs".
        log_level (int, optional): File log level. Defaults to logging.INFO.
        console_level (int, optional): Console log level. Defaults to logging.INFO.
        filename (str, optional): Log filename. Defaults to "pydeevo.log".
        
    Returns:
        logging.Logger: Logger instance
    """
    # Create directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    # Create file handler
    file_handler = logging.FileHandler(os.path.join(log_dir, filename))
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to root logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_device():
    """
    Get the most powerful available device (CUDA, MPS, or CPU)
    
    Returns:
        torch.device: Device to use
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")


def save_dict_to_json(data: Dict, filename: str):
    """
    Save dictionary to JSON file
    
    Args:
        data (Dict): Data to save
        filename (str): Output filename
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else str(x))


def load_dict_from_json(filename: str) -> Dict:
    """
    Load dictionary from JSON file
    
    Args:
        filename (str): JSON filename
        
    Returns:
        Dict: Loaded data
    """
    with open(filename, 'r') as f:
        return json.load(f)


def plot_search_progress(history: List[Dict], output_file: str):
    """
    Plot optimization progress
    
    Args:
        history (List[Dict]): List of optimization steps
        output_file (str): Output filename
    """
    # Extract data
    iterations = [i for i in range(len(history))]
    fitness_values = [step['fitness'] for step in history]
    
    # Create figure
    fig = plt.figure(figsize=(10, 6))
    
    # Plot fitness progress
    plt.plot(iterations, fitness_values, 'b-', marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.title('Optimization Progress')
    plt.grid(True)
    
    # Save figure
    plt.savefig(output_file)
    plt.close()


def visualize_architecture_comparison(
    architectures: List[Any], 
    fitness_values: List[float], 
    output_file: str
):
    """
    Visualize architecture comparison
    
    Args:
        architectures (List[Any]): List of architectures
        fitness_values (List[float]): List of fitness values
        output_file (str): Output filename
    """
    # Sort by fitness
    sorted_indices = np.argsort(fitness_values)[::-1]  # Descending order
    sorted_architectures = [architectures[i] for i in sorted_indices]
    sorted_fitness = [fitness_values[i] for i in sorted_indices]
    
    # Limit to top 5
    n = min(5, len(sorted_architectures))
    top_architectures = sorted_architectures[:n]
    top_fitness = sorted_fitness[:n]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # For MLP architectures
    if isinstance(top_architectures[0], list):
        # Plot comparison
        x = np.arange(n)
        width = 0.5
        
        ax.bar(x, top_fitness, width, label='Fitness')
        
        # Add text labels
        for i, (arch, fitness) in enumerate(zip(top_architectures, top_fitness)):
            arch_str = ' → '.join(str(layer) for layer in arch)
            ax.text(i, fitness/2, arch_str, ha='center', va='center', rotation=90, color='white')
            ax.text(i, fitness + 0.01, f"{fitness:.4f}", ha='center', va='bottom')
        
        ax.set_xlabel('Architecture Rank')
        ax.set_ylabel('Fitness')
        ax.set_title('Top Neural Network Architectures')
        ax.set_xticks(x)
        ax.set_xticklabels([f"#{i+1}" for i in range(n)])
    
    # For CNN architectures
    elif isinstance(top_architectures[0], tuple) and len(top_architectures[0]) == 2:
        # Plot comparison
        x = np.arange(n)
        width = 0.5
        
        ax.bar(x, top_fitness, width, label='Fitness')
        
        # Add text labels
        for i, (arch, fitness) in enumerate(zip(top_architectures, top_fitness)):
            conv_layers, fc_layers = arch
            
            # Simplified architecture representation
            conv_str = '+'.join(f"{layer.get('filters')}c{layer.get('kernel_size')}" 
                               for layer in conv_layers)
            fc_str = '+'.join(str(neurons) for neurons in fc_layers)
            arch_str = f"{conv_str} → {fc_str}"
            
            ax.text(i, fitness/2, arch_str, ha='center', va='center', rotation=90, color='white')
            ax.text(i, fitness + 0.01, f"{fitness:.4f}", ha='center', va='bottom')
        
        ax.set_xlabel('Architecture Rank')
        ax.set_ylabel('Fitness')
        ax.set_title('Top CNN Architectures')
        ax.set_xticks(x)
        ax.set_xticklabels([f"#{i+1}" for i in range(n)])
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def calculate_model_complexity(model):
    """
    Calculate model complexity (number of parameters and FLOPs)
    
    Args:
        model: PyTorch model
        
    Returns:
        Dict: Complexity metrics
    """
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return {
        'total_parameters': total_params,
        'trainable_parameters': trainable_params,
    }
