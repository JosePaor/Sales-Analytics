import sqlite3
import pandas as pd

def execute_query(db_path, query):
    """
    Executes a SQL query on the given SQLite database and returns the result as a DataFrame.
    
    Args:
        db_path (str): The path to the SQLite database.
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: The result of the query as a DataFrame.
    """
    conn = sqlite3.connect(db_path)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

if __name__ == "__main__":
    # Define the path to the SQLite database
    db_path = "data/sales_dashboard.db"

    # Query 1: Total revenue and average price per category
    query1 = """
    SELECT category, average_price, total_revenue, day_with_highest_sales
    FROM aggregated_metrics;
    """
    print("Aggregated Metrics by Category:")
    print(execute_query(db_path, query1))

    # Query 2: Outliers
    query2 = """
    SELECT * FROM outliers;
    """
    print("\nOutliers:")
    print(execute_query(db_path, query2))

    # Query 3: Transactions
    query3 = """
    SELECT * FROM transactions;
    """
    print("\nTransactions:")
    print(execute_query(db_path, query3))

    # Query 4: Total revenue and average price per category
    query4 = """
    SELECT category, AVG(price) as average_price, SUM(total_sales) as total_revenue
    FROM transactions
    GROUP BY category;
    """
    print("\nTotal Revenue and Average Price per Category:")
    print(execute_query(db_path, query4))

    # Query 5: Day with highest sales per category
    query5 = """
    SELECT category, day_of_week, SUM(total_sales) as total_sales
    FROM transactions
    GROUP BY category, day_of_week
    ORDER BY category, total_sales DESC;
    """
    print("\nDay with Highest Sales per Category:")
    print(execute_query(db_path, query5))