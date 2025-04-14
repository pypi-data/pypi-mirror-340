"""
Evolutionary architecture search using PyGAD
"""
import logging
import numpy as np
from typing import List, Dict, Any, Callable, Optional, Union, Tuple

import pygad
import torch
from torch.utils.data import DataLoader

from ..optimization.optuna_optimizer import OptunaOptimizer

logger = logging.getLogger(__name__)


class ArchitectureEncoding:
    """
    Base class for encoding and decoding neural network architectures
    
    This abstract class defines the interface for architecture encoding and decoding.
    Subclasses should implement encode() and decode() methods.
    """
    
    def encode(self, architecture: Any) -> np.ndarray:
        """
        Encode architecture into a genetic representation
        
        Args:
            architecture: Architecture to encode
            
        Returns:
            np.ndarray: Genetic representation
        """
        raise NotImplementedError("Subclasses must implement encode()")
    
    def decode(self, genes: np.ndarray) -> Any:
        """
        Decode genetic representation into an architecture
        
        Args:
            genes (np.ndarray): Genetic representation
            
        Returns:
            Any: Decoded architecture
        """
        raise NotImplementedError("Subclasses must implement decode()")


class MLPArchitectureEncoding(ArchitectureEncoding):
    """
    Encoding for multilayer perceptron architectures
    
    This class encodes and decodes MLP architectures using binary representation.
    
    Args:
        input_size (int): Input size
        output_size (int): Output size
        max_layers (int, optional): Maximum number of hidden layers. Defaults to 5.
        min_neurons (int, optional): Minimum neurons per layer. Defaults to 16.
        max_neurons (int, optional): Maximum neurons per layer. Defaults to 512.
        bits_per_layer (int, optional): Bits used to encode each layer. Defaults to 8.
    """
    
    def __init__(
        self,
        input_size: int,
        output_size: int,
        max_layers: int = 5,
        min_neurons: int = 16,
        max_neurons: int = 512,
        bits_per_layer: int = 8
    ):
        self.input_size = input_size
        self.output_size = output_size
        self.max_layers = max_layers
        self.min_neurons = min_neurons
        self.max_neurons = max_neurons
        self.bits_per_layer = bits_per_layer
        
        # Total number of genes
        self.num_genes = max_layers * bits_per_layer
    
    def encode(self, architecture: List[int]) -> np.ndarray:
        """
        Encode architecture into a genetic representation
        
        Args:
            architecture (List[int]): List of layer sizes
            
        Returns:
            np.ndarray: Binary encoded architecture
        """
        # Remove input and output layer from the encoding
        hidden_layers = architecture[1:-1]
        
        # Initialize genes
        genes = np.zeros(self.num_genes, dtype=int)
        
        # Encode each hidden layer
        for i, neurons in enumerate(hidden_layers):
            if i >= self.max_layers:
                break
                
            # Scale neurons to 0-255 range
            scaled = int((neurons - self.min_neurons) / 
                         (self.max_neurons - self.min_neurons) * (2**self.bits_per_layer - 1))
            
            # Convert to binary
            binary = [(scaled >> bit) & 1 for bit in range(self.bits_per_layer)]
            
            # Set genes
            start_idx = i * self.bits_per_layer
            genes[start_idx:start_idx + self.bits_per_layer] = binary
        
        return genes
    
    def decode(self, genes: np.ndarray) -> List[int]:
        """
        Decode genetic representation into an architecture
        
        Args:
            genes (np.ndarray): Binary encoded architecture
            
        Returns:
            List[int]: Layer sizes including input and output
        """
        architecture = [self.input_size]
        
        # Decode each hidden layer
        for i in range(self.max_layers):
            start_idx = i * self.bits_per_layer
            binary = genes[start_idx:start_idx + self.bits_per_layer]
            
            # Convert binary to decimal
            decimal = sum(bit * (2**idx) for idx, bit in enumerate(binary))
            
            # Scale to neuron range
            neurons = int(self.min_neurons + (decimal / (2**self.bits_per_layer - 1)) * 
                          (self.max_neurons - self.min_neurons))
            
            # Skip layers with too few neurons (allows variable depth networks)
            if neurons >= self.min_neurons:
                architecture.append(neurons)
        
        architecture.append(self.output_size)
        return architecture


