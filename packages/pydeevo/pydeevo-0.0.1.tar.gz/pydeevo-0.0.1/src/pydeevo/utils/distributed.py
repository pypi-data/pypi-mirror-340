"""
Advanced utilities for distributed training and memory optimization
"""
import os
import logging
import json
import time
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

import torch
import lightning as L
from lightning.fabric import Fabric
from lightning.fabric.strategies import FSDPStrategy, DDPStrategy
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    CPUOffload,
    MixedPrecision,
    BackwardPrefetch,
    ShardingStrategy,
    StateDictType,
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from safetensors.torch import save_file, load_file

logger = logging.getLogger(__name__)


class DistributedTrainingHelper:
    """
    Helper class for distributed training with Lightning Fabric
    
    This class provides utilities for distributed training with Lightning Fabric,
    including FSDP (Fully Sharded Data Parallel) support for training large models.
    
    Args:
        model_size_gb (float, optional): Estimated model size in GB. Defaults to None.
        precision (str, optional): Precision to use for training. Defaults to '16-mixed'.
        devices (Union[int, str, List[int]], optional): Devices to use. Defaults to 'auto'.
        strategy (str, optional): Distributed strategy to use. Defaults to 'auto'.
        checkpoint_dir (Optional[str], optional): Directory for checkpoints. Defaults to None.
        cpu_offload (bool, optional): Whether to offload parameters to CPU. Defaults to False.
        mixed_precision (bool, optional): Whether to use mixed precision. Defaults to True.
        activation_checkpointing (bool, optional): Whether to use activation checkpointing. Defaults to False.
        profiling (bool, optional): Whether to enable profiling. Defaults to False.
    """
    
    def __init__(
        self,
        model_size_gb: Optional[float] = None,
        precision: str = '16-mixed',
        devices: Union[int, str, List[int]] = 'auto',
        strategy: str = 'auto',
        checkpoint_dir: Optional[str] = None,
        cpu_offload: bool = False,
        mixed_precision: bool = True,
        activation_checkpointing: bool = False,
        profiling: bool = False,
    ):
        self.model_size_gb = model_size_gb
        self.precision = precision
        self.devices = devices
        self.strategy = strategy
        self.checkpoint_dir = checkpoint_dir or "./checkpoints"
        self.cpu_offload = cpu_offload
        self.mixed_precision = mixed_precision
        self.activation_checkpointing = activation_checkpointing
        self.profiling = profiling
        
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        
        self.fabric = None
        self.strategy_obj = None
        self.profiler = None
    
    def setup_fabric(self, transformer_modules: Optional[List[type]] = None):
        """
        Set up Lightning Fabric for distributed training
        
        Args:
            transformer_modules (Optional[List[type]], optional): List of transformer module types
                for auto wrapping policy. Defaults to None.
                
        Returns:
            lightning.fabric.Fabric: Configured Fabric instance
        """
        # Determine optimal strategy based on model size and available resources
        if self.strategy == 'auto':
            self.strategy = self._select_optimal_strategy()
        
        # Create appropriate strategy object
        if self.strategy == 'fsdp':
            # Configure FSDP strategy
            mp_config = None
            if self.mixed_precision:
                mp_config = MixedPrecision(
                    param_dtype=torch.float16,
                    reduce_dtype=torch.float16,
                    buffer_dtype=torch.float16,
                )
            
            # Configure auto wrapping policy if transformer modules provided
            auto_wrap_policy = None
            if transformer_modules:
                auto_wrap_policy = transformer_auto_wrap_policy(
                    transformer_layer_cls=tuple(transformer_modules)
                )
            
            # Create FSDP strategy
            self.strategy_obj = FSDPStrategy(
                auto_wrap_policy=auto_wrap_policy,
                cpu_offload=CPUOffload(offload_params=self.cpu_offload),
                mixed_precision=mp_config,
                backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
                activation_checkpointing=self.activation_checkpointing,
                sharding_strategy=ShardingStrategy.FULL_SHARD,
                state_dict_type=StateDictType.FULL_STATE_DICT,
                limit_all_gathers=True,
            )
        elif self.strategy == 'ddp':
            # Create DDP strategy
            self.strategy_obj = DDPStrategy(
                find_unused_parameters=False,
                gradient_as_bucket_view=True,
            )
        
        # Set up profiler if enabled
        if self.profiling:
            from lightning.pytorch.profilers import PyTorchProfiler
            self.profiler = PyTorchProfiler(
                activities=[
                    torch.profiler.ProfilerActivity.CPU,
                    torch.profiler.ProfilerActivity.CUDA,
                ],
                schedule=torch.profiler.schedule(
                    wait=1,
                    warmup=1,
                    active=3,
                ),
                on_trace_ready=torch.profiler.tensorboard_trace_handler(
                    os.path.join(self.checkpoint_dir, "profiler_traces")
                ),
                record_shapes=True,
                profile_memory=True,
            )
        
        # Create Fabric instance
        self.fabric = Fabric(
            accelerator="auto",
            devices=self.devices,
            precision=self.precision,
            strategy=self.strategy_obj,
            loggers=None,  # Can be configured separately
            callbacks=None,  # Can be configured separately
            profiler=self.profiler,
        )
        
        return self.fabric
    
    def _select_optimal_strategy(self) -> str:
        """
        Select the optimal distributed strategy based on model size and available resources
        
        Returns:
            str: Selected strategy ('fsdp', 'ddp', or 'single')
        """
        # Check if CUDA is available
        if not torch.cuda.is_available():
            return 'single'
        
        # Get number of GPUs
        num_gpus = torch.cuda.device_count()
        
        if num_gpus <= 1:
            return 'single'
        
        # If model size is provided, use it to determine strategy
        if self.model_size_gb is not None:
            # Calculate available GPU memory
            gpu_mem_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            
            # If model doesn't fit in a single GPU, use FSDP
            if self.model_size_gb > gpu_mem_gb * 0.8:  # 80% of GPU memory
                return 'fsdp'
        
        # Default to DDP for multi-GPU setups
        return 'ddp' if num_gpus > 1 else 'single'
    
    def setup_model_and_optimizer(
        self, 
        model: torch.nn.Module, 
        optimizer_fn: Callable,
        setup_module_fn: Optional[Callable] = None
    ) -> Tuple[torch.nn.Module, torch.optim.Optimizer]:
        """
        Set up model and optimizer with Fabric
        
        Args:
            model (torch.nn.Module): PyTorch model
            optimizer_fn (Callable): Function to create optimizer given model parameters
            setup_module_fn (Optional[Callable], optional): Function to set up model modules
                before wrapping with Fabric. Defaults to None.
                
        Returns:
            Tuple[torch.nn.Module, torch.optim.Optimizer]: Configured model and optimizer
        """
        if self.fabric is None:
            raise ValueError("Fabric not set up. Call setup_fabric() first.")
        
        # Apply custom module setup if provided
        if setup_module_fn is not None:
            model = setup_module_fn(model)
        
        # Create optimizer
        optimizer = optimizer_fn(model.parameters())
        
        # Set up model and optimizer with Fabric
        model, optimizer = self.fabric.setup(model, optimizer)
        
        return model, optimizer
    
    def save_model_checkpoint(
        self, 
        model: torch.nn.Module, 
        optimizer: torch.optim.Optimizer, 
        epoch: int, 
        metrics: Dict[str, Any],
        filename: Optional[str] = None,
        save_with_safetensors: bool = True,
    ) -> str:
        """
        Save model checkpoint with Fabric
        
        Args:
            model (torch.nn.Module): PyTorch model
            optimizer (torch.optim.Optimizer): Optimizer
            epoch (int): Current epoch
            metrics (Dict[str, Any]): Training metrics
            filename (Optional[str], optional): Checkpoint filename. Defaults to None.
            save_with_safetensors (bool, optional): Whether to use safetensors. Defaults to True.
                
        Returns:
            str: Path to saved checkpoint
        """
        if self.fabric is None:
            raise ValueError("Fabric not set up. Call setup_fabric() first.")
        
        # Generate checkpoint filename if not provided
        if filename is None:
            filename = f"model_epoch_{epoch:03d}.pt"
        
        checkpoint_path = os.path.join(self.checkpoint_dir, filename)
        
        # Save checkpoint with Fabric
        state = {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "epoch": epoch,
            "metrics": metrics,
        }
        
        if save_with_safetensors:
            # Save model state dict with safetensors (more secure)
            model_path = os.path.splitext(checkpoint_path)[0] + ".safetensors"
            save_file(model.state_dict(), model_path)
            
            # Save optimizer and metadata separately
            metadata_path = os.path.splitext(checkpoint_path)[0] + "_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(
                    {
                        "epoch": epoch,
                        "metrics": {k: float(v) if isinstance(v, torch.Tensor) else v for k, v in metrics.items()},
                    }, 
                    f, 
                    indent=2
                )
            
            logger.info(f"Saved checkpoint to {model_path} and {metadata_path}")
            return model_path
        else:
            # Save using Fabric's checkpoint system
            self.fabric.save(checkpoint_path, state)
            logger.info(f"Saved checkpoint to {checkpoint_path}")
            return checkpoint_path
    
    def load_model_checkpoint(
        self, 
        model: torch.nn.Module, 
        optimizer: Optional[torch.optim.Optimizer] = None,
        checkpoint_path: Optional[str] = None,
        load_optimizer: bool = True,
        strict: bool = True,
        from_safetensors: bool = True,
    ) -> Tuple[torch.nn.Module, Optional[torch.optim.Optimizer], Dict[str, Any]]:
        """
        Load model checkpoint with Fabric
        
        Args:
            model (torch.nn.Module): PyTorch model
            optimizer (Optional[torch.optim.Optimizer], optional): Optimizer. Defaults to None.
            checkpoint_path (Optional[str], optional): Path to checkpoint. Defaults to None.
            load_optimizer (bool, optional): Whether to load optimizer. Defaults to True.
            strict (bool, optional): Whether to enforce strict loading. Defaults to True.
            from_safetensors (bool, optional): Whether to load from safetensors. Defaults to True.
                
        Returns:
            Tuple[torch.nn.Module, Optional[torch.optim.Optimizer], Dict[str, Any]]: 
                Loaded model, optimizer, and metadata
        """
        if self.fabric is None:
            raise ValueError("Fabric not set up. Call setup_fabric() first.")
        
        # Find latest checkpoint if path not provided
        if checkpoint_path is None:
            checkpoints = [f for f in os.listdir(self.checkpoint_dir) if f.endswith(".pt") or f.endswith(".safetensors")]
            if not checkpoints:
                raise ValueError(f"No checkpoints found in {self.checkpoint_dir}")
            
            # Sort by modification time
            checkpoints = sorted(
                checkpoints,
                key=lambda x: os.path.getmtime(os.path.join(self.checkpoint_dir, x)),
                reverse=True
            )
            checkpoint_path = os.path.join(self.checkpoint_dir, checkpoints[0])
        
        # Load checkpoint
        if from_safetensors and checkpoint_path.endswith(".safetensors"):
            # Load model state dict from safetensors
            state_dict = load_file(checkpoint_path)
            model.load_state_dict(state_dict, strict=strict)
            
            # Load metadata if available
            metadata = {}
            metadata_path = os.path.splitext(checkpoint_path)[0] + "_metadata.json"
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
            
            if load_optimizer and optimizer is not None:
                logger.warning("Optimizer state not available in safetensors format.")
        else:
            # Load using Fabric's checkpoint system
            state = self.fabric.load(checkpoint_path)
            
            # Load model state dict
            model.load_state_dict(state["model"], strict=strict)
            
            # Load optimizer state dict if requested
            if load_optimizer and optimizer is not None and "optimizer" in state:
                optimizer.load_state_dict(state["optimizer"])
            
            # Extract metadata
            metadata = {
                "epoch": state.get("epoch", 0),
                "metrics": state.get("metrics", {})
            }
        
        logger.info(f"Loaded checkpoint from {checkpoint_path}")
        return model, optimizer, metadata


