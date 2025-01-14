from fastapi import APIRouter
import sqlite3
import pandas as pd
from typing import Optional

router = APIRouter()

def execute_query(query: str, params: Optional[tuple] = None):
    """
    Executes a SQL query on the SQLite database and returns the result as a DataFrame.
    
    Args:
        query (str): The SQL query to execute.
        params (Optional[tuple]): Parameters to pass to the query.

    Returns:
        pd.DataFrame: The result of the query as a DataFrame.
    """
    conn = sqlite3.connect("data/sales_dashboard.db")
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

@router.get("/sales/category")
def get_sales_by_category():
    """
    Returns aggregated metrics for each category (e.g., total revenue, average price, day with highest sales).
    
    Returns:
        List[dict]: A list of dictionaries containing the aggregated metrics for each category.
    """
    query = """
    SELECT category, average_price, total_revenue, day_with_highest_sales
    FROM aggregated_metrics
    """
    df = execute_query(query)
    return df.to_dict(orient="records")

@router.get("/sales/outliers")
def get_outliers():
    """
    Returns flagged outlier transactions.
    
    Returns:
        List[dict]: A list of dictionaries containing the outlier transactions.
    """
    query = "SELECT * FROM outliers"
    df = execute_query(query)
    return df.to_dict(orient="records")