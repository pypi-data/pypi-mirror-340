"""
Hyperparameter optimization using Optuna
"""
import os
import logging
from typing import Callable, Dict, Any, List, Optional, Tuple, Union

import optuna
from optuna.integration import PyTorchLightningPruningCallback
import lightning as L
from lightning.pytorch.callbacks import EarlyStopping, ModelCheckpoint
import torch
from torch.utils.data import DataLoader

logger = logging.getLogger(__name__)


class OptunaOptimizer:
    """
    Hyperparameter optimizer using Optuna
    
    This class provides an interface for hyperparameter optimization using Optuna
    with PyTorch Lightning models.
    
    Args:
        model_class (type): Lightning model class to optimize
        model_kwargs (Dict[str, Any]): Fixed arguments for model initialization
        train_loader (DataLoader): Training data loader
        val_loader (DataLoader): Validation data loader
        metric_name (str): Name of the metric to optimize
        direction (str): Direction of optimization ('minimize' or 'maximize')
        max_epochs (int, optional): Maximum number of training epochs. Defaults to 10.
        patience (int, optional): Early stopping patience. Defaults to 3.
        n_trials (int, optional): Number of optimization trials. Defaults to 20.
        timeout (Optional[int], optional): Timeout in seconds. Defaults to None.
        study_name (Optional[str], optional): Name of the study. Defaults to None.
        storage (Optional[str], optional): Storage URL for the study. Defaults to None.
    """
    
    def __init__(
        self,
        model_class: type,
        model_kwargs: Dict[str, Any],
        train_loader: DataLoader,
        val_loader: DataLoader,
        metric_name: str = 'val_loss',
        direction: str = 'minimize',
        max_epochs: int = 10,
        patience: int = 3,
        n_trials: int = 20,
        timeout: Optional[int] = None,
        study_name: Optional[str] = None,
        storage: Optional[str] = None,
    ):
        self.model_class = model_class
        self.model_kwargs = model_kwargs
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.metric_name = metric_name
        self.direction = direction
        self.max_epochs = max_epochs
        self.patience = patience
        self.n_trials = n_trials
        self.timeout = timeout
        self.study_name = study_name
        self.storage = storage
        
        # Initialize study
        self.study = None
        self.param_generators = {}
        self.param_spaces = {}
    
    def add_param_space(self, param_name: str, generator: Callable[[optuna.trial.Trial], Any]) -> None:
        """
        Add a parameter space for optimization
        
        Args:
            param_name (str): Name of the parameter
            generator (Callable): Function that generates parameter values from a trial
        """
        self.param_generators[param_name] = generator
    
    def add_categorical_param(self, param_name: str, choices: List[Any]) -> None:
        """
        Add a categorical parameter space
        
        Args:
            param_name (str): Name of the parameter
            choices (List[Any]): List of possible values
        """
        self.add_param_space(
            param_name, 
            lambda trial: trial.suggest_categorical(param_name, choices)
        )
    
    def add_float_param(
        self, 
        param_name: str, 
        low: float, 
        high: float, 
        log: bool = False, 
        step: Optional[float] = None
    ) -> None:
        """
        Add a float parameter space
        
        Args:
            param_name (str): Name of the parameter
            low (float): Lower bound
            high (float): Upper bound
            log (bool, optional): Use log scale. Defaults to False.
            step (Optional[float], optional): Step size. Defaults to None.
        """
        if step:
            self.add_param_space(
                param_name,
                lambda trial: trial.suggest_float(param_name, low, high, step=step)
            )
        else:
            self.add_param_space(
                param_name,
                lambda trial: trial.suggest_float(param_name, low, high, log=log)
            )
    
    def add_int_param(
        self, 
        param_name: str, 
        low: int, 
        high: int, 
        log: bool = False, 
        step: int = 1
    ) -> None:
        """
        Add an integer parameter space
        
        Args:
            param_name (str): Name of the parameter
            low (int): Lower bound
            high (int): Upper bound
            log (bool, optional): Use log scale. Defaults to False.
            step (int, optional): Step size. Defaults to 1.
        """
        self.add_param_space(
            param_name,
            lambda trial: trial.suggest_int(param_name, low, high, log=log, step=step)
        )
    
    def objective(self, trial: optuna.trial.Trial) -> float:
        """
        Objective function for optimization
        
        Args:
            trial (optuna.trial.Trial): Optuna trial
            
        Returns:
            float: Value of the objective function
        """
        # Generate hyperparameters from param spaces
        params = {}
        for param_name, generator in self.param_generators.items():
            params[param_name] = generator(trial)
        
        # Combine with fixed model kwargs
        model_kwargs = {**self.model_kwargs, **params}
        
        # Create model with these hyperparameters
        model = self.model_class(**model_kwargs)
        
        # Callbacks
        early_stop = EarlyStopping(
            monitor=self.metric_name,
            patience=self.patience,
            mode='min' if self.direction == 'minimize' else 'max'
        )
        
        pruning_callback = PyTorchLightningPruningCallback(
            trial, 
            monitor=self.metric_name
        )
        
        # Trainer
        trainer = L.Trainer(
            max_epochs=self.max_epochs,
            callbacks=[early_stop, pruning_callback],
            enable_model_summary=False,
            enable_progress_bar=False,
            logger=False
        )
        
        # Train model
        trainer.fit(model, self.train_loader, self.val_loader)
        
        # Get metric value
        metric_value = trainer.callback_metrics[self.metric_name].item()
        
        # For minimization, return as is; for maximization, return negative
        return metric_value if self.direction == 'minimize' else -metric_value
    
    def optimize(self) -> Dict[str, Any]:
        """
        Run the optimization process
        
        Returns:
            Dict[str, Any]: Best hyperparameters
        """
        # Create Optuna study
        self.study = optuna.create_study(
            direction='minimize',  # Always minimize (we negate for maximization)
            study_name=self.study_name,
            storage=self.storage,
            load_if_exists=True if (self.study_name and self.storage) else False
        )
        
        # Run optimization
        self.study.optimize(
            self.objective, 
            n_trials=self.n_trials,
            timeout=self.timeout
        )
        
        # Get best parameters
        best_params = self.study.best_params
        
        # For maximization, we need to negate the best value
        best_value = self.study.best_value
        if self.direction == 'maximize':
            best_value = -best_value
        
        logger.info(f"Best {self.metric_name}: {best_value:.4f}")
        logger.info(f"Best parameters: {best_params}")
        
        return best_params
    
    def train_with_best_params(
        self, 
        test_loader: Optional[DataLoader] = None,
        checkpoint_dir: Optional[str] = None
    ) -> Tuple[L.LightningModule, Dict[str, float]]:
        """
        Train a model with the best hyperparameters
        
        Args:
            test_loader (Optional[DataLoader], optional): Test data loader. Defaults to None.
            checkpoint_dir (Optional[str], optional): Directory to save checkpoints. Defaults to None.
            
        Returns:
            Tuple[L.LightningModule, Dict[str, float]]: Trained model and metrics
        """
        if self.study is None:
            raise ValueError("No optimization has been performed yet. Call optimize() first.")
        
        # Combine best params with fixed model kwargs
        model_kwargs = {**self.model_kwargs, **self.study.best_params}
        
        # Create model with best hyperparameters
        model = self.model_class(**model_kwargs)
        
        # Callbacks
        callbacks = []
        
        if checkpoint_dir:
            os.makedirs(checkpoint_dir, exist_ok=True)
            checkpoint_callback = ModelCheckpoint(
                dirpath=checkpoint_dir,
                filename='best-{epoch:02d}-{' + self.metric_name + ':.4f}',
                monitor=self.metric_name,
                mode='min' if self.direction == 'minimize' else 'max',
                save_top_k=1
            )
            callbacks.append(checkpoint_callback)
        
        # Trainer
        trainer = L.Trainer(
            max_epochs=self.max_epochs * 2,  # Train longer for final model
            callbacks=callbacks
        )
        
        # Train model
        trainer.fit(model, self.train_loader, self.val_loader)
        
        # Test if test loader provided
        metrics = {}
        if test_loader:
            test_results = trainer.test(model, test_loader)
            metrics.update(test_results[0])
        
        # Add validation metrics
        for name, value in trainer.callback_metrics.items():
            if isinstance(value, torch.Tensor):
                metrics[name] = value.item()
        
        return model, metrics
