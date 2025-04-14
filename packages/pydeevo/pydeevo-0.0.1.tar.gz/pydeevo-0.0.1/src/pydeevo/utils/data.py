"""
Data handling utilities using Polars for high-performance DataFrame operations
"""
import os
import logging
import json
from typing import Dict, List, Any, Optional, Union, Tuple, Callable, Iterable

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import polars as pl

logger = logging.getLogger(__name__)


class PolarsDataProcessor:
    """
    Utility for efficient data preprocessing using Polars
    
    This class provides methods for loading, transforming and analyzing data
    using the high-performance Polars library.
    
    Args:
        cache_dir (str, optional): Directory to cache processed data. Defaults to "./data_cache".
    """
    
    def __init__(self, cache_dir: str = "./data_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def load_data(
        self, 
        path: str, 
        file_type: Optional[str] = None,
        **kwargs
    ) -> pl.DataFrame:
        """
        Load data from various file formats into a Polars DataFrame
        
        Args:
            path (str): Path to the data file
            file_type (Optional[str], optional): File type override. Defaults to None (autodetect).
            **kwargs: Additional arguments to pass to the reader
            
        Returns:
            pl.DataFrame: Loaded data
        """
        # Determine file type if not provided
        if file_type is None:
            file_ext = os.path.splitext(path)[1].lower()
            if file_ext in ['.csv', '.txt']:
                file_type = 'csv'
            elif file_ext in ['.parquet', '.pq']:
                file_type = 'parquet'
            elif file_ext in ['.json', '.jsonl']:
                file_type = 'json'
            elif file_ext in ['.xlsx', '.xls']:
                file_type = 'excel'
            else:
                raise ValueError(f"Could not determine file type for {path}. Please specify file_type.")
        
        # Load data based on file type
        logger.info(f"Loading data from {path} as {file_type}")
        
        if file_type == 'csv':
            return pl.read_csv(path, **kwargs)
        elif file_type == 'parquet':
            return pl.read_parquet(path, **kwargs)
        elif file_type == 'json':
            return pl.read_json(path, **kwargs)
        elif file_type == 'excel':
            # Polars supports Excel directly (in recent versions)
            try:
                return pl.read_excel(path, **kwargs)
            except AttributeError:
                # Fallback for older Polars versions
                try:
                    import pandas as pd
                    pandas_df = pd.read_excel(path, **kwargs)
                    return pl.from_pandas(pandas_df)
                except ImportError:
                    raise ImportError("To read Excel files with older Polars versions, pandas must be installed.")
        elif file_type == 'numpy':
            # Handle numpy arrays
            data = np.load(path, **kwargs)
            return pl.from_numpy(data)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def preprocess_data(
        self, 
        df: pl.DataFrame, 
        preprocessing_steps: List[Callable[[pl.DataFrame], pl.DataFrame]],
        cache_key: Optional[str] = None
    ) -> pl.DataFrame:
        """
        Apply a sequence of preprocessing steps to a DataFrame
        
        Args:
            df (pl.DataFrame): Input DataFrame
            preprocessing_steps (List[Callable]): List of functions to apply
            cache_key (Optional[str], optional): Key for caching results. Defaults to None.
            
        Returns:
            pl.DataFrame: Processed DataFrame
        """
        # Check cache if cache_key provided
        if cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.parquet")
            if os.path.exists(cache_path):
                logger.info(f"Loading preprocessed data from cache: {cache_path}")
                return pl.read_parquet(cache_path)
        
        # Apply preprocessing steps sequentially
        processed_df = df
        for i, step in enumerate(preprocessing_steps):
            logger.info(f"Applying preprocessing step {i+1}/{len(preprocessing_steps)}")
            processed_df = step(processed_df)
        
        # Cache result if cache_key provided
        if cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.parquet")
            logger.info(f"Caching preprocessed data to: {cache_path}")
            processed_df.write_parquet(cache_path)
        
        return processed_df
    
    @staticmethod
    def create_feature_engineering_pipeline(transformations: Dict[str, Callable]) -> Callable:
        """
        Create a feature engineering pipeline function
        
        Args:
            transformations (Dict[str, Callable]): Dictionary mapping column names to transformation functions
            
        Returns:
            Callable: Pipeline function that can be used in preprocess_data
        """
        def pipeline(df: pl.DataFrame) -> pl.DataFrame:
            for column, transform in transformations.items():
                if column in df.columns:
                    # Apply the transformation
                    df = transform(df, column)
            return df
        
        return pipeline
    
    @staticmethod
    def split_train_val_test(
        df: pl.DataFrame, 
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        stratify_by: Optional[str] = None,
        seed: int = 42
    ) -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
        """
        Split DataFrame into training, validation and test sets
        
        Args:
            df (pl.DataFrame): Input DataFrame
            train_ratio (float, optional): Proportion for training. Defaults to 0.7.
            val_ratio (float, optional): Proportion for validation. Defaults to 0.15.
            test_ratio (float, optional): Proportion for testing. Defaults to 0.15.
            stratify_by (Optional[str], optional): Column to stratify by. Defaults to None.
            seed (int, optional): Random seed. Defaults to 42.
            
        Returns:
            Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]: Train, validation, and test DataFrames
        """
        # Validate ratios
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1"
        
        # Set seed for reproducibility
        np.random.seed(seed)
        
        if stratify_by is None:
            # Simple random split
            n = df.shape[0]
            indices = np.random.permutation(n)
            
            train_size = int(n * train_ratio)
            val_size = int(n * val_ratio)
            
            train_indices = indices[:train_size]
            val_indices = indices[train_size:train_size + val_size]
            test_indices = indices[train_size + val_size:]
            
            train_df = df.filter(pl.lit(pl.Series(df.row_nr()).is_in(train_indices)))
            val_df = df.filter(pl.lit(pl.Series(df.row_nr()).is_in(val_indices)))
            test_df = df.filter(pl.lit(pl.Series(df.row_nr()).is_in(test_indices)))
        else:
            # Stratified split
            strata = df.groupby(stratify_by)
            train_dfs, val_dfs, test_dfs = [], [], []
            
            for _, group in strata:
                n = group.shape[0]
                indices = np.random.permutation(n)
                
                train_size = int(n * train_ratio)
                val_size = int(n * val_ratio)
                
                train_indices = indices[:train_size]
                val_indices = indices[train_size:train_size + val_size]
                test_indices = indices[train_size + val_size:]
                
                train_dfs.append(group.filter(pl.lit(pl.Series(group.row_nr()).is_in(train_indices))))
                val_dfs.append(group.filter(pl.lit(pl.Series(group.row_nr()).is_in(val_indices))))
                test_dfs.append(group.filter(pl.lit(pl.Series(group.row_nr()).is_in(test_indices))))
            
            train_df = pl.concat(train_dfs)
            val_df = pl.concat(val_dfs)
            test_df = pl.concat(test_dfs)
        
        logger.info(f"Data split: train={train_df.shape[0]}, val={val_df.shape[0]}, test={test_df.shape[0]}")
        
        return train_df, val_df, test_df
    
    @staticmethod
    def analyze_dataset(df: pl.DataFrame) -> Dict[str, Any]:
        """
        Perform exploratory data analysis on a DataFrame
        
        Args:
            df (pl.DataFrame): Input DataFrame
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        # Basic statistics
        n_rows, n_cols = df.shape
        
        # Column types and statistics
        column_info = {}
        
        for col in df.columns:
            col_type = str(df[col].dtype)
            
            # Check for missing values
            null_count = df[col].null_count()
            null_pct = 100 * null_count / n_rows if n_rows > 0 else 0
            
            # Get basic statistics based on column type
            stats = {}
            
            if col_type in ['Int64', 'float64', 'int32', 'float32', 'i64', 'f64', 'i32', 'f32']:
                # Numeric column
                stats = {
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'mean': df[col].mean(),
                    'std': df[col].std(),
                    'median': df[col].median(),
                }
            elif col_type in ['str', 'string', 'Utf8', 'object']:
                # String column
                unique_count = df[col].n_unique()
                unique_pct = 100 * unique_count / n_rows if n_rows > 0 else 0
                
                stats = {
                    'unique_count': unique_count,
                    'unique_pct': unique_pct,
                }
                
                # Get top values if not too many
                if unique_count <= 10:
                    value_counts = df[col].value_counts()
                    values = value_counts.struct.field(col).to_list()
                    counts = value_counts.struct.field("counts").to_list()
                    
                    stats['value_counts'] = {
                        str(val): int(count) for val, count in zip(values, counts)
                    }
            
            # Store column info
            column_info[col] = {
                'type': col_type,
                'null_count': null_count,
                'null_pct': null_pct,
                'stats': stats
            }
        
        # Assemble full analysis
        analysis = {
            'n_rows': n_rows,
            'n_cols': n_cols,
            'columns': column_info,
            'memory_usage': df.estimated_size(),
        }
        
        return analysis


class PolarsDataset(Dataset):
    """
    PyTorch Dataset wrapper for Polars DataFrames
    
    This class provides an efficient way to use Polars DataFrames
    with PyTorch DataLoaders.
    
    Args:
        df (pl.DataFrame): Polars DataFrame
        feature_cols (List[str]): Feature column names
        target_col (Optional[str], optional): Target column name. Defaults to None.
        transform (Optional[Callable], optional): Transform to apply to features. Defaults to None.
        target_transform (Optional[Callable], optional): Transform to apply to target. Defaults to None.
    """
    
    def __init__(
        self,
        df: pl.DataFrame,
        feature_cols: List[str],
        target_col: Optional[str] = None,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None
    ):
        self.df = df
        self.feature_cols = feature_cols
        self.target_col = target_col
        self.transform = transform
        self.target_transform = target_transform
    
    def __len__(self) -> int:
        """Return the number of samples"""
        return len(self.df)
    
    def __getitem__(self, idx: int) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """Get a sample"""
        # Extract features
        features = self.df[idx, self.feature_cols]
        
        # Convert to proper format
        if isinstance(features, pl.DataFrame):
            features = features.to_numpy().astype(np.float32)
        else:
            # Single row
            features = np.array([features.item() for features in features], dtype=np.float32)
        
        # Apply feature transform if provided
        if self.transform:
            features = self.transform(features)
        else:
            features = torch.tensor(features, dtype=torch.float32)
        
        # If no target column, return just features
        if self.target_col is None:
            return features
        
        # Extract target
        target = self.df[idx, self.target_col]
        
        # Convert to proper format
        if isinstance(target, (pl.Series, pl.DataFrame)):
            if target.shape[0] == 1:
                target = target[0].item()
            else:
                target = target.to_numpy()
                
        # Apply target transform if provided
        if self.target_transform:
            target = self.target_transform(target)
        else:
            if isinstance(target, (int, float)):
                target = torch.tensor(target)
            else:
                target = torch.tensor(target, dtype=torch.float32)
        
        return features, target


class DatasetBuilder:
    """
    Utility for building PyTorch datasets from Polars DataFrames
    
    This class provides methods for creating train, validation, and test
    datasets from Polars DataFrames with various preprocessing options.
    
    Args:
        df_processor (PolarsDataProcessor): Polars data processor instance
    """
    
    def __init__(self, df_processor: PolarsDataProcessor):
        self.df_processor = df_processor
    
    def from_polars(
        self,
        df: pl.DataFrame,
        feature_cols: List[str],
        target_col: Optional[str] = None,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        stratify_by: Optional[str] = None,
        preprocessing_steps: Optional[List[Callable]] = None,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        cache_key: Optional[str] = None,
        seed: int = 42
    ) -> Tuple[PolarsDataset, Optional[PolarsDataset], Optional[PolarsDataset]]:
        """
        Create PyTorch datasets from a Polars DataFrame
        
        Args:
            df (pl.DataFrame): Input DataFrame
            feature_cols (List[str]): Feature column names
            target_col (Optional[str], optional): Target column name. Defaults to None.
            val_ratio (float, optional): Validation set ratio. Defaults to 0.15.
            test_ratio (float, optional): Test set ratio. Defaults to 0.15.
            stratify_by (Optional[str], optional): Column to stratify by. Defaults to None.
            preprocessing_steps (Optional[List[Callable]], optional): Preprocessing steps. Defaults to None.
            transform (Optional[Callable], optional): Feature transform. Defaults to None.
            target_transform (Optional[Callable], optional): Target transform. Defaults to None.
            cache_key (Optional[str], optional): Cache key. Defaults to None.
            seed (int, optional): Random seed. Defaults to 42.
            
        Returns:
            Tuple[PolarsDataset, Optional[PolarsDataset], Optional[PolarsDataset]]: 
                Train, validation, and test datasets
        """
        # Apply preprocessing if needed
        if preprocessing_steps:
            df = self.df_processor.preprocess_data(df, preprocessing_steps, cache_key)
        
        # Split data
        train_ratio = 1.0 - val_ratio - test_ratio
        train_df, val_df, test_df = self.df_processor.split_train_val_test(
            df, train_ratio, val_ratio, test_ratio, stratify_by, seed
        )
        
        # Create datasets
        train_dataset = PolarsDataset(train_df, feature_cols, target_col, transform, target_transform)
        
        val_dataset = None
        if val_ratio > 0 and val_df.shape[0] > 0:
            val_dataset = PolarsDataset(val_df, feature_cols, target_col, transform, target_transform)
        
        test_dataset = None
        if test_ratio > 0 and test_df.shape[0] > 0:
            test_dataset = PolarsDataset(test_df, feature_cols, target_col, transform, target_transform)
        
        return train_dataset, val_dataset, test_dataset
    
    def from_file(
        self,
        file_path: str,
        feature_cols: List[str],
        target_col: Optional[str] = None,
        file_type: Optional[str] = None,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        stratify_by: Optional[str] = None,
        preprocessing_steps: Optional[List[Callable]] = None,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        cache_key: Optional[str] = None,
        seed: int = 42,
        **load_kwargs
    ) -> Tuple[PolarsDataset, Optional[PolarsDataset], Optional[PolarsDataset]]:
        """
        Create PyTorch datasets directly from a file
        
        Args:
            file_path (str): Path to data file
            feature_cols (List[str]): Feature column names
            target_col (Optional[str], optional): Target column name. Defaults to None.
            file_type (Optional[str], optional): File type. Defaults to None (autodetect).
            val_ratio (float, optional): Validation set ratio. Defaults to 0.15.
            test_ratio (float, optional): Test set ratio. Defaults to 0.15.
            stratify_by (Optional[str], optional): Column to stratify by. Defaults to None.
            preprocessing_steps (Optional[List[Callable]], optional): Preprocessing steps. Defaults to None.
            transform (Optional[Callable], optional): Feature transform. Defaults to None.
            target_transform (Optional[Callable], optional): Target transform. Defaults to None.
            cache_key (Optional[str], optional): Cache key. Defaults to None.
            seed (int, optional): Random seed. Defaults to 42.
            **load_kwargs: Additional arguments for data loading
            
        Returns:
            Tuple[PolarsDataset, Optional[PolarsDataset], Optional[PolarsDataset]]: 
                Train, validation, and test datasets
        """
        # Load data
        df = self.df_processor.load_data(file_path, file_type, **load_kwargs)
        
        # Create datasets
        return self.from_polars(
            df, 
            feature_cols, 
            target_col, 
            val_ratio, 
            test_ratio, 
            stratify_by,
            preprocessing_steps, 
            transform, 
            target_transform, 
            cache_key, 
            seed
        )


# Common preprocessing functions

def handle_missing_values(
    strategy: str = 'mean',
    fill_values: Optional[Dict[str, Any]] = None
) -> Callable[[pl.DataFrame], pl.DataFrame]:
    """
    Create a function to handle missing values
    
    Args:
        strategy (str, optional): Strategy for numeric columns ('mean', 'median', 'mode', 'constant').
            Defaults to 'mean'.
        fill_values (Optional[Dict[str, Any]], optional): Custom fill values per column.
            Defaults to None.
            
    Returns:
        Callable: Function that handles missing values
    """
    def _handle_missing(df: pl.DataFrame) -> pl.DataFrame:
        result = df
        
        # Handle columns with custom fill values first
        if fill_values:
            for col, value in fill_values.items():
                if col in result.columns:
                    result = result.with_columns(pl.col(col).fill_null(value))
        
        # Handle remaining columns based on type and strategy
        for col in result.columns:
            # Skip if already handled or no nulls
            if fill_values and col in fill_values:
                continue
                
            if result[col].null_count() == 0:
                continue
            
            col_type = str(result[col].dtype)
            
            # Handle numeric columns
            if col_type in ['Int64', 'float64', 'int32', 'float32', 'i64', 'f64', 'i32', 'f32']:
                if strategy == 'mean':
                    fill_val = result[col].mean()
                elif strategy == 'median':
                    fill_val = result[col].median()
                elif strategy == 'mode':
                    # Get mode (most common value)
                    value_counts = result[col].value_counts()
                    values = value_counts.struct.field(col).to_list()
                    counts = value_counts.struct.field("counts").to_list()
                    
                    if len(counts) > 0:
                        max_idx = np.argmax(counts)
                        fill_val = values[max_idx]
                    else:
                        fill_val = 0
                elif strategy == 'constant':
                    fill_val = 0
                else:
                    raise ValueError(f"Unknown strategy: {strategy}")
                
                result = result.with_columns(pl.col(col).fill_null(fill_val))
            
            # Handle string columns (fill with empty string)
            elif col_type in ['str', 'string', 'Utf8', 'object']:
                result = result.with_columns(pl.col(col).fill_null(""))
        
        return result
    
    return _handle_missing


def encode_categorical(
    columns: List[str],
    method: str = 'one-hot',
    max_categories: int = 20
) -> Callable[[pl.DataFrame], pl.DataFrame]:
    """
    Create a function to encode categorical variables
    
    Args:
        columns (List[str]): Columns to encode
        method (str, optional): Encoding method ('one-hot', 'label', 'ordinal').
            Defaults to 'one-hot'.
        max_categories (int, optional): Maximum categories for one-hot encoding.
            Defaults to 20.
            
    Returns:
        Callable: Function that encodes categorical variables
    """
    def _encode_categorical(df: pl.DataFrame) -> pl.DataFrame:
        result = df
        
        for col in columns:
            if col not in result.columns:
                continue
            
            if method == 'one-hot':
                # Get unique values
                unique_vals = result[col].unique().drop_nulls()
                
                # Skip if too many categories
                if len(unique_vals) > max_categories:
                    logger.warning(f"Skipping one-hot encoding for {col}: too many categories ({len(unique_vals)})")
                    continue
                
                # Create one-hot columns
                for val in unique_vals:
                    val_str = str(val)  # Convert to string for column name
                    new_col = f"{col}_{val_str}"
                    result = result.with_columns(
                        pl.lit(pl.col(col) == val).cast(pl.Int8).alias(new_col)
                    )
            
            elif method == 'label':
                # Label encoding (convert to integers)
                unique_vals = result[col].unique().drop_nulls()
                mapping = {val: i for i, val in enumerate(unique_vals)}
                
                # Create mapping function
                def map_value(x):
                    return mapping.get(x, -1) if x is not None else -1
                
                # Apply mapping
                result = result.with_columns(
                    pl.col(col).map_elements(map_value).alias(f"{col}_encoded")
                )
            
            elif method == 'ordinal':
                # Ordinal encoding (ranks)
                result = result.with_columns(
                    pl.col(col).rank().alias(f"{col}_rank")
                )
        
        return result
    
    return _encode_categorical


def normalize_features(
    columns: List[str],
    method: str = 'z-score'
) -> Callable[[pl.DataFrame], pl.DataFrame]:
    """
    Create a function to normalize features
    
    Args:
        columns (List[str]): Columns to normalize
        method (str, optional): Normalization method ('z-score', 'min-max', 'robust').
            Defaults to 'z-score'.
            
    Returns:
        Callable: Function that normalizes features
    """
    def _normalize(df: pl.DataFrame) -> pl.DataFrame:
        result = df
        
        for col in columns:
            if col not in result.columns:
                continue
            
            if method == 'z-score':
                # Z-score normalization (mean=0, std=1)
                mean = result[col].mean()
                std = result[col].std()
                
                if std == 0:  # Avoid division by zero
                    std = 1
                
                result = result.with_columns(
                    ((pl.col(col) - mean) / std).alias(f"{col}_normalized")
                )
            
            elif method == 'min-max':
                # Min-max scaling (0 to 1)
                min_val = result[col].min()
                max_val = result[col].max()
                
                if max_val == min_val:  # Avoid division by zero
                    result = result.with_columns(
                        (pl.lit(0.5)).alias(f"{col}_normalized")
                    )
                else:
                    result = result.with_columns(
                        ((pl.col(col) - min_val) / (max_val - min_val)).alias(f"{col}_normalized")
                    )
            
            elif method == 'robust':
                # Robust scaling (using median and IQR)
                median = result[col].median()
                q1 = result[col].quantile(0.25)
                q3 = result[col].quantile(0.75)
                iqr = q3 - q1
                
                if iqr == 0:  # Avoid division by zero
                    iqr = 1
                
                result = result.with_columns(
                    ((pl.col(col) - median) / iqr).alias(f"{col}_normalized")
                )
        
        return result
    
    return _normalize


def create_polynomial_features(
    columns: List[str],
    degree: int = 2,
    interaction_only: bool = False
) -> Callable[[pl.DataFrame], pl.DataFrame]:
    """
    Create polynomial features from existing features
    
    Args:
        columns (List[str]): Base columns to use
        degree (int, optional): Polynomial degree. Defaults to 2.
        interaction_only (bool, optional): Whether to include interaction terms only.
            Defaults to False.
            
    Returns:
        Callable: Function that creates polynomial features
    """
    def _create_poly_features(df: pl.DataFrame) -> pl.DataFrame:
        from itertools import combinations_with_replacement, combinations
        
        result = df
        
        # Get combinations of columns
        if interaction_only:
            # Only interactions between different features
            for d in range(2, degree + 1):
                for cols in combinations(columns, d):
                    # Check if all columns exist
                    if not all(col in result.columns for col in cols):
                        continue
                    
                    # Create interaction term
                    new_col = "_".join(cols)
                    
                    # Calculate product
                    product = result[cols[0]]
                    for col in cols[1:]:
                        product = product * result[col]
                    
                    result = result.with_columns(product.alias(new_col))
        else:
            # All polynomial terms
            for cols in combinations_with_replacement(columns, degree):
                # Count occurrences of each column
                col_counts = {}
                for col in cols:
                    col_counts[col] = col_counts.get(col, 0) + 1
                
                # Check if all columns exist
                if not all(col in result.columns for col in col_counts.keys()):
                    continue
                
                # Create feature name
                new_col = "_".join([f"{col}^{count}" if count > 1 else col 
                                  for col, count in col_counts.items()])
                
                # Calculate product
                product = pl.lit(1)
                for col, count in col_counts.items():
                    product = product * result[col] ** count
                
                result = result.with_columns(product.alias(new_col))
        
        return result
    
    return _create_poly_features
