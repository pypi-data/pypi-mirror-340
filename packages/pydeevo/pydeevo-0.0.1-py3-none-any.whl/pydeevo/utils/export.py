"""
Export and inference utilities for optimized model deployment
"""
import os
import time
import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

import torch
import numpy as np
import onnx
from safetensors.torch import save_file

logger = logging.getLogger(__name__)


class ModelExporter:
    """
    Utility for exporting PyTorch models to different formats
    
    This class provides methods for exporting models to formats like ONNX,
    TorchScript, and safetensors for deployment.
    
    Args:
        model (torch.nn.Module): PyTorch model to export
        input_shape (Tuple): Input shape for the model (including batch dimension)
        output_dir (str, optional): Directory to save exported models. Defaults to "./exported_models".
        export_name (str, optional): Base name for exported files. Defaults to None.
    """
    
    def __init__(
        self, 
        model: torch.nn.Module, 
        input_shape: Tuple,
        output_dir: str = "./exported_models",
        export_name: Optional[str] = None
    ):
        self.model = model
        self.input_shape = input_shape
        self.output_dir = output_dir
        self.export_name = export_name or model.__class__.__name__
        
        os.makedirs(output_dir, exist_ok=True)
    
    def export_to_torchscript(
        self, 
        method: str = "trace",
        optimize: bool = True,
        use_dynamo: bool = False,
    ) -> str:
        """
        Export model to TorchScript format
        
        Args:
            method (str, optional): Method to use ('trace' or 'script'). Defaults to "trace".
            optimize (bool, optional): Whether to optimize the model. Defaults to True.
            use_dynamo (bool, optional): Whether to use torch.dynamo. Defaults to False.
            
        Returns:
            str: Path to exported model
        """
        logger.info(f"Exporting model to TorchScript using {method} method...")
        
        # Set model to eval mode
        model = self.model.to("cpu").eval()
        
        # Create input tensor
        example_input = torch.randn(self.input_shape)
        
        # Export using specified method
        if method == "trace":
            with torch.no_grad():
                traced_model = torch.jit.trace(model, example_input)
        elif method == "script":
            scripted_model = torch.jit.script(model)
        else:
            raise ValueError(f"Unknown export method: {method}. Use 'trace' or 'script'.")
        
        # Apply optimizations if requested
        exported_model = traced_model if method == "trace" else scripted_model
        
        if optimize:
            exported_model = torch.jit.optimize_for_inference(exported_model)
        
        # Use dynamo if requested (PyTorch 2.0+ feature)
        if use_dynamo and hasattr(torch, 'dynamo'):
            try:
                exported_model = torch.dynamo.optimize()(exported_model)
                logger.info("Applied torch.dynamo optimization")
            except Exception as e:
                logger.warning(f"Failed to apply torch.dynamo: {e}")
        
        # Save model
        output_path = os.path.join(self.output_dir, f"{self.export_name}_torchscript.pt")
        exported_model.save(output_path)
        
        logger.info(f"TorchScript model saved to {output_path}")
        return output_path
    
    def export_to_onnx(
        self, 
        opset_version: int = 17,
        dynamic_axes: Optional[Dict[str, Dict[int, str]]] = None,
        simplify: bool = True,
    ) -> str:
        """
        Export model to ONNX format
        
        Args:
            opset_version (int, optional): ONNX opset version. Defaults to 17.
            dynamic_axes (Optional[Dict[str, Dict[int, str]]], optional): Dynamic axes configuration.
                Defaults to None.
            simplify (bool, optional): Whether to simplify the model. Defaults to True.
            
        Returns:
            str: Path to exported model
        """
        try:
            import onnxsim
        except ImportError:
            logger.warning("onnx-simplifier not installed. Will not simplify ONNX model.")
            simplify = False
        
        logger.info(f"Exporting model to ONNX (opset {opset_version})...")
        
        # Set model to eval mode
        model = self.model.to("cpu").eval()
        
        # Create input tensor
        example_input = torch.randn(self.input_shape)
        
        # Set up dynamic axes if not provided
        if dynamic_axes is None:
            # By default, only the batch dimension (0) is dynamic
            dynamic_axes = {
                'input': {0: 'batch_size'},
                'output': {0: 'batch_size'}
            }
        
        # Export to ONNX
        output_path = os.path.join(self.output_dir, f"{self.export_name}.onnx")
        
        torch.onnx.export(
            model,
            example_input,
            output_path,
            verbose=False,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes=dynamic_axes,
            opset_version=opset_version,
            do_constant_folding=True,
            export_params=True,
        )
        
        # Simplify ONNX model if requested
        if simplify:
            try:
                logger.info("Simplifying ONNX model...")
                model_onnx = onnx.load(output_path)
                model_simp, check = onnxsim.simplify(model_onnx)
                
                if check:
                    onnx.save(model_simp, output_path)
                    logger.info("Simplified ONNX model saved")
                else:
                    logger.warning("ONNX simplification failed verification, using original model")
            except Exception as e:
                logger.warning(f"ONNX simplification failed: {e}")
        
        logger.info(f"ONNX model saved to {output_path}")
        return output_path
    
    def export_to_safetensors(self) -> str:
        """
        Export model weights to safetensors format
        
        Returns:
            str: Path to exported weights
        """
        logger.info("Exporting model weights to safetensors format...")
        
        # Set model to eval mode
        model = self.model.to("cpu").eval()
        
        # Get state dict
        state_dict = model.state_dict()
        
        # Save using safetensors
        output_path = os.path.join(self.output_dir, f"{self.export_name}.safetensors")
        save_file(state_dict, output_path)
        
        logger.info(f"Model weights saved to {output_path}")
        return output_path
    
    def export_all_formats(self) -> Dict[str, str]:
        """
        Export model to all supported formats
        
        Returns:
            Dict[str, str]: Dictionary mapping format names to file paths
        """
        export_paths = {}
        
        try:
            # Export to TorchScript
            export_paths['torchscript'] = self.export_to_torchscript()
            
            # Export to ONNX
            export_paths['onnx'] = self.export_to_onnx()
            
            # Export to safetensors
            export_paths['safetensors'] = self.export_to_safetensors()
            
            # Create model info file
            model_info = {
                'model_name': self.model.__class__.__name__,
                'input_shape': list(self.input_shape),
                'parameter_count': sum(p.numel() for p in self.model.parameters()),
                'export_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'export_paths': export_paths,
            }
            
            info_path = os.path.join(self.output_dir, f"{self.export_name}_info.json")
            with open(info_path, 'w') as f:
                json.dump(model_info, f, indent=2)
            
            export_paths['info'] = info_path
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise
        
        logger.info(f"Model exported in all formats to {self.output_dir}")
        return export_paths


