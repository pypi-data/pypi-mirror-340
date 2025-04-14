"""
Example showing advanced distributed training with PyDeevo
"""
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
import lightning as L

from pydeevo import PyDeevo
from pydeevo.models.base import CNNModule
from pydeevo.utils.distributed import DistributedTrainingHelper, MemoryOptimization
from pydeevo.utils.profiling import ModelProfiler, FlopsCalculator
from pydeevo.utils.export import ModelExporter, InferenceProfiler


def main():
    """Advanced distributed training example"""
    # Set up PyDeevo
    pydeevo = PyDeevo(base_dir="./distributed_example")
    
    # Load CIFAR-10 dataset
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    
    train_dataset = torchvision.datasets.CIFAR10('./data', train=True, download=True, transform=transform_train)
    test_dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=transform_test)
    
    # Split training dataset into train and validation
    train_size = int(0.8 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(train_dataset, [train_size, val_size])
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64)
    test_loader = DataLoader(test_dataset, batch_size=64)
    
    # Define CNN architecture
    input_shape = (3, 32, 32)  # CIFAR-10 images (channels, height, width)
    output_size = 10  # 10 classes
    
    # Define a CNN architecture manually
    conv_architecture = [
        {'filters': 32, 'kernel_size': 3, 'pool_size': 2},
        {'filters': 64, 'kernel_size': 3, 'pool_size': 2},
        {'filters': 128, 'kernel_size': 3, 'pool_size': 2},
    ]
    
    fc_architecture = [512, 128, output_size]
    
    # Create the model
    model = CNNModule(
        conv_architecture=conv_architecture,
        fc_architecture=fc_architecture,
        input_shape=input_shape,
        learning_rate=0.001
    )
    
    print("Model created. Now setting up distributed training...")
    
    # Set up distributed training helper
    dist_helper = DistributedTrainingHelper(
        model_size_gb=0.1,  # Small model, approximate size in GB
        precision='16-mixed',
        devices='auto',
        strategy='auto',
        checkpoint_dir="./distributed_example/checkpoints",
        mixed_precision=True
    )
    
    # Profile the model's memory usage and FLOPs
    print("Profiling the model...")
    batch_size = train_loader.batch_size
    input_shape_with_batch = (batch_size,) + input_shape
    
    memory_optimizer = MemoryOptimization()
    memory_stats = memory_optimizer.print_model_memory_usage(model, input_shape_with_batch)
    
    flops_calculator = FlopsCalculator(model, input_shape_with_batch)
    flops_stats = flops_calculator.calculate_flops()
    
    print(f"Model has {flops_stats['total_gflops']:.2f} GFLOPs and uses {memory_stats['total_memory_mb']:.2f} MB of memory")
    
    # Apply memory optimizations
    optimized_model = memory_optimizer.optimize_memory_usage(
        model, 
        use_channels_last=True,
        use_compile=True,
        use_activation_checkpointing=False
    )
    
    # Set up Fabric for distributed training
    print("Setting up Lightning Fabric for distributed training...")
    transformer_modules = [nn.Conv2d, nn.Linear]  # Modules that can be wrapped for distributed training
    
    fabric = dist_helper.setup_fabric(transformer_modules)
    
    # Set up optimizer
    optimizer_fn = lambda params: torch.optim.Adam(params, lr=0.001)
    
    # Set up model and optimizer with Fabric
    model, optimizer = dist_helper.setup_model_and_optimizer(optimized_model, optimizer_fn)
    
    # Prepare data loaders with Fabric
    train_loader = fabric.setup_dataloaders(train_loader)
    val_loader = fabric.setup_dataloaders(val_loader)
    test_loader = fabric.setup_dataloaders(test_loader)
    
    print("Starting distributed training...")
    
    # Training loop
    num_epochs = 10
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            # Forward pass
            output = model(data)
            loss = F.cross_entropy(output, target)
            
            # Backward pass and optimize
            fabric.backward(loss)
            optimizer.step()
            optimizer.zero_grad()
            
            # Update metrics
            train_loss += loss.item()
            
            # Calculate accuracy
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            # Print progress
            if batch_idx % 50 == 0:
                fabric.print(f"Epoch: {epoch+1}/{num_epochs}, Batch: {batch_idx}/{len(train_loader)}, "
                      f"Loss: {train_loss/(batch_idx+1):.4f}, "
                      f"Acc: {100.*correct/total:.2f}%")
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(val_loader):
                # Forward pass
                output = model(data)
                loss = F.cross_entropy(output, target)
                
                # Update metrics
                val_loss += loss.item()
                
                # Calculate accuracy
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        # Print epoch results
        fabric.print(f"Epoch: {epoch+1}/{num_epochs}, "
              f"Train Loss: {train_loss/len(train_loader):.4f}, "
              f"Val Loss: {val_loss/len(val_loader):.4f}, "
              f"Val Acc: {100.*correct/total:.2f}%")
        
        # Save checkpoint
        if epoch % 2 == 0:
            metrics = {
                "epoch": epoch,
                "train_loss": train_loss/len(train_loader),
                "val_loss": val_loss/len(val_loader),
                "val_acc": correct/total
            }
            
            dist_helper.save_model_checkpoint(
                model, 
                optimizer, 
                epoch, 
                metrics,
                f"model_epoch_{epoch:03d}.pt",
                save_with_safetensors=True
            )
    
    # Test the model
    print("Testing the model...")
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(test_loader):
            # Forward pass
            output = model(data)
            loss = F.cross_entropy(output, target)
            
            # Update metrics
            test_loss += loss.item()
            
            # Calculate accuracy
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
    
    print(f"Test Loss: {test_loss/len(test_loader):.4f}, Test Acc: {100.*correct/total:.2f}%")
    
    # Export the model
    print("Exporting the model...")
    # Move model to CPU for export
    cpu_model = CNNModule(
        conv_architecture=conv_architecture,
        fc_architecture=fc_architecture,
        input_shape=input_shape,
        learning_rate=0.001
    )
    
    # Load the trained weights (assume we load from the last checkpoint)
    last_checkpoint = os.path.join("./distributed_example/checkpoints", f"model_epoch_{num_epochs-1:03d}.pt")
    if os.path.exists(last_checkpoint):
        state_dict = torch.load(last_checkpoint)["model"]
        cpu_model.load_state_dict(state_dict)
    else:
        # Just for demo purposes if no checkpoint exists
        cpu_model.load_state_dict(model.state_dict())
    
    cpu_model = cpu_model.to("cpu").eval()
    
    # Export to different formats
    exporter = ModelExporter(
        cpu_model, 
        (1,) + input_shape,  # Use batch size 1 for export
        output_dir="./distributed_example/exported_models"
    )
    
    export_paths = exporter.export_all_formats()
    print(f"Model exported to: {export_paths}")
    
    # Profile inference performance
    print("Profiling inference performance...")
    inference_profiler = InferenceProfiler(
        (1,) + input_shape,  # Use batch size 1 for inference
        output_dir="./distributed_example/inference_profiles"
    )
    
    comparison_results = inference_profiler.compare_formats(cpu_model)
    print(f"Inference comparison results saved to: {comparison_results}")
    
    print("Distributed training example completed!")


if __name__ == "__main__":
    main()