class MemoryOptimization:
    """
    Utilities for memory optimization in deep learning models
    
    Provides methods for analyzing and optimizing memory usage in deep learning models,
    especially useful for large models trained with limited resources.
    """
    
    @staticmethod
    def print_model_memory_usage(model: torch.nn.Module, input_shape: Tuple) -> Dict[str, float]:
        """
        Analyze memory usage of a model
        
        Args:
            model (torch.nn.Module): PyTorch model
            input_shape (Tuple): Input shape for the model
            
        Returns:
            Dict[str, float]: Memory usage statistics in MB
        """
        # Calculate parameter memory
        param_size = 0
        buffer_size = 0
        
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        
        for buffer in model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        
        param_size_mb = param_size / (1024 ** 2)
        buffer_size_mb = buffer_size / (1024 ** 2)
        
        # Estimate activation memory
        device = next(model.parameters()).device
        input_tensor = torch.randn(input_shape, device=device)
        
        # Record memory before forward pass
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()
        start_mem = torch.cuda.memory_allocated()
        
        # Forward pass
        with torch.no_grad():
            output = model(input_tensor)
        
        # Record memory after forward pass
        end_mem = torch.cuda.max_memory_allocated()
        activation_memory = end_mem - start_mem
        activation_memory_mb = activation_memory / (1024 ** 2)
        
        # Total memory
        total_memory_mb = param_size_mb + buffer_size_mb + activation_memory_mb
        
        # Print results
        memory_stats = {
            "parameter_memory_mb": param_size_mb,
            "buffer_memory_mb": buffer_size_mb,
            "activation_memory_mb": activation_memory_mb,
            "total_memory_mb": total_memory_mb
        }
        
        logger.info(f"Model Memory Usage:")
        logger.info(f"  Parameters: {param_size_mb:.2f} MB")
        logger.info(f"  Buffers: {buffer_size_mb:.2f} MB")
        logger.info(f"  Activations: {activation_memory_mb:.2f} MB")
        logger.info(f"  Total: {total_memory_mb:.2f} MB")
        
        return memory_stats
    
    @staticmethod
    def apply_activation_checkpointing(model: torch.nn.Module, modules_to_checkpoint: List[type]) -> torch.nn.Module:
        """
        Apply activation checkpointing to reduce memory usage
        
        Args:
            model (torch.nn.Module): PyTorch model
            modules_to_checkpoint (List[type]): List of module types to apply checkpointing to
            
        Returns:
            torch.nn.Module: Model with checkpointing applied
        """
        # Import checkpoint function
        from torch.utils.checkpoint import checkpoint
        
        # Apply checkpointing to specified module types
        for name, module in model.named_children():
            if any(isinstance(module, module_type) for module_type in modules_to_checkpoint):
                # Wrap module's forward method with checkpoint
                original_forward = module.forward
                
                def checkpointed_forward(self, *args, **kwargs):
                    return checkpoint(original_forward, *args, **kwargs)
                
                module.forward = checkpointed_forward.__get__(module)
            
            # Recursively apply to children
            if len(list(module.children())) > 0:
                MemoryOptimization.apply_activation_checkpointing(module, modules_to_checkpoint)
        
        return model
    
    @staticmethod
    def optimize_memory_usage(
        model: torch.nn.Module,
        use_channels_last: bool = True,
        use_compile: bool = True,
        use_activation_checkpointing: bool = False,
        modules_to_checkpoint: Optional[List[type]] = None,
    ) -> torch.nn.Module:
        """
        Apply various memory optimization techniques to a model
        
        Args:
            model (torch.nn.Module): PyTorch model
            use_channels_last (bool, optional): Whether to use channels last memory format. Defaults to True.
            use_compile (bool, optional): Whether to use torch.compile. Defaults to True.
            use_activation_checkpointing (bool, optional): Whether to use activation checkpointing. Defaults to False.
            modules_to_checkpoint (Optional[List[type]], optional): Module types to checkpoint. Defaults to None.
            
        Returns:
            torch.nn.Module: Optimized model
        """
        # Use channels last memory format for convolutional models (improves performance on CUDA)
        if use_channels_last and torch.cuda.is_available():
            model = model.to(memory_format=torch.channels_last)
            logger.info("Using channels last memory format")
        
        # Apply activation checkpointing if requested
        if use_activation_checkpointing and modules_to_checkpoint:
            model = MemoryOptimization.apply_activation_checkpointing(model, modules_to_checkpoint)
            logger.info(f"Applied activation checkpointing to {len(modules_to_checkpoint)} module types")
        
        # Use torch.compile if available and requested (PyTorch 2.0+)
        if use_compile and hasattr(torch, 'compile'):
            model = torch.compile(model)
            logger.info("Applied torch.compile to model")
        
        return model


