"""
Performance profiling and benchmarking utilities
"""
import os
import time
import json
import logging
import platform
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

import torch
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
import lightning as L

logger = logging.getLogger(__name__)


class ModelProfiler:
    """
    Utility for profiling PyTorch models
    
    This class provides methods for profiling model performance, 
    including inference time, memory usage, and parameter counts.
    
    Args:
        model (torch.nn.Module): PyTorch model to profile
        input_shape (Tuple): Input shape for the model (including batch dimension)
        device (str, optional): Device to run profiling on. Defaults to "cuda" if available.
        log_dir (str, optional): Directory to save profile results. Defaults to "./profiles".
    """
    
    def __init__(
        self, 
        model: torch.nn.Module, 
        input_shape: Tuple,
        device: Optional[str] = None,
        log_dir: str = "./profiles"
    ):
        self.model = model
        self.input_shape = input_shape
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.log_dir = log_dir
        
        os.makedirs(log_dir, exist_ok=True)
    
    def profile_inference_time(
        self, 
        num_warmup: int = 10, 
        num_runs: int = 100,
        batch_size: Optional[int] = None,
    ) -> Dict[str, float]:
        """
        Profile model inference time
        
        Args:
            num_warmup (int, optional): Number of warmup runs. Defaults to 10.
            num_runs (int, optional): Number of timed runs. Defaults to 100.
            batch_size (Optional[int], optional): Custom batch size. Defaults to None
                (uses batch size from input_shape).
                
        Returns:
            Dict[str, float]: Inference time statistics in milliseconds
        """
        # Move model to device and set to eval mode
        model = self.model.to(self.device)
        model.eval()
        
        # Create input tensor
        if batch_size is not None:
            input_shape = (batch_size,) + self.input_shape[1:]
        else:
            input_shape = self.input_shape
        
        input_tensor = torch.randn(input_shape, device=self.device)
        
        # Warmup runs
        with torch.no_grad():
            for _ in range(num_warmup):
                _ = model(input_tensor)
        
        # Synchronize before timing
        if self.device == "cuda":
            torch.cuda.synchronize()
        
        # Timed runs
        times = []
        with torch.no_grad():
            for _ in range(num_runs):
                start_time = time.time()
                _ = model(input_tensor)
                
                if self.device == "cuda":
                    torch.cuda.synchronize()
                
                end_time = time.time()
                times.append((end_time - start_time) * 1000)  # Convert to ms
        
        # Calculate statistics
        times = np.array(times)
        stats = {
            "mean_ms": float(np.mean(times)),
            "median_ms": float(np.median(times)),
            "min_ms": float(np.min(times)),
            "max_ms": float(np.max(times)),
            "std_ms": float(np.std(times)),
            "p95_ms": float(np.percentile(times, 95)),
            "p99_ms": float(np.percentile(times, 99)),
            "samples_per_second": float(input_shape[0] * 1000 / np.mean(times)),
            "batch_size": input_shape[0],
        }
        
        # Print summary
        logger.info(f"Inference Time Summary (batch size={input_shape[0]}):")
        logger.info(f"  Mean: {stats['mean_ms']:.2f} ms")
        logger.info(f"  Median: {stats['median_ms']:.2f} ms")
        logger.info(f"  Min: {stats['min_ms']:.2f} ms")
        logger.info(f"  Max: {stats['max_ms']:.2f} ms")
        logger.info(f"  P95: {stats['p95_ms']:.2f} ms")
        logger.info(f"  P99: {stats['p99_ms']:.2f} ms")
        logger.info(f"  Throughput: {stats['samples_per_second']:.2f} samples/sec")
        
        return stats
    
    def profile_memory_usage(self) -> Dict[str, float]:
        """
        Profile model memory usage
        
        Returns:
            Dict[str, float]: Memory usage statistics in MB
        """
        # Move model to device and set to eval mode
        model = self.model.to(self.device)
        model.eval()
        
        # Create input tensor
        input_tensor = torch.randn(self.input_shape, device=self.device)
        
        # Calculate parameter memory
        param_size = 0
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        
        param_size_mb = param_size / (1024 ** 2)
        
        # Empty cache and record memory before forward pass
        if self.device == "cuda":
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
            start_mem = torch.cuda.memory_allocated()
        
        # Forward pass
        with torch.no_grad():
            _ = model(input_tensor)
        
        # Record memory after forward pass
        if self.device == "cuda":
            end_mem = torch.cuda.max_memory_allocated()
            activation_memory = end_mem - start_mem
            activation_memory_mb = activation_memory / (1024 ** 2)
            
            # Get total GPU memory
            total_gpu_memory = torch.cuda.get_device_properties(0).total_memory
            total_gpu_memory_mb = total_gpu_memory / (1024 ** 2)
        else:
            # CPU memory estimation is less accurate
            activation_memory_mb = 0  # Not easily measurable on CPU
            total_gpu_memory_mb = 0
        
        # Count number of parameters
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        # Calculate total memory
        total_memory_mb = param_size_mb + activation_memory_mb
        
        # Create memory stats
        memory_stats = {
            "parameter_memory_mb": param_size_mb,
            "activation_memory_mb": activation_memory_mb,
            "total_memory_mb": total_memory_mb,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "total_gpu_memory_mb": total_gpu_memory_mb,
            "memory_utilization": total_memory_mb / total_gpu_memory_mb if total_gpu_memory_mb > 0 else 0,
        }
        
        # Print summary
        logger.info(f"Memory Usage Summary:")
        logger.info(f"  Parameters: {total_params:,} ({memory_stats['parameter_memory_mb']:.2f} MB)")
        logger.info(f"  Activations: {memory_stats['activation_memory_mb']:.2f} MB")
        logger.info(f"  Total: {memory_stats['total_memory_mb']:.2f} MB")
        if self.device == "cuda":
            logger.info(f"  GPU Memory Utilization: {memory_stats['memory_utilization']:.2%}")
        
        return memory_stats
    
    def profile_layer_compute_time(
        self, 
        num_runs: int = 10, 
        return_per_layer: bool = False,
    ) -> Dict[str, Union[float, Dict[str, float]]]:
        """
        Profile computation time for each layer
        
        Args:
            num_runs (int, optional): Number of runs. Defaults to 10.
            return_per_layer (bool, optional): Whether to return per-layer times. Defaults to False.
            
        Returns:
            Dict[str, Union[float, Dict[str, float]]]: Layer timing statistics
        """
        # Move model to device and set to eval mode
        model = self.model.to(self.device)
        model.eval()
        
        # Create input tensor
        input_tensor = torch.randn(self.input_shape, device=self.device)
        
        # Dictionary to store times
        layer_times = {}
        
        # Define forward hooks
        def hook_fn(name):
            def hook(module, input, output):
                if self.device == "cuda":
                    torch.cuda.synchronize()
                end_time = time.time()
                if name in layer_times:
                    layer_times[name].append(end_time)
                else:
                    layer_times[name] = [end_time]
                return None
            return hook
        
        def pre_hook_fn(name):
            def hook(module, input):
                if self.device == "cuda":
                    torch.cuda.synchronize()
                start_time = time.time()
                if name + "_pre" in layer_times:
                    layer_times[name + "_pre"].append(start_time)
                else:
                    layer_times[name + "_pre"] = [start_time]
                return None
            return hook
        
        # Register hooks
        hooks = []
        pre_hooks = []
        for name, module in model.named_modules():
            if name:  # Skip the root module
                hooks.append(module.register_forward_hook(hook_fn(name)))
                pre_hooks.append(module.register_forward_pre_hook(pre_hook_fn(name)))
        
        # Multiple forward passes
        with torch.no_grad():
            for _ in range(num_runs):
                _ = model(input_tensor)
        
        # Remove hooks
        for hook in hooks:
            hook.remove()
        for hook in pre_hooks:
            hook.remove()
        
        # Calculate time per layer
        layer_compute_times = {}
        for name in layer_times:
            if name.endswith("_pre"):
                base_name = name[:-4]
                if base_name in layer_times:
                    times = []
                    pre_times = layer_times[name]
                    post_times = layer_times[base_name]
                    for i in range(1, len(pre_times)):  # Skip first run (warmup)
                        times.append((post_times[i] - pre_times[i]) * 1000)  # ms
                    layer_compute_times[base_name] = times
        
        # Calculate statistics
        total_time = 0
        layer_stats = {}
        for name, times in layer_compute_times.items():
            mean_time = np.mean(times) if times else 0
            total_time += mean_time
            layer_stats[name] = {
                "mean_ms": float(mean_time),
                "percent": 0,  # Will fill later
                "max_ms": float(np.max(times)) if times else 0,
                "min_ms": float(np.min(times)) if times else 0,
            }
        
        # Calculate percentages
        for name in layer_stats:
            layer_stats[name]["percent"] = layer_stats[name]["mean_ms"] / total_time if total_time > 0 else 0
        
        # Sort by compute time
        sorted_layers = sorted(
            layer_stats.items(), 
            key=lambda x: x[1]["mean_ms"], 
            reverse=True
        )
        
        # Print top 10 most expensive layers
        logger.info(f"Top 10 most compute-intensive layers:")
        for i, (name, stats) in enumerate(sorted_layers[:10]):
            logger.info(f"  {i+1}. {name}: {stats['mean_ms']:.2f} ms ({stats['percent']:.2%})")
        
        result = {
            "total_compute_time_ms": float(total_time),
        }
        
        if return_per_layer:
            result["layer_stats"] = layer_stats
        
        return result
    
    def generate_profile_report(
        self, 
        include_layer_profile: bool = True,
        batch_sizes: Optional[List[int]] = None,
    ) -> str:
        """
        Generate comprehensive profile report
        
        Args:
            include_layer_profile (bool, optional): Whether to include layer-wise profiling. 
                Defaults to True.
            batch_sizes (Optional[List[int]], optional): Batch sizes to profile. 
                Defaults to None (uses [1, 2, 4, 8, 16, 32] if possible).
                
        Returns:
            str: Path to saved report
        """
        # Get hardware info
        system_info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "torch_version": torch.__version__,
            "cuda_version": torch.version.cuda if torch.cuda.is_available() else "N/A",
            "device": self.device,
        }
        
        if self.device == "cuda":
            system_info["gpu"] = torch.cuda.get_device_name(0)
            system_info["gpu_count"] = torch.cuda.device_count()
        
        # Profile memory
        memory_stats = self.profile_memory_usage()
        
        # Profile batch sizes
        if batch_sizes is None:
            original_batch_size = self.input_shape[0]
            batch_sizes = []
            for bs in [1, 2, 4, 8, 16, 32]:
                if bs <= original_batch_size * 2:  # Don't go too far beyond original batch size
                    batch_sizes.append(bs)
        
        batch_size_results = {}
        for bs in batch_sizes:
            try:
                batch_size_results[bs] = self.profile_inference_time(
                    num_warmup=5, 
                    num_runs=20, 
                    batch_size=bs
                )
            except RuntimeError as e:
                logger.warning(f"Failed to profile batch size {bs}: {e}")
        
        # Profile layer compute time if requested
        layer_stats = None
        if include_layer_profile:
            result = self.profile_layer_compute_time(return_per_layer=True)
            layer_stats = result.get("layer_stats", None)
        
        # Compile results
        profile_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": system_info,
            "model_name": self.model.__class__.__name__,
            "input_shape": list(self.input_shape),
            "memory_stats": memory_stats,
            "batch_size_results": batch_size_results,
            "layer_stats": layer_stats,
        }
        
        # Save results
        report_path = os.path.join(
            self.log_dir, 
            f"profile_{self.model.__class__.__name__}_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(report_path, "w") as f:
            json.dump(profile_results, f, indent=2)
        
        logger.info(f"Profile report saved to {report_path}")
        
        # Generate plots
        self._generate_profile_plots(profile_results)
        
        return report_path
    
    def _generate_profile_plots(self, profile_results: Dict[str, Any]) -> None:
        """
        Generate plots from profile results
        
        Args:
            profile_results (Dict[str, Any]): Profile results
        """
        # Get model name for plot titles
        model_name = profile_results["model_name"]
        
        # Create batch size vs throughput plot
        if profile_results["batch_size_results"]:
            plt.figure(figsize=(10, 6))
            
            batch_sizes = sorted([int(bs) for bs in profile_results["batch_size_results"].keys()])
            throughput = [profile_results["batch_size_results"][str(bs)]["samples_per_second"] for bs in batch_sizes]
            latency = [profile_results["batch_size_results"][str(bs)]["mean_ms"] for bs in batch_sizes]
            
            # Plot throughput
            plt.subplot(1, 2, 1)
            plt.plot(batch_sizes, throughput, 'o-', color='blue')
            plt.xlabel('Batch Size')
            plt.ylabel('Throughput (samples/sec)')
            plt.title(f'{model_name} Throughput vs Batch Size')
            plt.grid(True)
            
            # Plot latency
            plt.subplot(1, 2, 2)
            plt.plot(batch_sizes, latency, 'o-', color='red')
            plt.xlabel('Batch Size')
            plt.ylabel('Latency (ms)')
            plt.title(f'{model_name} Latency vs Batch Size')
            plt.grid(True)
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.log_dir, f"{model_name}_batch_performance.png"))
            plt.close()
        
        # Create layer compute time plot
        if profile_results["layer_stats"]:
            # Sort layers by compute time
            layer_stats = profile_results["layer_stats"]
            sorted_layers = sorted(
                layer_stats.items(), 
                key=lambda x: x[1]["mean_ms"], 
                reverse=True
            )
            
            # Plot top 15 layers
            top_n = min(15, len(sorted_layers))
            top_layers = sorted_layers[:top_n]
            
            plt.figure(figsize=(12, 6))
            
            names = [layer[0].split(".")[-1] for layer in top_layers]  # Use only last part of name
            compute_times = [layer[1]["mean_ms"] for layer in top_layers]
            percentages = [layer[1]["percent"] for layer in top_layers]
            
            # Create horizontal bar chart
            y_pos = range(len(names))
            plt.barh(y_pos, compute_times, align='center', color='skyblue')
            
            # Add percentage labels
            for i, (time, pct) in enumerate(zip(compute_times, percentages)):
                plt.text(time + 0.1, i, f"{time:.2f} ms ({pct:.1%})", va='center')
            
            plt.yticks(y_pos, names)
            plt.xlabel('Compute Time (ms)')
            plt.title(f'Top {top_n} Most Compute-Intensive Layers in {model_name}')
            plt.tight_layout()
            
            plt.savefig(os.path.join(self.log_dir, f"{model_name}_layer_profile.png"))
            plt.close()


