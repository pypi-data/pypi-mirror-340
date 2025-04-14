"""
Example using DuckDB with PyDeevo for SQL-based data analytics
"""
import os
import polars as pl
import torch
from torch.utils.data import DataLoader
import lightning as L
import matplotlib.pyplot as plt
import numpy as np

from pydeevo.models.base import FlexibleModule
from pydeevo.utils.database import (
    DuckDBManager,
    AnalyticalDataManager,
    sql_to_pytorch_dataset,
    execute_analytical_query
)


def main():
    """Example of using DuckDB with PyDeevo"""
    print("Setting up analytics environment with DuckDB...")
    
    # Set up directories
    os.makedirs("./duckdb_example", exist_ok=True)
    db_path = "./duckdb_example/analytics.duckdb"
    
    # Create sample data using Polars
    print("Creating sample data...")
    # Customer data
    customers = pl.DataFrame({
        "customer_id": list(range(1, 1001)),
        "age": np.random.randint(18, 80, 1000),
        "income": np.random.lognormal(10, 1, 1000),
        "segment": np.random.choice(["A", "B", "C"], 1000)
    })
    
    # Transaction data
    transactions = pl.DataFrame({
        "transaction_id": list(range(1, 10001)),
        "customer_id": np.random.randint(1, 1001, 10000),
        "amount": np.random.lognormal(4, 1, 10000),
        "category": np.random.choice(["Food", "Electronics", "Clothing", "Services"], 10000),
        "timestamp": np.random.randint(1600000000, 1700000000, 10000)
    })
    
    # Set up DuckDB and load data
    print("Loading data into DuckDB...")
    analytics = AnalyticalDataManager(db_path, cache_dir="./duckdb_example/cache")
    analytics.load_data(customers, "customers")
    analytics.load_data(transactions, "transactions")
    
    # Run some analytical queries
    print("Running analytical queries...")
    
    # Customer spending by segment
    segment_query = """
    SELECT 
        c.segment, 
        COUNT(DISTINCT c.customer_id) as customer_count,
        COUNT(t.transaction_id) as transaction_count,
        SUM(t.amount) as total_spend,
        AVG(t.amount) as avg_transaction,
        SUM(t.amount) / COUNT(DISTINCT c.customer_id) as spend_per_customer
    FROM customers c
    JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.segment
    ORDER BY total_spend DESC
    """
    
    segment_results = analytics.execute_sql(
        segment_query, 
        cache_key="segment_analysis"
    )
    
    print("\nCustomer Spending by Segment:")
    print(segment_results)
    
    # Category popularity
    category_query = """
    SELECT 
        t.category,
        COUNT(*) as transaction_count,
        SUM(t.amount) as total_spend,
        AVG(t.amount) as avg_amount
    FROM transactions t
    GROUP BY t.category
    ORDER BY total_spend DESC
    """
    
    category_results = analytics.execute_sql(
        category_query, 
        cache_key="category_analysis"
    )
    
    print("\nCategory Popularity:")
    print(category_results)
    
    # High-value customers
    top_customers_query = """
    SELECT 
        c.customer_id,
        c.age,
        c.segment,
        COUNT(t.transaction_id) as transaction_count,
        SUM(t.amount) as total_spend
    FROM customers c
    JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id, c.age, c.segment
    ORDER BY total_spend DESC
    LIMIT 20
    """
    
    top_customers = analytics.execute_sql(
        top_customers_query, 
        cache_key="top_customers"
    )
    
    print("\nTop 5 Customers by Spend:")
    print(top_customers.head(5))
    
    # Prepare data for machine learning model
    print("\nPreparing data for machine learning...")
    
    # Get feature data for predicting customer spending
    feature_query = """
    SELECT 
        c.customer_id,
        c.age,
        CASE WHEN c.segment = 'A' THEN 1 WHEN c.segment = 'B' THEN 2 ELSE 3 END as segment_num,
        c.income,
        COUNT(t.transaction_id) as transaction_count,
        AVG(t.amount) as avg_transaction,
        SUM(t.amount) as total_spend
    FROM customers c
    JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id, c.age, c.segment, c.income
    """
    
    # Create a PyTorch dataset directly from SQL
    dataset = sql_to_pytorch_dataset(
        db_path=db_path,
        query=feature_query,
        feature_cols=["age", "segment_num", "income", "transaction_count", "avg_transaction"],
        target_col="total_spend",
        batch_size=100
    )
    
    print(f"Created dataset with {len(dataset)} samples")
    
    # Split into train, validation, test sets
    train_size = int(0.7 * len(dataset))
    val_size = int(0.15 * len(dataset))
    test_size = len(dataset) - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size, test_size]
    )
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32)
    test_loader = DataLoader(test_dataset, batch_size=32)
    
    # Create and train a regression model
    print("Creating and training model...")
    
    model = FlexibleModule(
        architecture=[5, 64, 32, 16, 1],  # 5 features, 1 output
        learning_rate=0.001,
        loss_fn=torch.nn.MSELoss()
    )
    
    trainer = L.Trainer(
        max_epochs=50,
        enable_progress_bar=True,
        log_every_n_steps=10,
        enable_model_summary=True,
    )
    
    trainer.fit(model, train_loader, val_loader)
    
    # Test model
    results = trainer.test(model, test_loader)
    print(f"Test results: {results}")
    
    # Make predictions for sample data
    print("Making predictions...")
    model.eval()
    predictions = []
    actuals = []
    
    with torch.no_grad():
        for batch in test_loader:
            features, target = batch
            output = model(features)
            predictions.extend(output.squeeze().cpu().numpy())
            actuals.extend(target.squeeze().cpu().numpy())
    
    # Plot predictions vs actuals
    plt.figure(figsize=(10, 6))
    plt.scatter(actuals, predictions, alpha=0.5)
    
    # Add perfect prediction line
    min_val = min(min(actuals), min(predictions))
    max_val = max(max(actuals), max(predictions))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')
    
    plt.xlabel('Actual Spending')
    plt.ylabel('Predicted Spending')
    plt.title('Customer Spending Prediction')
    plt.grid(True)
    
    plt.savefig("./duckdb_example/predictions.png")
    print("Results saved to ./duckdb_example/predictions.png")
    
    # Run an analytical pipeline
    print("\nRunning analytical pipeline...")
    
    pipeline = [
        {
            "type": "sql",
            "name": "age_brackets",
            "query": """
            SELECT 
                CASE 
                    WHEN age < 30 THEN 'Under 30'
                    WHEN age >= 30 AND age < 45 THEN '30-44'
                    WHEN age >= 45 AND age < 60 THEN '45-59'
                    ELSE '60+' 
                END as age_group,
                COUNT(*) as customer_count,
                AVG(income) as avg_income
            FROM customers
            GROUP BY age_group
            ORDER BY age_group
            """,
            "cache_key": "age_brackets"
        },
        {
            "type": "sql",
            "name": "age_spending",
            "query": """
            SELECT 
                CASE 
                    WHEN c.age < 30 THEN 'Under 30'
                    WHEN c.age >= 30 AND c.age < 45 THEN '30-44'
                    WHEN c.age >= 45 AND c.age < 60 THEN '45-59'
                    ELSE '60+' 
                END as age_group,
                AVG(t.amount) as avg_transaction,
                SUM(t.amount) / COUNT(DISTINCT c.customer_id) as spend_per_customer
            FROM customers c
            JOIN transactions t ON c.customer_id = t.customer_id
            GROUP BY age_group
            ORDER BY age_group
            """,
            "cache_key": "age_spending"
        },
        {
            "type": "transform",
            "name": "combined_age_analysis",
            "input": "age_brackets",
            "transform_type": "join",
            "right": "age_spending",
            "on": "age_group",
            "how": "inner"
        },
        {
            "type": "export",
            "input": "combined_age_analysis",
            "path": "./duckdb_example/age_analysis.csv",
            "export_type": "csv"
        }
    ]
    
    pipeline_results = analytics.run_analytical_pipeline(pipeline)
    
    print("\nAge Group Analysis:")
    print(pipeline_results["combined_age_analysis"])
    print("\nAnalysis exported to ./duckdb_example/age_analysis.csv")
    
    print("\nDuckDB example completed!")


if __name__ == "__main__":
    main()