class InferenceProfiler:
    """
    Utility for profiling inference performance across different formats
    
    This class provides methods for benchmarking models in different formats
    to compare inference speed.
    
    Args:
        input_shape (Tuple): Input shape for the model (including batch dimension)
        output_dir (str, optional): Directory for exports and reports. Defaults to "./inference_profiles".
        device (str, optional): Device to run profiling on. Defaults to "cuda" if available.
    """
    
    def __init__(
        self, 
        input_shape: Tuple,
        output_dir: str = "./inference_profiles",
        device: Optional[str] = None,
    ):
        self.input_shape = input_shape
        self.output_dir = output_dir
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        os.makedirs(output_dir, exist_ok=True)
    
    def profile_pytorch_model(
        self, 
        model: torch.nn.Module,
        num_warmup: int = 10,
        num_iters: int = 100,
    ) -> Dict[str, float]:
        """
        Profile inference of PyTorch model
        
        Args:
            model (torch.nn.Module): PyTorch model
            num_warmup (int, optional): Number of warmup iterations. Defaults to 10.
            num_iters (int, optional): Number of measured iterations. Defaults to 100.
            
        Returns:
            Dict[str, float]: Inference time statistics
        """
        logger.info(f"Profiling PyTorch model inference...")
        
        # Set model to eval mode and move to device
        model = model.to(self.device).eval()
        
        # Create input tensor
        input_tensor = torch.randn(self.input_shape, device=self.device)
        
        # Warmup
        with torch.no_grad():
            for _ in range(num_warmup):
                _ = model(input_tensor)
        
        # Synchronize before timing
        if self.device == "cuda":
            torch.cuda.synchronize()
        
        # Measure inference time
        times = []
        with torch.no_grad():
            for _ in range(num_iters):
                start_time = time.time()
                _ = model(input_tensor)
                
                if self.device == "cuda":
                    torch.cuda.synchronize()
                    
                end_time = time.time()
                times.append((end_time - start_time) * 1000)  # ms
        
        # Calculate statistics
        times = np.array(times)
        stats = {
            "mean_ms": float(np.mean(times)),
            "median_ms": float(np.median(times)),
            "min_ms": float(np.min(times)),
            "max_ms": float(np.max(times)),
            "p95_ms": float(np.percentile(times, 95)),
            "throughput": float(self.input_shape[0] / (np.mean(times) / 1000)),
        }
        
        logger.info(f"PyTorch model inference: {stats['mean_ms']:.2f}ms (±{np.std(times):.2f}ms)")
        return stats
    
    def profile_torchscript_model(
        self, 
        model_path: str,
        num_warmup: int = 10,
        num_iters: int = 100,
    ) -> Dict[str, float]:
        """
        Profile inference of TorchScript model
        
        Args:
            model_path (str): Path to TorchScript model
            num_warmup (int, optional): Number of warmup iterations. Defaults to 10.
            num_iters (int, optional): Number of measured iterations. Defaults to 100.
            
        Returns:
            Dict[str, float]: Inference time statistics
        """
        logger.info(f"Profiling TorchScript model inference...")
        
        # Load model
        model = torch.jit.load(model_path).to(self.device).eval()
        
        # Create input tensor
        input_tensor = torch.randn(self.input_shape, device=self.device)
        
        # Warmup
        with torch.no_grad():
            for _ in range(num_warmup):
                _ = model(input_tensor)
        
        # Synchronize before timing
        if self.device == "cuda":
            torch.cuda.synchronize()
        
        # Measure inference time
        times = []
        with torch.no_grad():
            for _ in range(num_iters):
                start_time = time.time()
                _ = model(input_tensor)
                
                if self.device == "cuda":
                    torch.cuda.synchronize()
                    
                end_time = time.time()
                times.append((end_time - start_time) * 1000)  # ms
        
        # Calculate statistics
        times = np.array(times)
        stats = {
            "mean_ms": float(np.mean(times)),
            "median_ms": float(np.median(times)),
            "min_ms": float(np.min(times)),
            "max_ms": float(np.max(times)),
            "p95_ms": float(np.percentile(times, 95)),
            "throughput": float(self.input_shape[0] / (np.mean(times) / 1000)),
        }
        
        logger.info(f"TorchScript model inference: {stats['mean_ms']:.2f}ms (±{np.std(times):.2f}ms)")
        return stats
    
    def profile_onnx_model(
        self, 
        model_path: str,
        num_warmup: int = 10,
        num_iters: int = 100,
        provider: str = 'auto',
    ) -> Dict[str, float]:
        """
        Profile inference of ONNX model
        
        Args:
            model_path (str): Path to ONNX model
            num_warmup (int, optional): Number of warmup iterations. Defaults to 10.
            num_iters (int, optional): Number of measured iterations. Defaults to 100.
            provider (str, optional): ONNX Runtime execution provider. 
                Defaults to 'auto' (selects based on device).
            
        Returns:
            Dict[str, float]: Inference time statistics
        """
        try:
            import onnxruntime as ort
        except ImportError:
            logger.error("onnxruntime not installed. Cannot profile ONNX model.")
            return {"error": "onnxruntime not installed"}
        
        logger.info(f"Profiling ONNX model inference...")
        
        # Select provider
        if provider == 'auto':
            if self.device == 'cuda' and 'CUDAExecutionProvider' in ort.get_available_providers():
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            else:
                providers = ['CPUExecutionProvider']
        else:
            providers = [provider]
        
        # Create session
        session_options = ort.SessionOptions()
        session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        session = ort.InferenceSession(model_path, providers=providers, sess_options=session_options)
        
        # Get input name
        input_name = session.get_inputs()[0].name
        
        # Create input tensor as numpy array
        input_numpy = np.random.randn(*self.input_shape).astype(np.float32)
        
        # Warmup
        for _ in range(num_warmup):
            _ = session.run(None, {input_name: input_numpy})
        
        # Measure inference time
        times = []
        for _ in range(num_iters):
            start_time = time.time()
            _ = session.run(None, {input_name: input_numpy})
            end_time = time.time()
            times.append((end_time - start_time) * 1000)  # ms
        
        # Calculate statistics
        times = np.array(times)
        stats = {
            "mean_ms": float(np.mean(times)),
            "median_ms": float(np.median(times)),
            "min_ms": float(np.min(times)),
            "max_ms": float(np.max(times)),
            "p95_ms": float(np.percentile(times, 95)),
            "throughput": float(self.input_shape[0] / (np.mean(times) / 1000)),
            "provider": providers[0],
        }
        
        logger.info(f"ONNX model inference: {stats['mean_ms']:.2f}ms (±{np.std(times):.2f}ms)")
        return stats
    
    def compare_formats(
        self,
        pytorch_model: torch.nn.Module,
        export_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Compare inference performance across different formats
        
        Args:
            pytorch_model (torch.nn.Module): PyTorch model
            export_name (Optional[str], optional): Base name for exports. Defaults to None.
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        # Export model in different formats
        exporter = ModelExporter(
            pytorch_model, 
            self.input_shape, 
            self.output_dir,
            export_name
        )
        
        export_paths = exporter.export_all_formats()
        
        # Profile each format
        results = {
            "pytorch": self.profile_pytorch_model(pytorch_model),
            "torchscript": self.profile_torchscript_model(export_paths["torchscript"]),
            "onnx": self.profile_onnx_model(export_paths["onnx"]),
        }
        
        # Calculate speedups
        pytorch_time = results["pytorch"]["mean_ms"]
        
        for fmt in ["torchscript", "onnx"]:
            if "error" not in results[fmt]:
                speedup = pytorch_time / results[fmt]["mean_ms"]
                results[fmt]["speedup"] = float(speedup)
        
        # Create comparison summary
        summary = {
            "input_shape": list(self.input_shape),
            "device": self.device,
            "export_paths": export_paths,
            "results": results,
        }
        
        # Save summary
        summary_path = os.path.join(
            self.output_dir, 
            f"inference_comparison_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        logger.info("Inference Performance Comparison:")
        logger.info(f"  PyTorch:     {results['pytorch']['mean_ms']:.2f}ms")
        
        if "error" not in results["torchscript"]:
            logger.info(f"  TorchScript: {results['torchscript']['mean_ms']:.2f}ms "
                       f"({results['torchscript']['speedup']:.2f}x speedup)")
        
        if "error" not in results["onnx"]:
            logger.info(f"  ONNX:        {results['onnx']['mean_ms']:.2f}ms "
                       f"({results['onnx']['speedup']:.2f}x speedup)")
        
        logger.info(f"Comparison saved to {summary_path}")
        
        return summary


class InferenceOptimizer:
    """
    Utility for optimizing model inference
    
    This class provides methods for optimizing models for inference,
    including quantization, fusion, and other techniques.
    
    Args:
        model (torch.nn.Module): PyTorch model to optimize
        input_shape (Tuple): Input shape for the model (including batch dimension)
        output_dir (str, optional): Directory for optimized models. Defaults to "./optimized_models".
    """
    
    def __init__(
        self, 
        model: torch.nn.Module, 
        input_shape: Tuple,
        output_dir: str = "./optimized_models",
    ):
        self.model = model
        self.input_shape = input_shape
        self.output_dir = output_dir
        
        os.makedirs(output_dir, exist_ok=True)
    
    def optimize_for_inference(
        self,
        optimize_memory_format: bool = True,
        apply_fusion: bool = True,
    ) -> torch.nn.Module:
        """
        Optimize model for inference
        
        Args:
            optimize_memory_format (bool, optional): Whether to optimize memory format. 
                Defaults to True.
            apply_fusion (bool, optional): Whether to apply operator fusion. 
                Defaults to True.
            
        Returns:
            torch.nn.Module: Optimized model
        """
        logger.info("Optimizing model for inference...")
        
        # Set model to eval mode
        model = self.model.eval()
        
        # Create a copy of the model to avoid modifying the original
        optimized_model = type(model)(*model.__init_args__, **model.__init_kwargs__)
        optimized_model.load_state_dict(model.state_dict())
        optimized_model.eval()
        
        # Optimize memory format if requested
        if optimize_memory_format and torch.cuda.is_available():
            logger.info("Optimizing memory format...")
            optimized_model = optimized_model.to(memory_format=torch.channels_last)
        
        # Apply fusion if requested and PyTorch version supports it
        if apply_fusion and hasattr(torch.jit, 'optimize_for_inference'):
            logger.info("Applying operator fusion...")
            
            # Create example input
            example_input = torch.randn(self.input_shape)
            
            # Trace and optimize
            with torch.no_grad():
                traced_model = torch.jit.trace(optimized_model, example_input)
                optimized_traced = torch.jit.optimize_for_inference(traced_model)
                
                # Convert back to regular PyTorch model (if possible)
                try:
                    # This is a bit of a hack - we try to recover a pure PyTorch model
                    # But this might not always be possible, so we fall back to the traced version
                    # pylint: disable=protected-access
                    optimized_model = torch.jit._recursive.wrap_cpp_module(optimized_traced._c)._c._get_method('forward')._get_optimized_graph_module()
                except:
                    # Fall back to traced model
                    optimized_model = optimized_traced
        
        logger.info("Model optimization complete")
        return optimized_model
    
    def quantize_model(
        self,
        quantization_type: str = "dynamic",
        dtype: torch.dtype = torch.qint8,
    ) -> torch.nn.Module:
        """
        Quantize model for reduced memory and faster inference
        
        Args:
            quantization_type (str, optional): Type of quantization 
                ('dynamic', 'static', or 'aware'). Defaults to "dynamic".
            dtype (torch.dtype, optional): Quantization data type. 
                Defaults to torch.qint8.
            
        Returns:
            torch.nn.Module: Quantized model
        """
        logger.info(f"Quantizing model using {quantization_type} quantization...")
        
        if not hasattr(torch, 'quantization'):
            logger.error("Quantization not supported in this PyTorch version")
            return self.model
        
        # Set model to eval mode
        model = self.model.to('cpu').eval()
        
        if quantization_type == "dynamic":
            # Dynamic quantization
            quantized_model = torch.quantization.quantize_dynamic(
                model,
                {torch.nn.Linear, torch.nn.LSTM, torch.nn.GRU},
                dtype=dtype
            )
        elif quantization_type == "static":
            # Static quantization requires calibration
            # This is simplified - real static quantization needs more preparation
            from torch.quantization import get_default_qconfig, quantize_jit
            
            # Create example input
            example_input = torch.randn(self.input_shape)
            
            # Trace and quantize
            traced_model = torch.jit.trace(model, example_input)
            
            # Configure quantization
            qconfig = get_default_qconfig("fbgemm")
            
            # Quantize model
            quantized_model = quantize_jit(
                traced_model,
                {"": qconfig},
                example_input
            )
        elif quantization_type == "aware":
            # QAT requires training - we'll just log a warning
            logger.warning("Quantization-aware training requires training the model with quantization")
            return model
        else:
            logger.error(f"Unknown quantization type: {quantization_type}")
            return model
        
        # Save quantized model
        output_path = os.path.join(self.output_dir, f"{model.__class__.__name__}_quantized_{quantization_type}.pt")
        torch.jit.save(torch.jit.script(quantized_model), output_path)
        
        logger.info(f"Quantized model saved to {output_path}")
        return quantized_model
    
    def benchmark_optimized_models(
        self,
        num_warmup: int = 10,
        num_iters: int = 100,
    ) -> Dict[str, Dict[str, float]]:
        """
        Benchmark different optimization techniques
        
        Args:
            num_warmup (int, optional): Number of warmup iterations. Defaults to 10.
            num_iters (int, optional): Number of measured iterations. Defaults to 100.
            
        Returns:
            Dict[str, Dict[str, float]]: Benchmark results
        """
        results = {}
        
        # Benchmark original model
        logger.info("Benchmarking original model...")
        original_model = self.model.to('cpu').eval()
        results["original"] = self._benchmark_model(original_model, num_warmup, num_iters)
        
        # Benchmark inference-optimized model
        logger.info("Benchmarking inference-optimized model...")
        optimized_model = self.optimize_for_inference()
        results["optimized"] = self._benchmark_model(optimized_model, num_warmup, num_iters)
        
        # Benchmark quantized model
        try:
            logger.info("Benchmarking quantized model...")
            quantized_model = self.quantize_model()
            results["quantized"] = self._benchmark_model(quantized_model, num_warmup, num_iters)
        except Exception as e:
            logger.warning(f"Quantization failed: {e}")
            results["quantized"] = {"error": str(e)}
        
        # Save results
        output_path = os.path.join(self.output_dir, f"optimization_benchmark_{time.strftime('%Y%m%d_%H%M%S')}.json")
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Benchmark results saved to {output_path}")
        return results
    
    def _benchmark_model(
        self, 
        model: torch.nn.Module,
        num_warmup: int,
        num_iters: int,
    ) -> Dict[str, float]:
        """
        Benchmark a specific model
        
        Args:
            model (torch.nn.Module): Model to benchmark
            num_warmup (int): Number of warmup iterations
            num_iters (int): Number of measured iterations
            
        Returns:
            Dict[str, float]: Benchmark results
        """
        # Move model to CPU for consistent comparison
        model = model.to('cpu').eval()
        
        # Create input tensor
        input_tensor = torch.randn(self.input_shape)
        
        # Warmup
        with torch.no_grad():
            for _ in range(num_warmup):
                _ = model(input_tensor)
        
        # Measure inference time
        times = []
        with torch.no_grad():
            for _ in range(num_iters):
                start_time = time.time()
                _ = model(input_tensor)
                end_time = time.time()
                times.append((end_time - start_time) * 1000)  # ms
        
        # Calculate statistics
        times = np.array(times)
        stats = {
            "mean_ms": float(np.mean(times)),
            "median_ms": float(np.median(times)),
            "min_ms": float(np.min(times)),
            "max_ms": float(np.max(times)),
            "p95_ms": float(np.percentile(times, 95)),
            "throughput": float(self.input_shape[0] / (np.mean(times) / 1000)),
        }
        
        # Calculate model size
        size_bytes = 0
        for param in model.parameters():
            size_bytes += param.nelement() * param.element_size()
        
        stats["model_size_mb"] = float(size_bytes / (1024 * 1024))
        
        return stats