class ModelShardingHelper:
    """
    Helper for model sharding and checkpoint sharding
    
    This class provides utilities for working with sharded models and checkpoints,
    particularly useful for very large models that don't fit in a single GPU.
    
    Args:
        model_size_gb (float): Estimated model size in GB
        checkpoint_dir (str, optional): Directory for checkpoints. Defaults to "./checkpoints".
    """
    
    def __init__(self, model_size_gb: float, checkpoint_dir: str = "./checkpoints"):
        self.model_size_gb = model_size_gb
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)
    
    def create_optimal_fsdp_config(
        self,
        transformer_modules: List[type],
        cpu_offload: bool = False,
    ) -> Dict[str, Any]:
        """
        Create optimal FSDP configuration based on model size and hardware
        
        Args:
            transformer_modules (List[type]): List of transformer module types to wrap
            cpu_offload (bool, optional): Whether to offload to CPU. Defaults to False.
            
        Returns:
            Dict[str, Any]: FSDP configuration
        """
        # Determine sharding strategy based on model size and available GPUs
        num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 0
        
        # Default to FULL_SHARD for large models
        sharding_strategy = ShardingStrategy.FULL_SHARD
        
        # For smaller models with enough GPUs, use SHARD_GRAD_OP for better performance
        if num_gpus >= 4 and self.model_size_gb < 10:
            sharding_strategy = ShardingStrategy.SHARD_GRAD_OP
        
        # Configure mixed precision
        mp_config = MixedPrecision(
            param_dtype=torch.float16,
            reduce_dtype=torch.float16,
            buffer_dtype=torch.float16,
        )
        
        # Create auto wrap policy
        auto_wrap_policy = transformer_auto_wrap_policy(
            transformer_layer_cls=tuple(transformer_modules)
        )
        
        # Return FSDP configuration
        return {
            "auto_wrap_policy": auto_wrap_policy,
            "cpu_offload": CPUOffload(offload_params=cpu_offload),
            "mixed_precision": mp_config,
            "backward_prefetch": BackwardPrefetch.BACKWARD_PRE,
            "sharding_strategy": sharding_strategy,
            "state_dict_type": StateDictType.FULL_STATE_DICT,
            "limit_all_gathers": True,
        }
    
    def convert_checkpoint_to_sharded(
        self,
        checkpoint_path: str,
        num_shards: int,
        save_with_safetensors: bool = True,
    ) -> List[str]:
        """
        Convert a large checkpoint to sharded checkpoints
        
        Args:
            checkpoint_path (str): Path to the checkpoint
            num_shards (int): Number of shards to create
            save_with_safetensors (bool, optional): Whether to use safetensors. Defaults to True.
            
        Returns:
            List[str]: Paths to sharded checkpoints
        """
        # Load checkpoint
        if checkpoint_path.endswith(".safetensors"):
            state_dict = load_file(checkpoint_path)
        else:
            state_dict = torch.load(checkpoint_path, map_location="cpu")
            if "model" in state_dict:
                state_dict = state_dict["model"]
        
        # Get all keys
        all_keys = list(state_dict.keys())
        keys_per_shard = len(all_keys) // num_shards + (1 if len(all_keys) % num_shards != 0 else 0)
        
        # Create shards
        shard_paths = []
        for i in range(num_shards):
            start_idx = i * keys_per_shard
            end_idx = min((i + 1) * keys_per_shard, len(all_keys))
            shard_keys = all_keys[start_idx:end_idx]
            
            # Create shard state dict
            shard_state_dict = {k: state_dict[k] for k in shard_keys}
            
            # Save shard
            base_path = os.path.splitext(checkpoint_path)[0]
            shard_path = f"{base_path}_shard_{i+1}_of_{num_shards}"
            
            if save_with_safetensors:
                shard_path += ".safetensors"
                save_file(shard_state_dict, shard_path)
            else:
                shard_path += ".pt"
                torch.save(shard_state_dict, shard_path)
            
            shard_paths.append(shard_path)
            logger.info(f"Saved shard {i+1}/{num_shards} with {len(shard_keys)} keys to {shard_path}")
        
        return shard_paths
    
    def load_sharded_checkpoint(
        self,
        model: torch.nn.Module,
        shard_paths: List[str],
        strict: bool = False,
    ) -> torch.nn.Module:
        """
        Load a model from sharded checkpoints
        
        Args:
            model (torch.nn.Module): PyTorch model
            shard_paths (List[str]): Paths to sharded checkpoints
            strict (bool, optional): Whether to strictly enforce loading. Defaults to False.
            
        Returns:
            torch.nn.Module: Model with loaded weights
        """
        # Create empty state dict
        state_dict = {}
        
        # Load each shard
        for shard_path in shard_paths:
            logger.info(f"Loading shard from {shard_path}")
            
            if shard_path.endswith(".safetensors"):
                shard_state_dict = load_file(shard_path)
            else:
                shard_state_dict = torch.load(shard_path, map_location="cpu")
                if "model" in shard_state_dict:
                    shard_state_dict = shard_state_dict["model"]
            
            # Update combined state dict
            state_dict.update(shard_state_dict)
        
        # Load state dict into model
        model.load_state_dict(state_dict, strict=strict)
        logger.info(f"Successfully loaded model from {len(shard_paths)} shards with {len(state_dict)} parameters")
        
        return model


