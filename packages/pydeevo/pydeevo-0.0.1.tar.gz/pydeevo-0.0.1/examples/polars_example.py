"""
Example using Polars with PyDeevo for efficient data processing
"""
import torch
import polars as pl
import lightning as L
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
import numpy as np

from pydeevo.models.base import FlexibleModule
from pydeevo.utils.data import (
    PolarsDataProcessor, 
    DatasetBuilder, 
    handle_missing_values,
    normalize_features,
    create_polynomial_features
)
from pydeevo.utils.distributed import MemoryOptimization
from pydeevo.utils.profiling import ModelProfiler


def main():
    """Example of using Polars with PyDeevo"""
    print("Loading and preprocessing data with Polars...")
    
    # Load diabetes dataset
    diabetes = load_diabetes()
    feature_names = diabetes.feature_names
    
    # Create Polars DataFrame
    data = pl.DataFrame(
        {name: diabetes.data[:, i] for i, name in enumerate(feature_names)},
    )
    data = data.with_columns(pl.Series(name="target", values=diabetes.target))
    
    # Print DataFrame info
    print("Dataset Overview:")
    print(f"Shape: {data.shape}")
    print(f"Columns: {data.columns}")
    print(f"Sample data:")
    print(data.head())
    
    # Create data processor and dataset builder
    processor = PolarsDataProcessor(cache_dir="./data_cache")
    builder = DatasetBuilder(processor)
    
    # Define preprocessing steps
    preprocessing_steps = [
        handle_missing_values(strategy='mean'),  # Handle any missing values
        normalize_features(feature_names, method='z-score'),  # Normalize features
        create_polynomial_features(['bmi', 'bp'], degree=2)  # Create polynomial features
    ]
    
    # Create PyTorch datasets
    feature_cols = feature_names + ['bmi^2', 'bp^2', 'bmi_bp']
    train_dataset, val_dataset, test_dataset = builder.from_polars(
        data,
        feature_cols=feature_cols,
        target_col="target",
        val_ratio=0.2,
        test_ratio=0.1,
        preprocessing_steps=preprocessing_steps,
        cache_key="diabetes_processed"
    )
    
    print(f"Created datasets: train={len(train_dataset)}, val={len(val_dataset)}, test={len(test_dataset)} samples")
    
    # Create data loaders
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=32, shuffle=True
    )
    val_loader = torch.utils.data.DataLoader(
        val_dataset, batch_size=32, shuffle=False
    )
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=32, shuffle=False
    )
    
    # Create model
    input_size = len(feature_cols)
    model = FlexibleModule(
        architecture=[input_size, 64, 32, 1],
        learning_rate=0.01,
        optimizer_kwargs={'weight_decay': 1e-5},
        loss_fn=torch.nn.MSELoss()
    )
    
    # Profile the model
    print("Profiling model...")
    profiler = ModelProfiler(
        model,
        input_shape=(32, input_size),
        log_dir="./polars_example/profiles"
    )
    memory_stats = profiler.profile_memory_usage()
    inference_stats = profiler.profile_inference_time(num_warmup=5, num_runs=20)
    
    print(f"Model memory usage: {memory_stats['total_memory_mb']:.2f} MB")
    print(f"Inference time: {inference_stats['mean_ms']:.2f} ms")
    
    # Train model
    print("Training model...")
    trainer = L.Trainer(
        max_epochs=100,
        enable_progress_bar=True,
        log_every_n_steps=10,
        enable_model_summary=True,
    )
    
    trainer.fit(model, train_loader, val_loader)
    
    # Evaluate model
    results = trainer.test(model, test_loader)
    print(f"Test results: {results}")
    
    # Make predictions and visualize results
    print("Making predictions...")
    model.eval()
    predictions = []
    targets = []
    
    with torch.no_grad():
        for batch in test_loader:
            features, target = batch
            output = model(features)
            predictions.extend(output.squeeze().cpu().numpy())
            targets.extend(target.squeeze().cpu().numpy())
    
    # Plot predictions vs targets
    plt.figure(figsize=(10, 6))
    plt.scatter(targets, predictions, alpha=0.5)
    
    # Add perfect prediction line
    min_val = min(min(targets), min(predictions))
    max_val = max(max(targets), max(predictions))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')
    
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Actual vs Predicted Values')
    plt.grid(True)
    
    plt.savefig("./polars_example/predictions.png")
    print("Results saved to ./polars_example/predictions.png")


if __name__ == "__main__":
    main()
