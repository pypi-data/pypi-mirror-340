"""
Training utilities for PyTorch Lightning
"""
import os
import json
from typing import List, Dict, Any, Optional, Union, Tuple, Callable

import lightning as L
from lightning.pytorch.callbacks import (
    EarlyStopping, 
    ModelCheckpoint, 
    LearningRateMonitor
)
from lightning.pytorch.loggers import TensorBoardLogger
import torch
from torch.utils.data import DataLoader, Dataset

from .callbacks import ArchitectureLogger, ArchitectureVisualizer


class LightningTrainer:
    """
    Wrapper for PyTorch Lightning Trainer with additional functionality
    
    Args:
        max_epochs (int, optional): Maximum number of epochs. Defaults to 100.
        patience (int, optional): Early stopping patience. Defaults to 10.
        monitor (str, optional): Metric to monitor. Defaults to "val_loss".
        mode (str, optional): Optimization mode. Defaults to "min".
        accelerator (str, optional): Accelerator type. Defaults to "auto".
        devices (Union[int, str, List[int]], optional): Devices to use. Defaults to "auto".
        checkpoint_dir (Optional[str], optional): Directory for checkpoints. Defaults to None.
        log_dir (Optional[str], optional): Directory for logs. Defaults to None.
    """
    
    def __init__(
        self,
        max_epochs: int = 100,
        patience: int = 10,
        monitor: str = "val_loss",
        mode: str = "min",
        accelerator: str = "auto",
        devices: Union[int, str, List[int]] = "auto",
        checkpoint_dir: Optional[str] = None,
        log_dir: Optional[str] = None
    ):
        self.max_epochs = max_epochs
        self.patience = patience
        self.monitor = monitor
        self.mode = mode
        self.accelerator = accelerator
        self.devices = devices
        self.checkpoint_dir = checkpoint_dir or "./checkpoints"
        self.log_dir = log_dir or "./logs"
        
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.trainer = None
        self.callbacks = []
    
    def setup_trainer(
        self, 
        additional_callbacks: Optional[List[Callable]] = None,
        logger: bool = True,
        enable_progress_bar: bool = True,
        **trainer_kwargs
    ) -> L.Trainer:
        """
        Set up the Lightning Trainer
        
        Args:
            additional_callbacks (Optional[List[Callable]], optional): Additional callbacks. Defaults to None.
            logger (bool, optional): Whether to use logger. Defaults to True.
            enable_progress_bar (bool, optional): Whether to enable progress bar. Defaults to True.
            **trainer_kwargs: Additional trainer arguments
            
        Returns:
            L.Trainer: Lightning Trainer
        """
        # Basic callbacks
        self.callbacks = [
            EarlyStopping(
                monitor=self.monitor,
                patience=self.patience,
                mode=self.mode,
                verbose=True
            ),
            ModelCheckpoint(
                dirpath=self.checkpoint_dir,
                filename=f"best-{{epoch}}-{{{self.monitor}:.4f}}",
                monitor=self.monitor,
                mode=self.mode,
                save_top_k=1,
                verbose=True
            ),
            LearningRateMonitor(logging_interval="epoch"),
            ArchitectureLogger(log_dir=os.path.join(self.log_dir, "architecture")),
            ArchitectureVisualizer(log_dir=os.path.join(self.log_dir, "visualizations"))
        ]
        
        # Add additional callbacks
        if additional_callbacks:
            self.callbacks.extend(additional_callbacks)
        
        # Logger
        tb_logger = TensorBoardLogger(save_dir=self.log_dir) if logger else False
        
        # Create trainer
        self.trainer = L.Trainer(
            max_epochs=self.max_epochs,
            callbacks=self.callbacks,
            accelerator=self.accelerator,
            devices=self.devices,
            logger=tb_logger,
            enable_progress_bar=enable_progress_bar,
            **trainer_kwargs
        )
        
        return self.trainer
    
    def fit(
        self, 
        model: L.LightningModule, 
        train_dataloader: DataLoader, 
        val_dataloader: Optional[DataLoader] = None,
        **trainer_kwargs
    ) -> L.Trainer:
        """
        Train the model
        
        Args:
            model (L.LightningModule): Lightning model
            train_dataloader (DataLoader): Training dataloader
            val_dataloader (Optional[DataLoader], optional): Validation dataloader. Defaults to None.
            **trainer_kwargs: Additional trainer arguments
            
        Returns:
            L.Trainer: Lightning Trainer
        """
        # Set up trainer if not already set up
        if self.trainer is None:
            self.setup_trainer(**trainer_kwargs)
        
        # Train model
        self.trainer.fit(model, train_dataloader, val_dataloader)
        
        return self.trainer
    
    def test(
        self, 
        model: L.LightningModule, 
        test_dataloader: DataLoader
    ) -> Dict[str, float]:
        """
        Test the model
        
        Args:
            model (L.LightningModule): Lightning model
            test_dataloader (DataLoader): Test dataloader
            
        Returns:
            Dict[str, float]: Test metrics
        """
        if self.trainer is None:
            raise ValueError("Trainer not set up yet. Call setup_trainer() or fit() first.")
        
        # Test model
        results = self.trainer.test(model, test_dataloader)
        
        # Save results
        results_file = os.path.join(self.log_dir, "test_results.json")
        with open(results_file, "w") as f:
            json.dump(results[0], f, indent=2)
        
        return results[0]
    
    def save_model_summary(self, model: L.LightningModule, filename: str = "model_summary.txt") -> None:
        """
        Save model summary to file
        
        Args:
            model (L.LightningModule): Lightning model
            filename (str, optional): Output filename. Defaults to "model_summary.txt".
        """
        # Create summary
        summary = str(model)
        
        # Save to file
        summary_file = os.path.join(self.log_dir, filename)
        with open(summary_file, "w") as f:
            f.write(summary)
    
    def get_best_model_path(self) -> Optional[str]:
        """
        Get path to the best model checkpoint
        
        Returns:
            Optional[str]: Path to best model checkpoint
        """
        if self.trainer is None:
            raise ValueError("Trainer not set up yet. Call setup_trainer() or fit() first.")
        
        # Get checkpoint callback
        checkpoint_callback = None
        for callback in self.callbacks:
            if isinstance(callback, ModelCheckpoint):
                checkpoint_callback = callback
                break
        
        if checkpoint_callback is None:
            return None
        
        return checkpoint_callback.best_model_path
    
    def load_best_model(self, model_class: type, **model_kwargs) -> L.LightningModule:
        """
        Load the best model from checkpoint
        
        Args:
            model_class (type): Lightning model class
            **model_kwargs: Model initialization arguments
            
        Returns:
            L.LightningModule: Loaded model
        """
        best_model_path = self.get_best_model_path()
        
        if best_model_path is None or not os.path.exists(best_model_path):
            raise ValueError("No best model checkpoint found.")
        
        # Load model
        model = model_class.load_from_checkpoint(best_model_path, **model_kwargs)
        
        return model