class BatchSizeOptimizer:
    """
    Utility to find the optimal batch size for a model
    
    This class automatically finds the optimal batch size for a model
    based on available GPU memory and model characteristics.
    
    Args:
        model (torch.nn.Module): PyTorch model
        input_shape_template (Tuple): Template for input shape (without batch dimension)
        device (str, optional): Device to use. Defaults to "cuda".
        start_batch_size (int, optional): Starting batch size. Defaults to 1.
        max_batch_size (int, optional): Maximum batch size to try. Defaults to 512.
        max_memory_usage (float, optional): Maximum fraction of GPU memory to use. Defaults to 0.85.
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        input_shape_template: Tuple,
        device: str = "cuda",
        start_batch_size: int = 1,
        max_batch_size: int = 512,
        max_memory_usage: float = 0.85,
    ):
        self.model = model
        self.input_shape_template = input_shape_template
        self.device = device
        self.start_batch_size = start_batch_size
        self.max_batch_size = max_batch_size
        self.max_memory_usage = max_memory_usage
    
    def find_optimal_batch_size(
        self, 
        optimization_metric: str = "memory",
        verbose: bool = True,
    ) -> int:
        """
        Find the optimal batch size
        
        Args:
            optimization_metric (str, optional): What to optimize for - "memory" or "speed". 
                Defaults to "memory".
            verbose (bool, optional): Whether to print progress. Defaults to True.
            
        Returns:
            int: Optimal batch size
        """
        if not torch.cuda.is_available() and self.device == "cuda":
            logger.warning("CUDA not available, using CPU. This will be slow.")
            self.device = "cpu"
        
        # Move model to device
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Binary search for maximum batch size
        low, high = self.start_batch_size, self.max_batch_size
        optimal_batch_size = low
        
        # For speed optimization, we'll also track timing
        best_throughput = 0
        
        while low <= high:
            mid = (low + high) // 2
            
            if verbose:
                logger.info(f"Trying batch size: {mid}")
            
            try:
                # Reset memory stats
                if self.device == "cuda":
                    torch.cuda.reset_peak_memory_stats()
                    torch.cuda.empty_cache()
                
                # Create input tensor
                input_tensor = torch.randn((mid,) + self.input_shape_template, device=self.device)
                
                # Time the forward pass
                start_time = time.time()
                
                # Forward pass
                with torch.no_grad():
                    _ = self.model(input_tensor)
                
                # Calculate throughput
                elapsed = time.time() - start_time
                throughput = mid / elapsed
                
                if verbose:
                    logger.info(f"  Success - Throughput: {throughput:.2f} samples/sec")
                
                # Check memory usage
                if self.device == "cuda":
                    peak_memory = torch.cuda.max_memory_allocated()
                    total_memory = torch.cuda.get_device_properties(0).total_memory
                    memory_usage = peak_memory / total_memory
                    
                    if verbose:
                        logger.info(f"  Memory usage: {memory_usage:.2%}")
                    
                    # If we're over our memory threshold, we should go lower
                    if memory_usage > self.max_memory_usage:
                        if verbose:
                            logger.info("  Memory usage too high, reducing batch size")
                        high = mid - 1
                        continue
                
                # If we're optimizing for speed
                if optimization_metric == "speed" and throughput > best_throughput:
                    best_throughput = throughput
                    optimal_batch_size = mid
                else:
                    # For memory optimization, always prefer larger batch size
                    optimal_batch_size = mid
                
                # Try a larger batch size
                low = mid + 1
                
            except RuntimeError as e:
                # Check if it's an out-of-memory error
                if "CUDA out of memory" in str(e) or "DefaultCPUAllocator: not enough memory" in str(e):
                    if verbose:
                        logger.info(f"  Out of memory with batch size {mid}, reducing")
                    # Try a smaller batch size
                    high = mid - 1
                else:
                    # Some other error
                    raise e
        
        # Suggest a slightly smaller batch size for stability
        if optimization_metric == "memory" and optimal_batch_size > 1:
            # Reduce by 5% to provide some headroom
            optimal_batch_size = max(1, int(optimal_batch_size * 0.95))
        
        logger.info(f"Optimal batch size: {optimal_batch_size}")
        return optimal_batch_size


class SecurityWrapper:
    """
    Security utilities for model serialization and deserialization
    
    This class provides secure methods for saving and loading models
    to prevent vulnerabilities related to insecure deserialization.
    
    Args:
        base_dir (str, optional): Base directory for saving models. Defaults to "./secure_models".
    """
    
    def __init__(self, base_dir: str = "./secure_models"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def save_model_secure(
        self,
        model: torch.nn.Module,
        metadata: Dict[str, Any],
        filename: str,
    ) -> str:
        """
        Save model securely using safetensors
        
        Args:
            model (torch.nn.Module): PyTorch model
            metadata (Dict[str, Any]): Metadata to save
            filename (str): Filename for the model
            
        Returns:
            str: Path to saved model
        """
        # Ensure we're using safetensors
        model_path = os.path.join(self.base_dir, filename)
        if not model_path.endswith(".safetensors"):
            model_path += ".safetensors"
        
        # Get state dict
        state_dict = model.state_dict()
        
        # Save model state dict
        save_file(state_dict, model_path)
        
        # Save metadata separately as JSON
        metadata_path = os.path.splitext(model_path)[0] + "_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(
                {k: (float(v) if isinstance(v, torch.Tensor) else v) for k, v in metadata.items()}, 
                f, 
                indent=2
            )
        
        logger.info(f"Securely saved model to {model_path} and metadata to {metadata_path}")
        return model_path
    
    def load_model_secure(
        self,
        model: torch.nn.Module,
        filename: str,
        strict: bool = True,
    ) -> Tuple[torch.nn.Module, Dict[str, Any]]:
        """
        Load model securely using safetensors
        
        Args:
            model (torch.nn.Module): PyTorch model
            filename (str): Filename of the model
            strict (bool, optional): Whether to strictly enforce loading. Defaults to True.
            
        Returns:
            Tuple[torch.nn.Module, Dict[str, Any]]: Loaded model and metadata
        """
        # Ensure we're using safetensors
        model_path = os.path.join(self.base_dir, filename)
        if not model_path.endswith(".safetensors"):
            model_path += ".safetensors"
        
        # Check if file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load model state dict
        state_dict = load_file(model_path)
        
        # Load model
        model.load_state_dict(state_dict, strict=strict)
        
        # Load metadata if available
        metadata = {}
        metadata_path = os.path.splitext(model_path)[0] + "_metadata.json"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
        
        logger.info(f"Securely loaded model from {model_path}")
        return model, metadata
