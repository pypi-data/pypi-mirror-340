"""
Database utilities using DuckDB for SQL-based data processing and storage
"""
import os
import logging
import json
from typing import Dict, List, Any, Optional, Union, Tuple, Callable, Iterable

import numpy as np
import torch
import polars as pl
import duckdb
import pyarrow as pa

logger = logging.getLogger(__name__)


class DuckDBManager:
    """
    Utility for managing DuckDB databases and integrating with Polars
    
    This class provides methods for creating, querying, and managing DuckDB
    databases, with seamless integration with Polars DataFrames.
    
    Args:
        db_path (str, optional): Path to the database file. Defaults to ":memory:".
        read_only (bool, optional): Whether to open the database in read-only mode. Defaults to False.
        config (Optional[Dict[str, Any]], optional): Additional configuration options. Defaults to None.
    """
    
    def __init__(
        self,
        db_path: str = ":memory:",
        read_only: bool = False,
        config: Optional[Dict[str, Any]] = None
    ):
        self.db_path = db_path
        self.read_only = read_only
        self.config = config or {}
        
        # Create directory for the database if needed
        if db_path != ":memory:" and not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize connection
        self.conn = duckdb.connect(db_path, read_only=read_only)
        
        # Apply configuration
        for key, value in self.config.items():
            self.conn.execute(f"SET {key}={value}")
        
        # Enable automatic installation of extensions
        self.conn.execute("SET auto_install_extensions=true")
        
        logger.info(f"Connected to DuckDB database at {db_path}")
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info(f"Closed connection to DuckDB database at {self.db_path}")
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed"""
        self.close()
    
    def __enter__(self):
        """Support for context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting context"""
        self.close()
    
    def execute(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a SQL query
        
        Args:
            query (str): SQL query to execute
            parameters (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.
            
        Returns:
            Any: Query result
        """
        if parameters:
            result = self.conn.execute(query, parameters)
        else:
            result = self.conn.execute(query)
        return result
    
    def query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> pl.DataFrame:
        """
        Execute a SQL query and return results as a Polars DataFrame
        
        Args:
            query (str): SQL query to execute
            parameters (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.
            
        Returns:
            pl.DataFrame: Query result as a Polars DataFrame
        """
        # Execute query and convert result to Polars DataFrame
        result = self.execute(query, parameters)
        return result.pl()
    
    def create_table(
        self, 
        table_name: str, 
        df: Union[pl.DataFrame, pa.Table],
        if_exists: str = 'replace'
    ):
        """
        Create a table from a Polars DataFrame or PyArrow Table
        
        Args:
            table_name (str): Name of the table to create
            df (Union[pl.DataFrame, pa.Table]): Data to insert
            if_exists (str, optional): Action if table exists ('replace', 'append', 'error'). 
                Defaults to 'replace'.
        """
        if isinstance(df, pl.DataFrame):
            # Check if table exists
            exists = self.table_exists(table_name)
            
            if exists:
                if if_exists == 'replace':
                    self.execute(f"DROP TABLE IF EXISTS {table_name}")
                elif if_exists == 'error':
                    raise ValueError(f"Table {table_name} already exists")
                # For 'append', we don't need to do anything here
            
            if not exists or if_exists != 'append':
                # Create table
                self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df", {"df": df})
            else:
                # Append to existing table
                self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM df", {"df": df})
            
            logger.info(f"Created/updated table {table_name} with {len(df)} rows")
        else:
            # PyArrow table
            raise NotImplementedError("PyArrow tables not yet supported")
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists
        
        Args:
            table_name (str): Name of the table to check
            
        Returns:
            bool: Whether the table exists
        """
        result = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", 
            [table_name]
        )
        return len(result.fetchall()) > 0
    
    def list_tables(self) -> List[str]:
        """
        List all tables in the database
        
        Returns:
            List[str]: List of table names
        """
        result = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in result.fetchall()]
    
    def get_table_schema(self, table_name: str) -> Dict[str, str]:
        """
        Get the schema of a table
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            Dict[str, str]: Column names and types
        """
        result = self.conn.execute(f"PRAGMA table_info({table_name})")
        return {row[1]: row[2] for row in result.fetchall()}
    
    def get_table(self, table_name: str) -> pl.DataFrame:
        """
        Get a table as a Polars DataFrame
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            pl.DataFrame: Table data as a Polars DataFrame
        """
        if not self.table_exists(table_name):
            raise ValueError(f"Table {table_name} does not exist")
        
        return self.query(f"SELECT * FROM {table_name}")
    
    def register_pandas_df(self, df_name: str, pandas_df):
        """
        Register a pandas DataFrame for use in queries
        
        Args:
            df_name (str): Name to register the DataFrame as
            pandas_df: Pandas DataFrame to register
        """
        self.conn.register(df_name, pandas_df)
        logger.info(f"Registered pandas DataFrame as {df_name}")
    
    def register_polars_df(self, df_name: str, polars_df: pl.DataFrame):
        """
        Register a Polars DataFrame for use in queries
        
        Args:
            df_name (str): Name to register the DataFrame as
            polars_df (pl.DataFrame): Polars DataFrame to register
        """
        # Convert to Arrow table and register
        arrow_table = polars_df.to_arrow()
        self.conn.register(df_name, arrow_table)
        logger.info(f"Registered Polars DataFrame as {df_name}")
    
    def create_view(self, view_name: str, query: str):
        """
        Create a view from a SQL query
        
        Args:
            view_name (str): Name of the view to create
            query (str): SQL query to create the view from
        """
        self.execute(f"CREATE OR REPLACE VIEW {view_name} AS {query}")
        logger.info(f"Created view {view_name}")
    
    def explain(self, query: str) -> str:
        """
        Get the query execution plan
        
        Args:
            query (str): SQL query to explain
            
        Returns:
            str: Execution plan
        """
        result = self.conn.execute(f"EXPLAIN {query}")
        return "\n".join([row[0] for row in result.fetchall()])


class SQLDataProcessor:
    """
    SQL-based data processor using DuckDB and Polars
    
    This class provides methods for data processing using SQL queries,
    with integration between DuckDB and Polars.
    
    Args:
        db_manager (DuckDBManager): DuckDB manager instance
        cache_dir (str, optional): Directory to cache intermediate results. Defaults to "./sql_cache".
    """
    
    def __init__(
        self,
        db_manager: DuckDBManager,
        cache_dir: str = "./sql_cache"
    ):
        self.db_manager = db_manager
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def execute_query(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> pl.DataFrame:
        """
        Execute a SQL query and return results as a Polars DataFrame
        
        Args:
            query (str): SQL query to execute
            parameters (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.
            
        Returns:
            pl.DataFrame: Query result as a Polars DataFrame
        """
        return self.db_manager.query(query, parameters)
    
    def cached_query(
        self,
        query: str,
        cache_key: str,
        parameters: Optional[Dict[str, Any]] = None,
        force_refresh: bool = False
    ) -> pl.DataFrame:
        """
        Execute a SQL query with caching
        
        Args:
            query (str): SQL query to execute
            cache_key (str): Cache key for the query
            parameters (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.
            force_refresh (bool, optional): Whether to force refresh the cache. Defaults to False.
            
        Returns:
            pl.DataFrame: Query result as a Polars DataFrame
        """
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.parquet")
        
        # Check cache
        if not force_refresh and os.path.exists(cache_path):
            logger.info(f"Loading cached result from {cache_path}")
            return pl.read_parquet(cache_path)
        
        # Execute query
        result = self.execute_query(query, parameters)
        
        # Cache result
        result.write_parquet(cache_path)
        logger.info(f"Cached query result to {cache_path}")
        
        return result
    
    def process_sql_workflow(
        self,
        workflow: List[Dict[str, Any]],
        final_output: str = "result",
        cache_prefix: Optional[str] = None
    ) -> pl.DataFrame:
        """
        Process a SQL workflow with multiple steps
        
        Args:
            workflow (List[Dict[str, Any]]): List of workflow steps
            final_output (str, optional): Name of the final output table. Defaults to "result".
            cache_prefix (Optional[str], optional): Prefix for cache keys. Defaults to None.
            
        Returns:
            pl.DataFrame: Final result as a Polars DataFrame
        """
        results = {}
        
        for i, step in enumerate(workflow):
            step_type = step.get("type", "query")
            step_name = step.get("name", f"step_{i}")
            
            # Generate cache key
            cache_key = f"{cache_prefix}_{step_name}" if cache_prefix else step_name
            
            if step_type == "query":
                # Execute SQL query
                query = step["query"]
                parameters = step.get("parameters")
                use_cache = step.get("use_cache", True)
                
                if use_cache:
                    result = self.cached_query(query, cache_key, parameters)
                else:
                    result = self.execute_query(query, parameters)
                
                # Store result
                results[step_name] = result
                
                # Register as temporary table if specified
                if step.get("register_temp", False):
                    self.db_manager.register_polars_df(step_name, result)
            
            elif step_type == "create_table":
                # Create table from Polars DataFrame
                table_name = step["table_name"]
                df_name = step["df_name"]
                if_exists = step.get("if_exists", "replace")
                
                if df_name not in results:
                    raise ValueError(f"DataFrame {df_name} not found in results")
                
                self.db_manager.create_table(table_name, results[df_name], if_exists)
            
            elif step_type == "create_view":
                # Create view from SQL query
                view_name = step["view_name"]
                query = step["query"]
                self.db_manager.create_view(view_name, query)
            
            elif step_type == "load_table":
                # Load existing table
                table_name = step["table_name"]
                results[step_name] = self.db_manager.get_table(table_name)
            
            elif step_type == "transform":
                # Apply Polars transformation
                df_name = step["df_name"]
                transform_fn = step["transform_fn"]
                
                if df_name not in results:
                    raise ValueError(f"DataFrame {df_name} not found in results")
                
                results[step_name] = transform_fn(results[df_name])
            
            else:
                raise ValueError(f"Unknown step type: {step_type}")
            
            logger.info(f"Completed workflow step {i+1}/{len(workflow)}: {step_name}")
        
        # Return final result
        if final_output in results:
            return results[final_output]
        else:
            raise ValueError(f"Final output {final_output} not found in results")


class AnalyticalDataManager:
    """
    Manager for analytical data processing with DuckDB and Polars
    
    This class provides high-level methods for data analysis and transformation
    using DuckDB for SQL processing and Polars for DataFrame operations.
    
    Args:
        db_path (str, optional): Path to the database file. Defaults to ":memory:".
        cache_dir (str, optional): Directory to cache intermediate results. Defaults to "./data_cache".
    """
    
    def __init__(
        self,
        db_path: str = ":memory:",
        cache_dir: str = "./data_cache"
    ):
        self.db_manager = DuckDBManager(db_path)
        self.sql_processor = SQLDataProcessor(self.db_manager, cache_dir)
        self.cache_dir = cache_dir
    
    def load_data(
        self,
        source: Union[str, pl.DataFrame],
        name: str,
        source_type: Optional[str] = None,
        if_exists: str = "replace",
        **kwargs
    ) -> pl.DataFrame:
        """
        Load data from various sources into the database
        
        Args:
            source (Union[str, pl.DataFrame]): Data source (file path or DataFrame)
            name (str): Name to register the data as
            source_type (Optional[str], optional): Type of source ('csv', 'parquet', etc.). 
                Defaults to None (auto-detect).
            if_exists (str, optional): Action if table exists. Defaults to "replace".
            **kwargs: Additional arguments for data loading
            
        Returns:
            pl.DataFrame: Loaded data as a Polars DataFrame
        """
        if isinstance(source, pl.DataFrame):
            # Source is a Polars DataFrame
            df = source
            self.db_manager.create_table(name, df, if_exists)
            return df
        
        # Source is a file path
        if source_type is None:
            # Auto-detect source type from file extension
            ext = os.path.splitext(source)[1].lower()
            if ext in ['.csv', '.txt']:
                source_type = 'csv'
            elif ext in ['.parquet', '.pq']:
                source_type = 'parquet'
            elif ext in ['.json', '.jsonl']:
                source_type = 'json'
            else:
                raise ValueError(f"Could not determine source type for {source}")
        
        # Load data using SQL
        query = ""
        if source_type == 'csv':
            query = f"SELECT * FROM read_csv('{source}'"
            # Add optional parameters
            if 'header' in kwargs:
                query += f", header={str(kwargs['header']).lower()}"
            if 'delimiter' in kwargs:
                query += f", delim='{kwargs['delimiter']}'"
            if 'columns' in kwargs:
                cols = kwargs['columns']
                if isinstance(cols, dict):
                    cols_str = ", ".join([f"'{k}' {v}" for k, v in cols.items()])
                    query += f", columns=({cols_str})"
            query += ")"
        elif source_type == 'parquet':
            query = f"SELECT * FROM read_parquet('{source}')"
        elif source_type == 'json':
            query = f"SELECT * FROM read_json('{source}')"
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        # Execute query and create table
        df = self.sql_processor.execute_query(query)
        self.db_manager.create_table(name, df, if_exists)
        
        return df
    
    def execute_sql(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        cache_key: Optional[str] = None
    ) -> pl.DataFrame:
        """
        Execute a SQL query
        
        Args:
            query (str): SQL query to execute
            parameters (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.
            cache_key (Optional[str], optional): Cache key for the query. Defaults to None.
            
        Returns:
            pl.DataFrame: Query result as a Polars DataFrame
        """
        if cache_key:
            return self.sql_processor.cached_query(query, cache_key, parameters)
        else:
            return self.sql_processor.execute_query(query, parameters)
    
    def run_analytical_pipeline(
        self,
        pipeline: List[Dict[str, Any]],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, pl.DataFrame]:
        """
        Run an analytical pipeline with multiple steps
        
        Args:
            pipeline (List[Dict[str, Any]]): List of pipeline steps
            params (Optional[Dict[str, Any]], optional): Pipeline parameters. Defaults to None.
            
        Returns:
            Dict[str, pl.DataFrame]: Results of each pipeline step
        """
        params = params or {}
        results = {}
        
        for i, step in enumerate(pipeline):
            step_type = step["type"]
            step_name = step["name"]
            
            try:
                # Process step based on type
                if step_type == "load_data":
                    source = step["source"]
                    # Substitute parameters if source is a string
                    if isinstance(source, str):
                        for param_name, param_value in params.items():
                            source = source.replace(f"{{{param_name}}}", str(param_value))
                    
                    source_type = step.get("source_type")
                    table_name = step.get("table_name", step_name)
                    
                    results[step_name] = self.load_data(
                        source=source,
                        name=table_name,
                        source_type=source_type,
                        **{k: v for k, v in step.items() if k not in ["type", "name", "source", "source_type", "table_name"]}
                    )
                
                elif step_type == "sql":
                    query = step["query"]
                    # Substitute parameters in query
                    for param_name, param_value in params.items():
                        query = query.replace(f"{{{param_name}}}", str(param_value))
                    
                    cache_key = step.get("cache_key")
                    store_table = step.get("store_table")
                    
                    result = self.execute_sql(query, cache_key=cache_key)
                    results[step_name] = result
                    
                    # Store as table if requested
                    if store_table:
                        self.db_manager.create_table(
                            store_table if isinstance(store_table, str) else step_name,
                            result
                        )
                
                elif step_type == "transform":
                    # Process data transformation using Polars
                    input_name = step["input"]
                    transform_type = step["transform_type"]
                    
                    if input_name not in results:
                        raise ValueError(f"Input {input_name} not found in results")
                    
                    input_df = results[input_name]
                    
                    if transform_type == "filter":
                        # Filter rows
                        filter_expr = step["filter"]
                        if isinstance(filter_expr, str):
                            # Parse as Polars expression
                            filter_expr = eval(f"pl.col('{filter_expr}')")
                        results[step_name] = input_df.filter(filter_expr)
                    
                    elif transform_type == "select":
                        # Select columns
                        columns = step["columns"]
                        results[step_name] = input_df.select(columns)
                    
                    elif transform_type == "groupby":
                        # Group by and aggregate
                        groupby_cols = step["groupby"]
                        aggs = step["aggs"]
                        
                        # Convert string aggregations to Polars expressions
                        if isinstance(aggs, dict):
                            agg_exprs = []
                            for col, agg in aggs.items():
                                if agg == "sum":
                                    agg_exprs.append(pl.col(col).sum().alias(f"{col}_sum"))
                                elif agg == "mean":
                                    agg_exprs.append(pl.col(col).mean().alias(f"{col}_mean"))
                                elif agg == "count":
                                    agg_exprs.append(pl.count().alias(f"{col}_count"))
                                elif agg == "min":
                                    agg_exprs.append(pl.col(col).min().alias(f"{col}_min"))
                                elif agg == "max":
                                    agg_exprs.append(pl.col(col).max().alias(f"{col}_max"))
                                else:
                                    raise ValueError(f"Unsupported aggregation: {agg}")
                            results[step_name] = input_df.groupby(groupby_cols).agg(agg_exprs)
                        else:
                            results[step_name] = input_df.groupby(groupby_cols).agg(aggs)
                    
                    elif transform_type == "join":
                        # Join with another DataFrame
                        right_name = step["right"]
                        if right_name not in results:
                            raise ValueError(f"Right DataFrame {right_name} not found in results")
                        
                        right_df = results[right_name]
                        on = step["on"]
                        how = step.get("how", "inner")
                        
                        results[step_name] = input_df.join(right_df, on=on, how=how)
                    
                    elif transform_type == "custom":
                        # Custom transformation function
                        transform_fn = step["transform_fn"]
                        results[step_name] = transform_fn(input_df)
                    
                    else:
                        raise ValueError(f"Unsupported transformation type: {transform_type}")
                
                elif step_type == "export":
                    # Export results to file
                    input_name = step["input"]
                    export_path = step["path"]
                    export_type = step.get("export_type", "parquet")
                    
                    if input_name not in results:
                        raise ValueError(f"Input {input_name} not found in results")
                    
                    input_df = results[input_name]
                    
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(export_path), exist_ok=True)
                    
                    if export_type == "parquet":
                        input_df.write_parquet(export_path)
                    elif export_type == "csv":
                        input_df.write_csv(export_path)
                    elif export_type == "json":
                        input_df.write_json(export_path)
                    else:
                        raise ValueError(f"Unsupported export type: {export_type}")
                    
                    logger.info(f"Exported {input_name} to {export_path}")
                
                else:
                    raise ValueError(f"Unsupported step type: {step_type}")
                
                logger.info(f"Completed pipeline step {i+1}/{len(pipeline)}: {step_name}")
            
            except Exception as e:
                logger.error(f"Error in pipeline step {step_name}: {str(e)}")
                raise
        
        return results


class DuckDBDataset(torch.utils.data.Dataset):
    """
    PyTorch Dataset backed by a DuckDB query
    
    This class provides a memory-efficient way to use DuckDB for
    feeding data into PyTorch models.
    
    Args:
        db_manager (DuckDBManager): DuckDB manager instance
        query (str): SQL query to execute
        feature_cols (List[str]): Feature column names
        target_col (Optional[str], optional): Target column name. Defaults to None.
        batch_size (int, optional): Batch size for efficient data loading. Defaults to 1000.
        transform (Optional[Callable], optional): Transform to apply to features. Defaults to None.
        target_transform (Optional[Callable], optional): Transform to apply to target. Defaults to None.
    """
    
    def __init__(
        self,
        db_manager: DuckDBManager,
        query: str,
        feature_cols: List[str],
        target_col: Optional[str] = None,
        batch_size: int = 1000,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None
    ):
        self.db_manager = db_manager
        self.query = query
        self.feature_cols = feature_cols
        self.target_col = target_col
        self.batch_size = batch_size
        self.transform = transform
        self.target_transform = target_transform
        
        # Determine total number of rows
        count_query = f"SELECT COUNT(*) FROM ({query}) as q"
        self.total_rows = self.db_manager.query(count_query).item(0, 0)
        
        # Number of batches
        self.num_batches = (self.total_rows + batch_size - 1) // batch_size
        
        # Cache for batches
        self.batch_cache = {}
    
    def __len__(self) -> int:
        """Return the number of samples"""
        return self.total_rows
    
    def _load_batch(self, batch_idx: int) -> pl.DataFrame:
        """
        Load a batch of data from the database
        
        Args:
            batch_idx (int): Batch index
            
        Returns:
            pl.DataFrame: Batch data
        """
        # Check if batch is already cached
        if batch_idx in self.batch_cache:
            return self.batch_cache[batch_idx]
        
        # Calculate offset and limit
        offset = batch_idx * self.batch_size
        limit = min(self.batch_size, self.total_rows - offset)
        
        # Execute query with pagination
        batch_query = f"SELECT * FROM ({self.query}) as q LIMIT {limit} OFFSET {offset}"
        batch_df = self.db_manager.query(batch_query)
        
        # Cache batch
        self.batch_cache[batch_idx] = batch_df
        
        return batch_df
    
    def __getitem__(self, idx: int) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """Get a sample"""
        # Calculate batch index and position within batch
        batch_idx = idx // self.batch_size
        pos_in_batch = idx % self.batch_size
        
        # Load batch if needed
        batch_df = self._load_batch(batch_idx)
        
        # Extract features
        if len(self.feature_cols) == 1:
            # Single feature column
            features = batch_df[pos_in_batch, self.feature_cols[0]]
            if isinstance(features, pl.Series):
                features = features.to_numpy().astype(np.float32)
            else:
                features = np.array([features], dtype=np.float32)
        else:
            # Multiple feature columns
            features = batch_df[pos_in_batch, self.feature_cols].to_numpy().astype(np.float32)
        
        # Apply feature transform if provided
        if self.transform:
            features = self.transform(features)
        else:
            features = torch.tensor(features, dtype=torch.float32)
        
        # If no target column, return just features
        if self.target_col is None:
            return features
        
        # Extract target
        target = batch_df[pos_in_batch, self.target_col]
        
        # Apply target transform if provided
        if self.target_transform:
            target = self.target_transform(target)
        else:
            if isinstance(target, (int, float)):
                target = torch.tensor(target)
            else:
                target = torch.tensor(target, dtype=torch.float32)
        
        return features, target
    
    def get_batch(self, batch_idx: int) -> Dict[str, torch.Tensor]:
        """
        Get a full batch of data
        
        Args:
            batch_idx (int): Batch index
            
        Returns:
            Dict[str, torch.Tensor]: Batch data as tensors
        """
        batch_df = self._load_batch(batch_idx)
        
        # Extract features
        features = batch_df.select(self.feature_cols).to_numpy().astype(np.float32)
        features_tensor = torch.tensor(features, dtype=torch.float32)
        
        result = {"features": features_tensor}
        
        # Extract target if available
        if self.target_col is not None:
            target = batch_df.select([self.target_col]).to_numpy()
            target_tensor = torch.tensor(target, dtype=torch.float32)
            result["target"] = target_tensor
        
        return result
    
    def clear_cache(self):
        """Clear the batch cache"""
        self.batch_cache = {}


def sql_to_pytorch_dataset(
    db_path: str,
    query: str,
    feature_cols: List[str],
    target_col: Optional[str] = None,
    batch_size: int = 1000,
    transform: Optional[Callable] = None,
    target_transform: Optional[Callable] = None
) -> DuckDBDataset:
    """
    Create a PyTorch Dataset from a SQL query
    
    Args:
        db_path (str): Path to the database file
        query (str): SQL query to execute
        feature_cols (List[str]): Feature column names
        target_col (Optional[str], optional): Target column name. Defaults to None.
        batch_size (int, optional): Batch size for efficient data loading. Defaults to 1000.
        transform (Optional[Callable], optional): Transform to apply to features. Defaults to None.
        target_transform (Optional[Callable], optional): Transform to apply to target. Defaults to None.
        
    Returns:
        DuckDBDataset: PyTorch Dataset backed by a DuckDB query
    """
    db_manager = DuckDBManager(db_path)
    return DuckDBDataset(
        db_manager=db_manager,
        query=query,
        feature_cols=feature_cols,
        target_col=target_col,
        batch_size=batch_size,
        transform=transform,
        target_transform=target_transform
    )


def execute_analytical_query(
    db_path: str,
    query: str,
    cache_dir: str = "./query_cache",
    cache_key: Optional[str] = None,
    read_only: bool = False
) -> pl.DataFrame:
    """
    Execute an analytical query and return results as a Polars DataFrame
    
    Args:
        db_path (str): Path to the database file
        query (str): SQL query to execute
        cache_dir (str, optional): Directory for query cache. Defaults to "./query_cache".
        cache_key (Optional[str], optional): Cache key. Defaults to None.
        read_only (bool, optional): Whether to open the database in read-only mode. Defaults to False.
        
    Returns:
        pl.DataFrame: Query result as a Polars DataFrame
    """
    with DuckDBManager(db_path, read_only=read_only) as db:
        processor = SQLDataProcessor(db, cache_dir)
        
        if cache_key:
            return processor.cached_query(query, cache_key)
        else:
            return processor.execute_query(query)


def etl_pipeline(
    source_db: str,
    destination_db: str,
    extract_query: str,
    transform_fn: Optional[Callable[[pl.DataFrame], pl.DataFrame]] = None,
    destination_table: str = "transformed_data",
    batch_size: int = 10000,
    show_progress: bool = True
) -> int:
    """
    Run an ETL pipeline from one database to another
    
    Args:
        source_db (str): Path to the source database file
        destination_db (str): Path to the destination database file
        extract_query (str): SQL query to extract data from source
        transform_fn (Optional[Callable], optional): Function to transform the data. 
            Defaults to None.
        destination_table (str, optional): Name of the destination table. 
            Defaults to "transformed_data".
        batch_size (int, optional): Batch size for processing. Defaults to 10000.
        show_progress (bool, optional): Whether to show a progress bar. Defaults to True.
        
    Returns:
        int: Number of rows processed
    """
    # Set up source and destination connections
    source = DuckDBManager(source_db, read_only=True)
    destination = DuckDBManager(destination_db)
    
    # Determine total rows to process
    count_query = f"SELECT COUNT(*) FROM ({extract_query}) as q"
    total_rows = source.query(count_query).item(0, 0)
    
    # Set up progress tracking
    processed_rows = 0
    total_batches = (total_rows + batch_size - 1) // batch_size
    
    try:
        if show_progress:
            try:
                from tqdm import tqdm
                progress = tqdm(total=total_rows, desc="ETL Progress")
            except ImportError:
                progress = None
                logger.info(f"Processing {total_rows} rows in {total_batches} batches")
        else:
            progress = None
        
        # Process in batches
        for batch in range(total_batches):
            # Extract batch
            offset = batch * batch_size
            limit = min(batch_size, total_rows - offset)
            
            batch_query = f"SELECT * FROM ({extract_query}) as q LIMIT {limit} OFFSET {offset}"
            data = source.query(batch_query)
            
            # Transform batch if needed
            if transform_fn:
                data = transform_fn(data)
            
            # Load batch into destination
            if batch == 0:
                # First batch, create table
                destination.create_table(destination_table, data, if_exists="replace")
            else:
                # Append to existing table
                destination.create_table(destination_table, data, if_exists="append")
            
            # Update progress
            processed_rows += len(data)
            if progress:
                progress.update(len(data))
            
            if not progress and batch % 10 == 0 and show_progress:
                logger.info(f"Processed {processed_rows}/{total_rows} rows ({processed_rows/total_rows:.1%})")
        
        if progress:
            progress.close()
        
        logger.info(f"ETL pipeline completed. Processed {processed_rows} rows.")
        
        return processed_rows
    
    finally:
        # Clean up connections
        source.close()
        destination.close()