class DataModule(L.LightningDataModule):
    """
    Lightning DataModule for standardized data handling
    
    Args:
        train_dataset (Dataset): Training dataset
        val_dataset (Optional[Dataset], optional): Validation dataset. Defaults to None.
        test_dataset (Optional[Dataset], optional): Test dataset. Defaults to None.
        batch_size (int, optional): Batch size. Defaults to 32.
        num_workers (int, optional): Number of worker processes. Defaults to 4.
        shuffle (bool, optional): Whether to shuffle training data. Defaults to True.
        pin_memory (bool, optional): Whether to pin memory. Defaults to True.
        drop_last (bool, optional): Whether to drop last incomplete batch. Defaults to False.
    """
    
    def __init__(
        self,
        train_dataset: Dataset,
        val_dataset: Optional[Dataset] = None,
        test_dataset: Optional[Dataset] = None,
        batch_size: int = 32,
        num_workers: int = 4,
        shuffle: bool = True,
        pin_memory: bool = True,
        drop_last: bool = False
    ):
        super().__init__()
        self.train_dataset = train_dataset
        self.val_dataset = val_dataset
        self.test_dataset = test_dataset
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        self.pin_memory = pin_memory
        self.drop_last = drop_last
    
    def train_dataloader(self) -> DataLoader:
        """Get training dataloader"""
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            drop_last=self.drop_last
        )
    
    def val_dataloader(self) -> Optional[DataLoader]:
        """Get validation dataloader"""
        if self.val_dataset is None:
            return None
        
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory
        )
    
    def test_dataloader(self) -> Optional[DataLoader]:
        """Get test dataloader"""
        if self.test_dataset is None:
            return None
        
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory
        )
