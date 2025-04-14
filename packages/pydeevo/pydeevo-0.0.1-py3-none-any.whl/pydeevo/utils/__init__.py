"""
PyDeevo utilities module initialization
"""
from .helpers import (
    setup_logging,
    get_device,
    save_dict_to_json,
    load_dict_from_json,
    plot_search_progress,
    visualize_architecture_comparison,
    calculate_model_complexity
)

from .profiling import (
    ModelProfiler,
    ArchitectureBenchmarker,
    LightningProfileCallback,
    FlopsCalculator
)

from .distributed import (
    DistributedTrainingHelper,
    MemoryOptimization,
    ModelShardingHelper,
    BatchSizeOptimizer,
    SecurityWrapper
)

from .export import (
    ModelExporter,
    InferenceProfiler,
    InferenceOptimizer
)

from .data import (
    PolarsDataProcessor,
    PolarsDataset,
    DatasetBuilder,
    handle_missing_values,
    encode_categorical,
    normalize_features,
    create_polynomial_features
)

from .database import (
    DuckDBManager,
    SQLDataProcessor,
    AnalyticalDataManager,
    DuckDBDataset,
    sql_to_pytorch_dataset,
    execute_analytical_query,
    etl_pipeline
)

__all__ = [
    # From helpers
    'setup_logging',
    'get_device',
    'save_dict_to_json',
    'load_dict_from_json',
    'plot_search_progress',
    'visualize_architecture_comparison',
    'calculate_model_complexity',
    
    # From profiling
    'ModelProfiler',
    'ArchitectureBenchmarker',
    'LightningProfileCallback',
    'FlopsCalculator',
    
    # From distributed
    'DistributedTrainingHelper',
    'MemoryOptimization',
    'ModelShardingHelper',
    'BatchSizeOptimizer',
    'SecurityWrapper',
    
    # From export
    'ModelExporter',
    'InferenceProfiler',
    'InferenceOptimizer',
    
    # From data
    'PolarsDataProcessor',
    'PolarsDataset',
    'DatasetBuilder',
    'handle_missing_values',
    'encode_categorical',
    'normalize_features',
    'create_polynomial_features',
    
    # From database
    'DuckDBManager',
    'SQLDataProcessor',
    'AnalyticalDataManager',
    'DuckDBDataset',
    'sql_to_pytorch_dataset',
    'execute_analytical_query',
    'etl_pipeline'
]
