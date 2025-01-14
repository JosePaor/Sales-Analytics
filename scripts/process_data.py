import pandas as pd
import sqlite3

def read_and_clean_data(csv_path):
    """
    Reads the CSV file and performs initial cleaning:
    - Fills missing quantity values with 0.
    - Replaces invalid or missing price values with NaN.
    - Fills missing price values with the median price within the same category.
    - Drops rows where both quantity and price are invalid.

    Args:
        csv_path (str): Path to the sales data CSV file.

    Returns:
        pd.DataFrame: Cleaned sales data.
    """
    # Read CSV file
    data = pd.read_csv(csv_path)

    # Fill missing quantity with 0
    data["quantity"] = data["quantity"].fillna(0)

    # Identify and replace invalid price values
    data["price"] = pd.to_numeric(data["price"], errors='coerce')

    # Fill missing price values with the median price within the same category
    data["price"] = data.groupby("category")["price"].transform(lambda x: x.fillna(x.median()))

    # Drop rows where both quantity and price are invalid
    data = data.dropna(subset=["price"])

    return data

def add_derived_columns(data):
    """
    Adds derived columns to the data:
    - total_sales: quantity * price
    - day_of_week: day of the week from the date
    - high_volume: True if quantity > 10, otherwise False

    Args:
        data (pd.DataFrame): Cleaned sales data.

    Returns:
        pd.DataFrame: Data with derived columns.
    """
    data["total_sales"] = data["quantity"] * data["price"]
    data["day_of_week"] = pd.to_datetime(data["date"]).dt.day_name()
    data["high_volume"] = data["quantity"] > 10
    return data

def detect_outliers(df):
    """
    Detects outliers in a DataFrame based on the quantity column using the Z-score method.

    Args:
        df (pd.DataFrame): DataFrame containing the data.

    Returns:
        pd.DataFrame: DataFrame with an additional 'outlier' column indicating outliers.
    """
    df['z_score'] = df.groupby("category")["quantity"].transform(lambda x: (x - x.mean()) / x.std())
    df['outlier'] = df['z_score'].abs() > 2
    return df

def calculate_aggregated_metrics(data):
    """
    Calculates aggregated metrics by category:
    - Average price per category.
    - Total revenue for each category.
    - Day with highest sales for the category.

    Args:
        data (pd.DataFrame): Cleaned sales data.

    Returns:
        pd.DataFrame: Aggregated metrics by category.
    """
    aggregated_metrics = data.groupby("category").agg(
        average_price=("price", "mean"),
        total_revenue=("total_sales", "sum"),
        day_with_highest_sales=("day_of_week", lambda x: x.value_counts().idxmax())
    ).reset_index()
    return aggregated_metrics

def store_data_in_sqlite(data, aggregated_metrics, db_path):
    """
    Stores the data in an SQLite database.

    Args:
        data (pd.DataFrame): Data to be stored.
        aggregated_metrics (pd.DataFrame): Aggregated metrics to be stored.
        db_path (str): Path to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    data.to_sql("transactions", conn, if_exists="replace", index=False)
    aggregated_metrics.to_sql("aggregated_metrics", conn, if_exists="replace", index=False)

    # Store outliers table
    outliers = data[data["outlier"]]
    outliers.to_sql("outliers", conn, if_exists="replace", index=False)

    # Close the connection
    conn.close()

    print("Data processed and stored successfully in", db_path)

if __name__ == "__main__":
    # Define paths
    csv_path = "data/sales_data.csv"
    db_path = "data/sales_dashboard.db"

    # Process data
    sales_data = read_and_clean_data(csv_path)
    sales_data = add_derived_columns(sales_data)
    sales_data = detect_outliers(sales_data)
    aggregated_metrics = calculate_aggregated_metrics(sales_data)
    store_data_in_sqlite(sales_data, aggregated_metrics, db_path)