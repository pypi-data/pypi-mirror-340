"""
Main integration module for PyDeevo
"""
import os
import logging
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

import torch
from torch.utils.data import DataLoader
import optuna
import lightning as L

from ..models.base import FlexibleModule, CNNModule
from ..optimization.optuna_optimizer import OptunaOptimizer
from ..evolution.architecture_search import (
    MLPArchitectureEncoding,
    CNNArchitectureEncoding,
    EvolutionarySearch,
    MultilevelOptimization
)
from ..training.trainer import LightningTrainer, DataModule
from ..utils.helpers import setup_logging, save_dict_to_json, visualize_architecture_comparison

logger = logging.getLogger(__name__)


class PyDeevo:
    """
    Main class integrating all PyDeevo components
    
    This class provides a high-level interface to the PyDeevo framework,
    combining PyTorch Lightning, Optuna, and PyGAD.
    
    Args:
        base_dir (str, optional): Base directory for outputs. Defaults to "./pydeevo_output".
        log_level (int, optional): Logging level. Defaults to logging.INFO.
    """
    
    def __init__(
        self,
        base_dir: str = "./pydeevo_output",
        log_level: int = logging.INFO
    ):
        self.base_dir = base_dir
        
        # Create directories
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "checkpoints"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "results"), exist_ok=True)
        
        # Setup logging
        self.logger = setup_logging(
            log_dir=os.path.join(base_dir, "logs"),
            log_level=log_level
        )
    
    def optimize_hyperparameters(
        self,
        model_class: type,
        model_kwargs: Dict[str, Any],
        train_loader: DataLoader,
        val_loader: DataLoader,
        param_spaces: Dict[str, Callable],
        metric_name: str = "val_loss",
        direction: str = "minimize",
        n_trials: int = 20,
        max_epochs: int = 10
    ) -> Dict[str, Any]:
        """
        Optimize hyperparameters using Optuna
        
        Args:
            model_class (type): Lightning model class
            model_kwargs (Dict[str, Any]): Model initialization arguments
            train_loader (DataLoader): Training data loader
            val_loader (DataLoader): Validation data loader
            param_spaces (Dict[str, Callable]): Parameter space generators
            metric_name (str, optional): Metric to optimize. Defaults to "val_loss".
            direction (str, optional): Optimization direction. Defaults to "minimize".
            n_trials (int, optional): Number of trials. Defaults to 20.
            max_epochs (int, optional): Maximum epochs per trial. Defaults to 10.
            
        Returns:
            Dict[str, Any]: Best hyperparameters
        """
        # Create optimizer
        optimizer = OptunaOptimizer(
            model_class=model_class,
            model_kwargs=model_kwargs,
            train_loader=train_loader,
            val_loader=val_loader,
            metric_name=metric_name,
            direction=direction,
            max_epochs=max_epochs,
            n_trials=n_trials,
            study_name=f"{model_class.__name__}_study",
            storage=f"sqlite:///{os.path.join(self.base_dir, 'optuna.db')}"
        )
        
        # Add parameter spaces
        for param_name, generator in param_spaces.items():
            optimizer.add_param_space(param_name, generator)
        
        # Run optimization
        best_params = optimizer.optimize()
        
        # Save results
        results = {
            "model_class": model_class.__name__,
            "best_params": best_params,
            "best_value": optimizer.study.best_value,
            "n_trials": n_trials
        }
        
        save_dict_to_json(
            results,
            os.path.join(self.base_dir, "results", "hyperparameter_optimization.json")
        )
        
        return best_params
    
    def evolve_architecture(
        self,
        input_shape: Union[int, Tuple[int, int, int]],
        output_size: int,
        train_loader: DataLoader,
        val_loader: DataLoader,
        network_type: str = "mlp",
        population_size: int = 10,
        num_generations: int = 10,
        hp_trials_per_arch: int = 5,
        max_epochs: int = 10,
        metric_name: str = "val_acc",
        direction: str = "maximize",
        fixed_model_kwargs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evolve neural network architecture using genetic algorithms
        
        Args:
            input_shape (Union[int, Tuple[int, int, int]]): Input shape (scalar for MLP, tuple for CNN)
            output_size (int): Output size
            train_loader (DataLoader): Training data loader
            val_loader (DataLoader): Validation data loader
            network_type (str, optional): Network type ("mlp" or "cnn"). Defaults to "mlp".
            population_size (int, optional): Population size. Defaults to 10.
            num_generations (int, optional): Number of generations. Defaults to 10.
            hp_trials_per_arch (int, optional): Hyperparameter trials per architecture. Defaults to 5.
            max_epochs (int, optional): Maximum epochs per trial. Defaults to 10.
            metric_name (str, optional): Metric to optimize. Defaults to "val_acc".
            direction (str, optional): Optimization direction. Defaults to "maximize".
            fixed_model_kwargs (Optional[Dict[str, Any]], optional): Fixed model arguments. Defaults to None.
            
        Returns:
            Dict[str, Any]: Evolution results
        """
        fixed_model_kwargs = fixed_model_kwargs or {}
        
        # Select model class and encoding based on network type
        if network_type.lower() == "mlp":
            model_class = FlexibleModule
            encoding = MLPArchitectureEncoding(
                input_size=input_shape,
                output_size=output_size,
                max_layers=5
            )
        elif network_type.lower() == "cnn":
            model_class = CNNModule
            encoding = CNNArchitectureEncoding(
                input_shape=input_shape,
                output_size=output_size,
                max_conv_layers=5,
                max_fc_layers=3
            )
        else:
            raise ValueError(f"Unknown network type: {network_type}")
        
        # Define hyperparameter spaces
        hp_param_generators = {
            'learning_rate': lambda trial: trial.suggest_float('learning_rate', 1e-4, 1e-1, log=True),
            'optimizer_kwargs': lambda trial: {
                'weight_decay': trial.suggest_float('weight_decay', 1e-6, 1e-3, log=True)
            }
        }
        
        # Create multi-level optimizer
        optimizer = MultilevelOptimization(
            model_class=model_class,
            encoding=encoding,
            train_loader=train_loader,
            val_loader=val_loader,
            metric_name=metric_name,
            direction=direction,
            fixed_model_kwargs=fixed_model_kwargs,
            hp_param_generators=hp_param_generators,
            population_size=population_size,
            num_generations=num_generations,
            n_trials=hp_trials_per_arch,
            max_epochs=max_epochs
        )
        
        # Run search
        best_architecture, best_hyperparams, best_model = optimizer.search()
        
        # Create result summary
        summary = optimizer.get_search_summary()
        
        # Save best architecture and hyperparameters
        save_dict_to_json(
            summary,
            os.path.join(self.base_dir, "results", "architecture_search.json")
        )
        
        # Visualize architecture comparison
        architectures = [arch for arch, _, _ in summary['architecture_history']]
        fitness_values = [fitness for _, fitness, _ in summary['architecture_history']]
        
        visualize_architecture_comparison(
            architectures,
            fitness_values,
            os.path.join(self.base_dir, "results", "architecture_comparison.png")
        )
        
        # Save model checkpoint if available
        if best_model is not None:
            checkpoint_path = os.path.join(self.base_dir, "checkpoints", "best_evolved_model.ckpt")
            trainer = L.Trainer()
            trainer.save_checkpoint(checkpoint_path)
        
        return {
            "best_architecture": best_architecture,
            "best_hyperparameters": best_hyperparams,
            "summary": summary
        }
    
    def train_model(
        self,
        model: L.LightningModule,
        train_loader: DataLoader,
        val_loader: Optional[DataLoader] = None,
        test_loader: Optional[DataLoader] = None,
        max_epochs: int = 100,
        patience: int = 10,
        monitor: str = "val_loss",
        mode: str = "min"
    ) -> Tuple[L.Trainer, Dict[str, float]]:
        """
        Train a Lightning model
        
        Args:
            model (L.LightningModule): Lightning model
            train_loader (DataLoader): Training data loader
            val_loader (Optional[DataLoader], optional): Validation data loader. Defaults to None.
            test_loader (Optional[DataLoader], optional): Test data loader. Defaults to None.
            max_epochs (int, optional): Maximum epochs. Defaults to 100.
            patience (int, optional): Early stopping patience. Defaults to 10.
            monitor (str, optional): Metric to monitor. Defaults to "val_loss".
            mode (str, optional): Optimization mode. Defaults to "min".
            
        Returns:
            Tuple[L.Trainer, Dict[str, float]]: Trainer and metrics
        """
        # Create trainer
        trainer = LightningTrainer(
            max_epochs=max_epochs,
            patience=patience,
            monitor=monitor,
            mode=mode,
            checkpoint_dir=os.path.join(self.base_dir, "checkpoints"),
            log_dir=os.path.join(self.base_dir, "logs")
        )
        
        # Setup trainer
        trainer.setup_trainer()
        
        # Train model
        trainer.fit(model, train_loader, val_loader)
        
        # Test if test loader provided
        metrics = {}
        if test_loader is not None:
            metrics = trainer.test(model, test_loader)
        
        # Save model summary
        trainer.save_model_summary(model)
        
        return trainer, metrics
    
    def load_best_model(
        self, 
        model_class: type, 
        checkpoint_path: Optional[str] = None, 
        **model_kwargs
    ) -> L.LightningModule:
        """
        Load a model from checkpoint
        
        Args:
            model_class (type): Lightning model class
            checkpoint_path (Optional[str], optional): Checkpoint path. Defaults to None.
            **model_kwargs: Model initialization arguments
            
        Returns:
            L.LightningModule: Loaded model
        """
        if checkpoint_path is None:
            # Try to find the latest checkpoint
            checkpoint_dir = os.path.join(self.base_dir, "checkpoints")
            checkpoints = [f for f in os.listdir(checkpoint_dir) if f.endswith(".ckpt")]
            
            if not checkpoints:
                raise ValueError("No checkpoints found.")
            
            # Use the latest checkpoint
            checkpoint_path = os.path.join(checkpoint_dir, sorted(checkpoints)[-1])
        
        # Load model
        model = model_class.load_from_checkpoint(checkpoint_path, **model_kwargs)
        
        return model