class CNNArchitectureEncoding(ArchitectureEncoding):
    """
    Encoding for convolutional neural network architectures
    
    This class encodes and decodes CNN architectures using binary representation.
    
    Args:
        input_shape (Tuple[int, int, int]): Input shape (channels, height, width)
        output_size (int): Output size
        max_conv_layers (int, optional): Maximum number of conv layers. Defaults to 5.
        max_fc_layers (int, optional): Maximum number of fully connected layers. Defaults to 3.
        min_filters (int, optional): Minimum filters per layer. Defaults to 8.
        max_filters (int, optional): Maximum filters per layer. Defaults to 256.
        min_fc_neurons (int, optional): Minimum neurons per FC layer. Defaults to 16.
        max_fc_neurons (int, optional): Maximum neurons per FC layer. Defaults to 1024.
        bits_per_conv_layer (int, optional): Bits for conv layer. Defaults to 12.
        bits_per_fc_layer (int, optional): Bits for FC layer. Defaults to 8.
    """
    
    def __init__(
        self,
        input_shape: Tuple[int, int, int],
        output_size: int,
        max_conv_layers: int = 5,
        max_fc_layers: int = 3,
        min_filters: int = 8,
        max_filters: int = 256,
        min_fc_neurons: int = 16,
        max_fc_neurons: int = 1024,
        bits_per_conv_layer: int = 12,
        bits_per_fc_layer: int = 8
    ):
        self.input_shape = input_shape
        self.output_size = output_size
        self.max_conv_layers = max_conv_layers
        self.max_fc_layers = max_fc_layers
        self.min_filters = min_filters
        self.max_filters = max_filters
        self.min_fc_neurons = min_fc_neurons
        self.max_fc_neurons = max_fc_neurons
        self.bits_per_conv_layer = bits_per_conv_layer
        self.bits_per_fc_layer = bits_per_fc_layer
        
        # Bit allocation for each conv layer:
        # - 8 bits for filter count
        # - 2 bits for kernel size (options: 3, 5, 7, 9)
        # - 1 bit for pooling (yes/no)
        # - 1 bit for layer activation (yes/no)
        
        # Total number of genes
        self.num_genes = (max_conv_layers * bits_per_conv_layer + 
                         max_fc_layers * bits_per_fc_layer)
    
    def decode(self, genes: np.ndarray) -> Tuple[List[Dict[str, Any]], List[int]]:
        """
        Decode genetic representation into a CNN architecture
        
        Args:
            genes (np.ndarray): Binary encoded architecture
            
        Returns:
            Tuple[List[Dict], List[int]]: Convolutional layers and FC layer sizes
        """
        # Decode convolutional layers
        conv_layers = []
        channels, height, width = self.input_shape
        
        for i in range(self.max_conv_layers):
            start_idx = i * self.bits_per_conv_layer
            layer_genes = genes[start_idx:start_idx + self.bits_per_conv_layer]
            
            # Extract filter count (8 bits)
            filter_bits = layer_genes[:8]
            filter_decimal = sum(bit * (2**idx) for idx, bit in enumerate(filter_bits))
            filters = int(self.min_filters + (filter_decimal / (2**8 - 1)) * 
                         (self.max_filters - self.min_filters))
            
            # Skip if too few filters (allows variable depth)
            if filters < self.min_filters:
                continue
            
            # Extract kernel size (2 bits)
            kernel_bits = layer_genes[8:10]
            kernel_decimal = sum(bit * (2**idx) for idx, bit in enumerate(kernel_bits))
            kernel_options = [3, 5, 7, 9]
            kernel_size = kernel_options[kernel_decimal % len(kernel_options)]
            
            # Extract pooling (1 bit)
            pool_bit = layer_genes[10]
            pool_size = 2 if pool_bit else 1
            
            # Create layer config
            layer = {
                'filters': filters,
                'kernel_size': kernel_size,
                'pool_size': pool_size,
                'padding': kernel_size // 2  # Same padding
            }
            
            # Add to layers
            conv_layers.append(layer)
            
            # Update dimensions for next layer
            height = height // pool_size
            width = width // pool_size
            channels = filters
            
            # Break if dimensions become too small
            if height < 2 or width < 2:
                break
        
        # Decode fully connected layers
        fc_layers = []
        start_idx = self.max_conv_layers * self.bits_per_conv_layer
        
        for i in range(self.max_fc_layers):
            layer_start = start_idx + i * self.bits_per_fc_layer
            layer_genes = genes[layer_start:layer_start + self.bits_per_fc_layer]
            
            # Convert binary to decimal
            decimal = sum(bit * (2**idx) for idx, bit in enumerate(layer_genes))
            
            # Scale to neuron range
            neurons = int(self.min_fc_neurons + (decimal / (2**self.bits_per_fc_layer - 1)) * 
                         (self.max_fc_neurons - self.min_fc_neurons))
            
            # Skip layers with too few neurons (allows variable depth)
            if neurons >= self.min_fc_neurons:
                fc_layers.append(neurons)
        
        fc_layers.append(self.output_size)
        
        return conv_layers, fc_layers
    
    def encode(self, architecture: Tuple[List[Dict[str, Any]], List[int]]) -> np.ndarray:
        """
        Encode CNN architecture into a genetic representation
        
        Args:
            architecture: Tuple of conv layers and FC layer sizes
            
        Returns:
            np.ndarray: Binary encoded architecture
        """
        conv_layers, fc_layers = architecture
        
        # Initialize genes
        genes = np.zeros(self.num_genes, dtype=int)
        
        # Encode convolutional layers
        for i, layer in enumerate(conv_layers):
            if i >= self.max_conv_layers:
                break
                
            start_idx = i * self.bits_per_conv_layer
            
            # Encode filter count (8 bits)
            filters = layer.get('filters', self.min_filters)
            filter_scaled = int((filters - self.min_filters) / 
                              (self.max_filters - self.min_filters) * (2**8 - 1))
            filter_binary = [(filter_scaled >> bit) & 1 for bit in range(8)]
            genes[start_idx:start_idx + 8] = filter_binary
            
            # Encode kernel size (2 bits)
            kernel_size = layer.get('kernel_size', 3)
            kernel_options = [3, 5, 7, 9]
            kernel_idx = kernel_options.index(kernel_size) if kernel_size in kernel_options else 0
            kernel_binary = [(kernel_idx >> bit) & 1 for bit in range(2)]
            genes[start_idx + 8:start_idx + 10] = kernel_binary
            
            # Encode pooling (1 bit)
            pool_size = layer.get('pool_size', 1)
            genes[start_idx + 10] = 1 if pool_size > 1 else 0
        
        # Encode fully connected layers
        fc_start_idx = self.max_conv_layers * self.bits_per_conv_layer
        
        for i, neurons in enumerate(fc_layers[:-1]):  # Skip output layer
            if i >= self.max_fc_layers:
                break
                
            start_idx = fc_start_idx + i * self.bits_per_fc_layer
            
            # Scale neurons to binary range
            scaled = int((neurons - self.min_fc_neurons) / 
                         (self.max_fc_neurons - self.min_fc_neurons) * (2**self.bits_per_fc_layer - 1))
            
            # Convert to binary
            binary = [(scaled >> bit) & 1 for bit in range(self.bits_per_fc_layer)]
            
            # Set genes
            genes[start_idx:start_idx + self.bits_per_fc_layer] = binary
        
        return genes