class ArchitectureBenchmarker:
    """
    Benchmark different neural network architectures
    
    This class allows easy benchmarking of multiple model architectures
    to compare performance metrics.
    
    Args:
        models (Dict[str, torch.nn.Module]): Dictionary of models to benchmark
        input_shape (Tuple): Input shape for models (including batch dimension)
        device (str, optional): Device to run benchmarks on. Defaults to "cuda" if available.
        log_dir (str, optional): Directory to save benchmark results. Defaults to "./benchmarks".
    """
    
    def __init__(
        self, 
        models: Dict[str, torch.nn.Module],
        input_shape: Tuple,
        device: Optional[str] = None,
        log_dir: str = "./benchmarks"
    ):
        self.models = models
        self.input_shape = input_shape
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.log_dir = log_dir
        
        os.makedirs(log_dir, exist_ok=True)
    
    def run_benchmarks(
        self,
        benchmark_memory: bool = True,
        benchmark_inference: bool = True,
        benchmark_throughput: bool = True,
        batch_size: Optional[int] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Run comprehensive benchmarks on all models
        
        Args:
            benchmark_memory (bool, optional): Whether to benchmark memory usage. Defaults to True.
            benchmark_inference (bool, optional): Whether to benchmark inference time. Defaults to True.
            benchmark_throughput (bool, optional): Whether to benchmark throughput. Defaults to True.
            batch_size (Optional[int], optional): Custom batch size for throughput test. 
                Defaults to None (uses batch size from input_shape).
                
        Returns:
            Dict[str, Dict[str, Any]]: Benchmark results per model
        """
        results = {}
        
        for name, model in self.models.items():
            logger.info(f"Benchmarking {name}...")
            model_results = {}
            profiler = ModelProfiler(model, self.input_shape, self.device, self.log_dir)
            
            # Benchmark memory
            if benchmark_memory:
                model_results["memory"] = profiler.profile_memory_usage()
            
            # Benchmark inference
            if benchmark_inference:
                model_results["inference"] = profiler.profile_inference_time()
            
            # Benchmark throughput with different batch size
            if benchmark_throughput and batch_size is not None:
                model_results["throughput"] = profiler.profile_inference_time(batch_size=batch_size)
            
            results[name] = model_results
        
        # Save results
        benchmark_path = os.path.join(
            self.log_dir, 
            f"benchmark_results_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(benchmark_path, "w") as f:
            # Convert any non-serializable values to strings or numbers
            serializable_results = json.loads(
                json.dumps(results, default=lambda o: float(o) if isinstance(o, torch.Tensor) else str(o))
            )
            json.dump(serializable_results, f, indent=2)
        
        logger.info(f"Benchmark results saved to {benchmark_path}")
        
        # Generate comparison plots
        self._generate_comparison_plots(results)
        
        return results
    
    def _generate_comparison_plots(self, results: Dict[str, Dict[str, Any]]) -> None:
        """
        Generate comparison plots from benchmark results
        
        Args:
            results (Dict[str, Dict[str, Any]]): Benchmark results
        """
        # Plot memory comparison
        if all("memory" in model_results for model_results in results.values()):
            plt.figure(figsize=(12, 6))
            
            model_names = list(results.keys())
            param_memory = [results[name]["memory"]["parameter_memory_mb"] for name in model_names]
            activation_memory = [results[name]["memory"]["activation_memory_mb"] for name in model_names]
            
            x = range(len(model_names))
            width = 0.35
            
            plt.bar(x, param_memory, width, label='Parameter Memory', color='skyblue')
            plt.bar([i + width for i in x], activation_memory, width, label='Activation Memory', color='orange')
            
            plt.xlabel('Model')
            plt.ylabel('Memory (MB)')
            plt.title('Memory Usage Comparison')
            plt.xticks([i + width/2 for i in x], model_names, rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            
            plt.savefig(os.path.join(self.log_dir, "memory_comparison.png"))
            plt.close()
        
        # Plot inference time comparison
        if all("inference" in model_results for model_results in results.values()):
            plt.figure(figsize=(12, 6))
            
            model_names = list(results.keys())
            inference_times = [results[name]["inference"]["mean_ms"] for name in model_names]
            
            plt.bar(model_names, inference_times, color='skyblue')
            plt.xlabel('Model')
            plt.ylabel('Inference Time (ms)')
            plt.title('Inference Time Comparison')
            plt.xticks(rotation=45, ha='right')
            
            # Add labels
            for i, v in enumerate(inference_times):
                plt.text(i, v + 0.5, f"{v:.2f} ms", ha='center')
            
            plt.tight_layout()
            
            plt.savefig(os.path.join(self.log_dir, "inference_comparison.png"))
            plt.close()
        
        # Plot throughput comparison
        if all("throughput" in model_results for model_results in results.values()):
            plt.figure(figsize=(12, 6))
            
            model_names = list(results.keys())
            throughput = [results[name]["throughput"]["samples_per_second"] for name in model_names]
            
            plt.bar(model_names, throughput, color='skyblue')
            plt.xlabel('Model')
            plt.ylabel('Throughput (samples/sec)')
            plt.title('Throughput Comparison')
            plt.xticks(rotation=45, ha='right')
            
            # Add labels
            for i, v in enumerate(throughput):
                plt.text(i, v + 0.5, f"{v:.2f}", ha='center')
            
            plt.tight_layout()
            
            plt.savefig(os.path.join(self.log_dir, "throughput_comparison.png"))
            plt.close()


class LightningProfileCallback(L.Callback):
    """
    Lightning callback for model profiling
    
    This callback profiles model performance during training,
    including iteration time, memory usage, and throughput.
    
    Args:
        profile_every_n_steps (int, optional): How often to profile. Defaults to 100.
        log_dir (str, optional): Directory to save profiles. Defaults to "./profiles".
        profile_memory (bool, optional): Whether to profile memory. Defaults to True.
        profile_batch_scaling (bool, optional): Whether to profile batch scaling. Defaults to False.
    """
    
    def __init__(
        self,
        profile_every_n_steps: int = 100,
        log_dir: str = "./profiles",
        profile_memory: bool = True,
        profile_batch_scaling: bool = False,
    ):
        self.profile_every_n_steps = profile_every_n_steps
        self.log_dir = log_dir
        self.profile_memory = profile_memory
        self.profile_batch_scaling = profile_batch_scaling
        
        os.makedirs(log_dir, exist_ok=True)
        
        self.step_times = []
        self.memory_usage = []
        self.throughput = []
        self.last_time = None
    
    def on_train_start(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """Log initial model state"""
        if self.profile_memory:
            self._log_memory_usage(trainer, pl_module)
    
    def on_train_batch_start(self, trainer: L.Trainer, pl_module: L.LightningModule, *args, **kwargs) -> None:
        """Record start time of batch"""
        self.last_time = time.time()
    
    def on_train_batch_end(self, trainer: L.Trainer, pl_module: L.LightningModule, *args, **kwargs) -> None:
        """Record end time of batch and calculate metrics"""
        if self.last_time is None:
            return
        
        # Calculate step time
        step_time = time.time() - self.last_time
        self.step_times.append(step_time)
        
        # Calculate throughput
        batch_size = trainer.train_dataloader.batch_size
        throughput = batch_size / step_time
        self.throughput.append(throughput)
        
        # Log memory usage
        if self.profile_memory:
            self._log_memory_usage(trainer, pl_module)
        
        # Profile at specified intervals
        if trainer.global_step % self.profile_every_n_steps == 0:
            self._log_profile(trainer, pl_module)
    
    def on_train_end(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """Log final profile summary"""
        self._save_profiles(trainer, pl_module)
    
    def _log_memory_usage(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """Log current memory usage"""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / (1024 ** 2)
            reserved = torch.cuda.memory_reserved() / (1024 ** 2)
            max_allocated = torch.cuda.max_memory_allocated() / (1024 ** 2)
            
            memory_info = {
                "allocated_mb": allocated,
                "reserved_mb": reserved,
                "max_allocated_mb": max_allocated,
                "step": trainer.global_step,
            }
            
            self.memory_usage.append(memory_info)
    
    def _log_profile(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """Log current profile data"""
        # Calculate statistics
        recent_times = self.step_times[-min(100, len(self.step_times)):]
        recent_throughput = self.throughput[-min(100, len(self.throughput)):]
        
        profile_data = {
            "step": trainer.global_step,
            "iteration_time": {
                "mean_ms": float(np.mean(recent_times) * 1000),
                "median_ms": float(np.median(recent_times) * 1000),
                "min_ms": float(np.min(recent_times) * 1000),
                "max_ms": float(np.max(recent_times) * 1000),
                "p95_ms": float(np.percentile(recent_times, 95) * 1000),
            },
            "throughput": {
                "mean": float(np.mean(recent_throughput)),
                "median": float(np.median(recent_throughput)),
                "min": float(np.min(recent_throughput)),
                "max": float(np.max(recent_throughput)),
            },
        }
        
        # Log to Lightning's logger
        if trainer.logger:
            trainer.logger.log_metrics({
                "iteration_time": profile_data["iteration_time"]["mean_ms"],
                "throughput": profile_data["throughput"]["mean"],
            }, step=trainer.global_step)
        
        # Profile batch scaling if enabled
        if self.profile_batch_scaling and trainer.global_step > 0 and trainer.global_step % (self.profile_every_n_steps * 5) == 0:
            try:
                device = pl_module.device
                batch_profiler = ModelProfiler(pl_module, (1,) + trainer.train_dataloader.dataset[0][0].shape, device, self.log_dir)
                batch_sizes = [1, 2, 4, 8, 16]
                
                for bs in batch_sizes:
                    try:
                        profile_data[f"batch_{bs}"] = batch_profiler.profile_inference_time(
                            num_warmup=3, 
                            num_runs=10, 
                            batch_size=bs
                        )
                    except RuntimeError:
                        break
            except Exception as e:
                logger.warning(f"Failed to profile batch scaling: {e}")
        
        logger.info(f"Profile at step {trainer.global_step}:")
        logger.info(f"  Iteration time: {profile_data['iteration_time']['mean_ms']:.2f} ms")
        logger.info(f"  Throughput: {profile_data['throughput']['mean']:.2f} samples/sec")
    
    def _save_profiles(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """Save profile data to disk"""
        # Calculate overall statistics
        if self.step_times:
            iteration_time = {
                "mean_ms": float(np.mean(self.step_times) * 1000),
                "median_ms": float(np.median(self.step_times) * 1000),
                "min_ms": float(np.min(self.step_times) * 1000),
                "max_ms": float(np.max(self.step_times) * 1000),
                "p95_ms": float(np.percentile(self.step_times, 95) * 1000),
            }
        else:
            iteration_time = {}
        
        if self.throughput:
            throughput = {
                "mean": float(np.mean(self.throughput)),
                "median": float(np.median(self.throughput)),
                "min": float(np.min(self.throughput)),
                "max": float(np.max(self.throughput)),
                "p95": float(np.percentile(self.throughput, 95)),
            }
        else:
            throughput = {}
        
        # Compile profile data
        profile_data = {
            "model_name": pl_module.__class__.__name__,
            "final_step": trainer.global_step,
            "total_iterations": len(self.step_times),
            "iteration_time": iteration_time,
            "throughput": throughput,
            "memory_usage": self.memory_usage if self.profile_memory else None,
        }
        
        # Save to disk
        profile_path = os.path.join(
            self.log_dir, 
            f"training_profile_{pl_module.__class__.__name__}_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(profile_path, "w") as f:
            json.dump(profile_data, f, indent=2)
        
        logger.info(f"Training profile saved to {profile_path}")
        
        # Generate plots
        self._generate_profile_plots(profile_data)
    
    def _generate_profile_plots(self, profile_data: Dict[str, Any]) -> None:
        """Generate plots from profile data"""
        model_name = profile_data["model_name"]
        
        # Plot iteration time and throughput over time
        if profile_data.get("memory_usage"):
            plt.figure(figsize=(12, 8))
            
            # Extract data
            steps = [entry["step"] for entry in profile_data["memory_usage"]]
            allocated = [entry["allocated_mb"] for entry in profile_data["memory_usage"]]
            reserved = [entry["reserved_mb"] for entry in profile_data["memory_usage"]]
            max_allocated = [entry["max_allocated_mb"] for entry in profile_data["memory_usage"]]
            
            # Plot memory
            plt.subplot(2, 1, 1)
            plt.plot(steps, allocated, label='Allocated')
            plt.plot(steps, reserved, label='Reserved')
            plt.plot(steps, max_allocated, label='Max Allocated')
            plt.xlabel('Training Step')
            plt.ylabel('Memory (MB)')
            plt.title(f'{model_name} Memory Usage During Training')
            plt.legend()
            plt.grid(True)
            
            # Plot iteration time
            if len(self.step_times) >= len(steps):
                iter_times = self.step_times[:len(steps)]
                throughputs = self.throughput[:len(steps)]
                
                # Create moving average
                window = min(20, len(iter_times))
                iter_times_smooth = np.convolve(
                    iter_times, 
                    np.ones(window) / window, 
                    mode='valid'
                ) * 1000  # Convert to ms
                
                throughput_smooth = np.convolve(
                    throughputs, 
                    np.ones(window) / window, 
                    mode='valid'
                )
                
                # Plot smoothed iteration time
                plt.subplot(2, 1, 2)
                plt.plot(steps[window-1:], iter_times_smooth, label='Iteration Time (ms)')
                plt.xlabel('Training Step')
                plt.ylabel('Time (ms)')
                plt.title(f'{model_name} Iteration Time During Training')
                plt.grid(True)
                
                # Add throughput as second axis
                ax2 = plt.gca().twinx()
                ax2.plot(steps[window-1:], throughput_smooth, 'r-', label='Throughput')
                ax2.set_ylabel('Samples/second', color='r')
                ax2.tick_params(axis='y', labelcolor='r')
                
                # Add both legends
                lines1, labels1 = plt.gca().get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.log_dir, f"{model_name}_training_profile.png"))
            plt.close()


class FlopsCalculator:
    """
    Utility for calculating FLOPs (Floating Point Operations) for neural networks
    
    This class provides methods for estimating the computational complexity
    of neural network models in terms of FLOPs.
    
    Args:
        model (torch.nn.Module): PyTorch model
        input_shape (Tuple): Input shape for the model (including batch dimension)
    """
    
    def __init__(self, model: torch.nn.Module, input_shape: Tuple):
        self.model = model
        self.input_shape = input_shape
        self.flops_per_module = {}
        self.total_flops = 0
    
    def calculate_flops(self) -> Dict[str, Union[int, Dict[str, int]]]:
        """
        Calculate FLOPs for the model
        
        Returns:
            Dict[str, Union[int, Dict[str, int]]]: FLOPs statistics
        """
        # Create input tensor
        input_tensor = torch.randn(self.input_shape)
        
        # Dictionary to track tensor shapes
        tensor_shapes = {}
        
        # Register hooks to capture input and output shapes
        handles = []
        
        def pre_hook(name):
            def hook(module, input):
                if input:
                    tensor_shapes[name + "_input"] = [tuple(x.shape) for x in input if isinstance(x, torch.Tensor)]
                return None
            return hook
        
        def post_hook(name):
            def hook(module, input, output):
                if isinstance(output, torch.Tensor):
                    tensor_shapes[name + "_output"] = tuple(output.shape)
                elif isinstance(output, tuple) and all(isinstance(x, torch.Tensor) for x in output):
                    tensor_shapes[name + "_output"] = [tuple(x.shape) for x in output]
                return None
            return hook
        
        # Register hooks
        for name, module in self.model.named_modules():
            if name:  # Skip the root module
                handles.append(module.register_forward_pre_hook(pre_hook(name)))
                handles.append(module.register_forward_hook(post_hook(name)))
        
        # Forward pass to capture shapes
        with torch.no_grad():
            _ = self.model(input_tensor)
        
        # Remove hooks
        for handle in handles:
            handle.remove()
        
        # Calculate FLOPs for each module
        for name, module in self.model.named_modules():
            if name:
                module_flops = self._calculate_module_flops(module, name, tensor_shapes)
                if module_flops > 0:
                    self.flops_per_module[name] = module_flops
                    self.total_flops += module_flops
        
        # Sort modules by FLOPs
        sorted_modules = sorted(
            self.flops_per_module.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Compile results
        results = {
            "total_flops": self.total_flops,
            "total_gflops": self.total_flops / (10**9),
            "module_flops": dict(sorted_modules),
        }
        
        # Log summary
        logger.info(f"FLOPs Analysis:")
        logger.info(f"  Total FLOPs: {results['total_flops']:,}")
        logger.info(f"  Total GFLOPs: {results['total_gflops']:.4f}")
        logger.info(f"  Top 5 modules by FLOPs:")
        for i, (name, flops) in enumerate(sorted_modules[:5]):
            logger.info(f"    {i+1}. {name}: {flops:,} ({flops/self.total_flops:.2%})")
        
        return results
    
    def _calculate_module_flops(
        self, 
        module: torch.nn.Module, 
        name: str, 
        tensor_shapes: Dict[str, Any]
    ) -> int:
        """
        Calculate FLOPs for a specific module
        
        Args:
            module (torch.nn.Module): Module to analyze
            name (str): Module name
            tensor_shapes (Dict[str, Any]): Dictionary of tensor shapes
            
        Returns:
            int: Estimated FLOPs for the module
        """
        if not (name + "_input" in tensor_shapes and name + "_output" in tensor_shapes):
            return 0
        
        input_shapes = tensor_shapes[name + "_input"]
        output_shape = tensor_shapes[name + "_output"]
        
        # Handle different module types
        if isinstance(module, torch.nn.Conv2d):
            # FLOPs for Conv2d: (K_h * K_w * C_in * C_out * H_out * W_out) / groups
            if not input_shapes:
                return 0
                
            input_shape = input_shapes[0]
            if len(input_shape) != 4:
                return 0
                
            batch_size, in_channels, in_h, in_w = input_shape
            
            if not isinstance(output_shape, tuple) or len(output_shape) != 4:
                return 0
                
            out_channels = output_shape[1]
            out_h, out_w = output_shape[2], output_shape[3]
            
            kernel_h, kernel_w = module.kernel_size
            groups = module.groups
            
            # Each output element requires (kernel_h * kernel_w * in_channels / groups) multiplications
            # and (kernel_h * kernel_w * in_channels / groups - 1) additions
            flops_per_element = 2 * kernel_h * kernel_w * in_channels * out_channels / groups
            total_flops = int(batch_size * out_h * out_w * flops_per_element)
            
            # Add bias if present
            if module.bias is not None:
                total_flops += batch_size * out_h * out_w * out_channels
            
            return total_flops
            
        elif isinstance(module, torch.nn.Linear):
            # FLOPs for Linear: 2 * in_features * out_features * batch_size
            if not input_shapes:
                return 0
                
            input_shape = input_shapes[0]
            if len(input_shape) < 2:
                return 0
                
            batch_size = input_shape[0]
            in_features = module.in_features
            out_features = module.out_features
            
            # Each output element requires in_features multiplications and in_features-1 additions
            flops_per_element = 2 * in_features * out_features
            total_flops = int(batch_size * flops_per_element)
            
            # Add bias if present
            if module.bias is not None:
                total_flops += batch_size * out_features
            
            return total_flops
            
        elif isinstance(module, torch.nn.BatchNorm2d):
            # FLOPs for BatchNorm2d: 2 * batch_size * channels * height * width
            if not input_shapes:
                return 0
                
            input_shape = input_shapes[0]
            if len(input_shape) != 4:
                return 0
                
            batch_size, channels, height, width = input_shape
            
            # Each element requires 2 operations (normalization and scale/shift)
            return int(2 * batch_size * channels * height * width)
            
        elif isinstance(module, torch.nn.ReLU) or isinstance(module, torch.nn.LeakyReLU):
            # FLOPs for ReLU: batch_size * elements (1 comparison per element)
            if not input_shapes:
                return 0
                
            input_shape = input_shapes[0]
            elements = 1
            for dim in input_shape:
                elements *= dim
            
            return int(elements)
            
        elif isinstance(module, torch.nn.MaxPool2d) or isinstance(module, torch.nn.AvgPool2d):
            # FLOPs for Pooling: batch_size * output_elements * kernel_size^2
            if not input_shapes:
                return 0
                
            input_shape = input_shapes[0]
            if len(input_shape) != 4:
                return 0
                
            batch_size = input_shape[0]
            channels = input_shape[1]
            
            if not isinstance(output_shape, tuple) or len(output_shape) != 4:
                return 0
                
            out_h, out_w = output_shape[2], output_shape[3]
            
            if isinstance(module.kernel_size, int):
                kernel_size = module.kernel_size ** 2
            else:
                kernel_size = module.kernel_size[0] * module.kernel_size[1]
            
            # Each output element requires kernel_size comparisons (MaxPool) or additions (AvgPool)
            return int(batch_size * channels * out_h * out_w * kernel_size)
        
        # Default: return 0 for unsupported module types
        return 0
    
    def generate_flops_report(self) -> str:
        """
        Generate detailed FLOPs report
        
        Returns:
            str: Path to saved report
        """
        # Calculate FLOPs
        flops_data = self.calculate_flops()
        
        # Add model parameters count
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        flops_data["total_params"] = total_params
        flops_data["trainable_params"] = trainable_params
        
        # Calculate FLOPs per parameter
        if total_params > 0:
            flops_data["flops_per_param"] = self.total_flops / total_params
        
        # Save report
        report_path = os.path.join(
            "./flops_reports", 
            f"flops_{self.model.__class__.__name__}_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, "w") as f:
            json.dump(flops_data, f, indent=2)
        
        logger.info(f"FLOPs report saved to {report_path}")
        
        # Generate visualization
        self._generate_flops_visualization(flops_data, report_path.replace(".json", ".png"))
        
        return report_path
    
    def _generate_flops_visualization(self, flops_data: Dict[str, Any], output_path: str) -> None:
        """
        Generate visualization of FLOPs distribution
        
        Args:
            flops_data (Dict[str, Any]): FLOPs data
            output_path (str): Path to save visualization
        """
        # Get top 10 modules by FLOPs
        module_flops = flops_data["module_flops"]
        sorted_modules = sorted(
            module_flops.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        top_n = 10
        top_modules = sorted_modules[:top_n]
        
        # Calculate other modules' total
        other_flops = sum(flops for _, flops in sorted_modules[top_n:])
        
        # Prepare data for pie chart
        if other_flops > 0:
            names = [name.split(".")[-1] for name, _ in top_modules] + ["Other"]
            values = [flops for _, flops in top_modules] + [other_flops]
        else:
            names = [name.split(".")[-1] for name, _ in top_modules]
            values = [flops for _, flops in top_modules]
        
        # Create figure
        plt.figure(figsize=(10, 12))
        
        # Create pie chart
        plt.subplot(2, 1, 1)
        explode = [0.1 if i == 0 else 0 for i in range(len(names))]
        plt.pie(
            values, 
            explode=explode,
            labels=names, 
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90
        )
        plt.axis('equal')
        plt.title(f'FLOPs Distribution ({flops_data["total_gflops"]:.2f} GFLOPs)')
        
        # Create bar chart
        plt.subplot(2, 1, 2)
        y_pos = range(len(names))
        plt.barh(y_pos, [v / 10**9 for v in values], align='center')
        plt.yticks(y_pos, names)
        plt.xlabel('GFLOPs')
        plt.title('Module Computational Complexity')
        
        # Add text with model details
        model_info = (
            f"Model: {self.model.__class__.__name__}\n"
            f"Total FLOPs: {flops_data['total_flops']:,}\n"
            f"Total GFLOPs: {flops_data['total_gflops']:.4f}\n"
            f"Total Parameters: {flops_data['total_params']:,}\n"
            f"Trainable Parameters: {flops_data['trainable_params']:,}\n"
        )
        
        plt.figtext(0.5, 0.01, model_info, ha='center', fontsize=10, bbox={"facecolor": "orange", "alpha": 0.2})
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.savefig(output_path)
        plt.close()