class EvolutionarySearch:
    """
    Evolutionary architecture search using PyGAD
    
    This class performs evolutionary search for neural network architectures
    using genetic algorithms.
    
    Args:
        encoding (ArchitectureEncoding): Architecture encoding/decoding
        fitness_function (Callable): Function to evaluate architecture fitness
        population_size (int, optional): Size of population. Defaults to 20.
        num_generations (int, optional): Number of generations. Defaults to 20.
        crossover_prob (float, optional): Crossover probability. Defaults to 0.7.
        mutation_prob (float, optional): Mutation probability. Defaults to 0.3.
        parent_selection (str, optional): Parent selection method. Defaults to "sss".
        K_tournament (int, optional): Tournament size if using tournament selection. Defaults to 3.
    """
    
    def __init__(
        self,
        encoding: ArchitectureEncoding,
        fitness_function: Callable[[Any], float],
        population_size: int = 20,
        num_generations: int = 20,
        crossover_prob: float = 0.7,
        mutation_prob: float = 0.3,
        parent_selection: str = "sss",
        K_tournament: int = 3
    ):
        self.encoding = encoding
        self.fitness_function = fitness_function
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.parent_selection = parent_selection
        self.K_tournament = K_tournament
        
        self.ga_instance = None
        self.best_solution = None
        self.best_fitness = None
    
    def _fitness_wrapper(self, solution, solution_idx):
        """
        Wrapper for the fitness function
        
        Args:
            solution: Genetic representation
            solution_idx: Index in population
            
        Returns:
            float: Fitness value
        """
        # Decode the solution
        architecture = self.encoding.decode(solution)
        
        try:
            # Evaluate the architecture
            fitness = self.fitness_function(architecture)
            return fitness
        except Exception as e:
            logger.error(f"Error evaluating architecture: {e}")
            return -1e9  # Very low fitness for failed architectures
    
    def evolve(self, initial_population=None):
        """
        Run the evolutionary search
        
        Args:
            initial_population: Optional initial population
            
        Returns:
            Tuple: Best architecture, best fitness
        """
        # Initialize GA instance
        self.ga_instance = pygad.GA(
            num_generations=self.num_generations,
            num_parents_mating=max(2, self.population_size // 5),
            sol_per_pop=self.population_size,
            num_genes=self.encoding.num_genes,
            fitness_func=self._fitness_wrapper,
            gene_type=int,
            gene_space=[0, 1],  # Binary genes
            crossover_probability=self.crossover_prob,
            mutation_probability=self.mutation_prob,
            parent_selection_type=self.parent_selection,
            K_tournament=self.K_tournament,
            initial_population=initial_population,
            save_best_solutions=True,
            stop_criteria=["reach_0.9999", "saturate_10"]
        )
        
        # Run GA
        self.ga_instance.run()
        
        # Get best solution
        solution, fitness, _ = self.ga_instance.best_solution()
        
        # Decode best architecture
        best_architecture = self.encoding.decode(solution)
        
        self.best_solution = solution
        self.best_fitness = fitness
        
        logger.info(f"Best fitness: {fitness}")
        logger.info(f"Best architecture: {best_architecture}")
        
        return best_architecture, fitness
    
    def get_solution_summary(self):
        """
        Get summary of the search
        
        Returns:
            Dict: Summary information
        """
        if self.ga_instance is None:
            raise ValueError("No search has been performed yet. Call evolve() first.")
        
        return {
            "best_solution": self.best_solution.tolist() if self.best_solution is not None else None,
            "best_fitness": self.best_fitness,
            "best_architecture": self.encoding.decode(self.best_solution) if self.best_solution is not None else None,
            "num_generations": self.ga_instance.generations_completed,
            "fitness_history": [gen.mean() for gen in self.ga_instance.best_solutions_fitness]
        }


class MultilevelOptimization:
    """
    Multi-level optimization combining evolutionary search and hyperparameter optimization
    
    This class integrates PyGAD for architecture search and Optuna for hyperparameter
    optimization in a multi-level approach.
    
    Args:
        model_class (type): Lightning model class
        encoding (ArchitectureEncoding): Architecture encoding/decoding
        train_loader (DataLoader): Training data loader
        val_loader (DataLoader): Validation data loader
        test_loader (Optional[DataLoader], optional): Test data loader. Defaults to None.
        metric_name (str, optional): Metric to optimize. Defaults to "val_acc".
        direction (str, optional): Optimization direction. Defaults to "maximize".
        fixed_model_kwargs (Dict[str, Any], optional): Fixed model parameters. Defaults to {}.
        hp_param_generators (Dict[str, Callable], optional): Hyperparameter generators. Defaults to {}.
        population_size (int, optional): GA population size. Defaults to 10.
        num_generations (int, optional): GA generations. Defaults to 10.
        n_trials (int, optional): Optuna trials per architecture. Defaults to 5.
        max_epochs (int, optional): Max training epochs. Defaults to 10.
    """
    
    def __init__(
        self,
        model_class: type,
        encoding: ArchitectureEncoding,
        train_loader: DataLoader,
        val_loader: DataLoader,
        test_loader: Optional[DataLoader] = None,
        metric_name: str = "val_acc",
        direction: str = "maximize",
        fixed_model_kwargs: Dict[str, Any] = None,
        hp_param_generators: Dict[str, Callable] = None,
        population_size: int = 10,
        num_generations: int = 10,
        n_trials: int = 5,
        max_epochs: int = 10
    ):
        self.model_class = model_class
        self.encoding = encoding
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.metric_name = metric_name
        self.direction = direction
        self.fixed_model_kwargs = fixed_model_kwargs or {}
        self.hp_param_generators = hp_param_generators or {}
        self.population_size = population_size
        self.num_generations = num_generations
        self.n_trials = n_trials
        self.max_epochs = max_epochs
        
        # Results tracking
        self.best_architecture = None
        self.best_hyperparams = None
        self.best_fitness = None if direction == "maximize" else float('inf')
        self.architecture_fitness_history = []
    
    def optimize_hyperparams(self, architecture):
        """
        Optimize hyperparameters for a given architecture
        
        Args:
            architecture: Neural network architecture
            
        Returns:
            Tuple[Dict[str, Any], float]: Best hyperparameters and fitness
        """
        # For MLPArchitectureEncoding
        if isinstance(architecture, list):
            model_kwargs = {
                **self.fixed_model_kwargs,
                'architecture': architecture
            }
        # For CNNArchitectureEncoding
        elif isinstance(architecture, tuple) and len(architecture) == 2:
            conv_architecture, fc_architecture = architecture
            model_kwargs = {
                **self.fixed_model_kwargs,
                'conv_architecture': conv_architecture,
                'fc_architecture': fc_architecture
            }
        else:
            raise ValueError(f"Unsupported architecture format: {type(architecture)}")
        
        # Create optimizer
        optimizer = OptunaOptimizer(
            model_class=self.model_class,
            model_kwargs=model_kwargs,
            train_loader=self.train_loader,
            val_loader=self.val_loader,
            metric_name=self.metric_name,
            direction=self.direction,
            max_epochs=self.max_epochs,
            n_trials=self.n_trials
        )
        
        # Add hyperparameter spaces
        for param_name, generator in self.hp_param_generators.items():
            optimizer.add_param_space(param_name, generator)
        
        # If no hyperparameters were added, add a default learning rate
        if not self.hp_param_generators:
            optimizer.add_float_param('learning_rate', 1e-4, 1e-1, log=True)
        
        # Optimize
        best_params = optimizer.optimize()
        
        # Get best value
        study = optimizer.study
        best_value = study.best_value
        if self.direction == 'maximize':
            best_value = -best_value  # Negate if maximizing
        
        return best_params, best_value
    
    def fitness_function(self, architecture):
        """
        Fitness function for evolutionary search
        
        Args:
            architecture: Neural network architecture
            
        Returns:
            float: Fitness value (higher is better)
        """
        logger.info(f"Evaluating architecture: {architecture}")
        
        try:
            # Optimize hyperparameters for this architecture
            best_params, best_fitness = self.optimize_hyperparams(architecture)
            
            # For minimization, invert the fitness
            fitness = best_fitness if self.direction == "maximize" else -best_fitness
            
            # Track architecture and fitness
            self.architecture_fitness_history.append((architecture, fitness, best_params))
            
            # Update best overall if better
            if self.direction == "maximize":
                if fitness > self.best_fitness:
                    self.best_architecture = architecture
                    self.best_hyperparams = best_params
                    self.best_fitness = fitness
            else:
                if fitness < self.best_fitness:
                    self.best_architecture = architecture
                    self.best_hyperparams = best_params
                    self.best_fitness = fitness
            
            logger.info(f"Architecture fitness: {fitness}")
            return fitness
        
        except Exception as e:
            logger.error(f"Error in fitness evaluation: {e}")
            return -1e9 if self.direction == "maximize" else 1e9
    
    def search(self):
        """
        Perform multi-level optimization
        
        Returns:
            Tuple: Best architecture, best hyperparameters, best model
        """
        # Create evolutionary search
        evolution = EvolutionarySearch(
            encoding=self.encoding,
            fitness_function=self.fitness_function,
            population_size=self.population_size,
            num_generations=self.num_generations
        )
        
        # Run evolutionary search
        evolution.evolve()
        
        # Train final model with best architecture and hyperparameters
        if self.best_architecture is not None and self.best_hyperparams is not None:
            # For MLPArchitectureEncoding
            if isinstance(self.best_architecture, list):
                model_kwargs = {
                    **self.fixed_model_kwargs,
                    **self.best_hyperparams,
                    'architecture': self.best_architecture
                }
            # For CNNArchitectureEncoding
            elif isinstance(self.best_architecture, tuple) and len(self.best_architecture) == 2:
                conv_architecture, fc_architecture = self.best_architecture
                model_kwargs = {
                    **self.fixed_model_kwargs,
                    **self.best_hyperparams,
                    'conv_architecture': conv_architecture,
                    'fc_architecture': fc_architecture
                }
            
            # Create and train model
            best_model = self.model_class(**model_kwargs)
            
            trainer = L.Trainer(max_epochs=self.max_epochs * 2)
            trainer.fit(best_model, self.train_loader, self.val_loader)
            
            # Test if test loader provided
            if self.test_loader:
                trainer.test(best_model, self.test_loader)
            
            return self.best_architecture, self.best_hyperparams, best_model
        
        return None, None, None
    
    def get_search_summary(self):
        """
        Get summary of the search
        
        Returns:
            Dict: Summary information
        """
        return {
            "best_architecture": self.best_architecture,
            "best_hyperparams": self.best_hyperparams,
            "best_fitness": self.best_fitness,
            "architecture_history": self.architecture_fitness_history
        }
