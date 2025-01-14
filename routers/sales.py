from fastapi import APIRouter, Query
from typing import Optional, List
import sqlite3
import pandas as pd

router = APIRouter()

def execute_query(query: str, params: Optional[tuple] = None):
    conn = sqlite3.connect("data/sales_dashboard.db")
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

@router.get("/sales/product")
def get_sales_by_product(category: Optional[str] = None, product: Optional[str] = None):
    query = "SELECT product, SUM(total_sales) as total_sales, category FROM transactions"
    conditions = []
    params = []

    if category:
        conditions.append("category = ?")
        params.append(category)
    if product:
        conditions.append("product = ?")
        params.append(product)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY product, category"
    df = execute_query(query, tuple(params))
    return {"products": df.to_dict(orient="records")}

@router.get("/sales/day")
def get_sales_by_day(startDate: Optional[str] = None, endDate: Optional[str] = None):
    query = "SELECT date, SUM(total_sales) as total_sales FROM transactions"
    conditions = []
    params = []

    if startDate:
        conditions.append("date >= ?")
        params.append(startDate)
    if endDate:
        conditions.append("date <= ?")
        params.append(endDate)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY date"
    df = execute_query(query, tuple(params))
    return {"sales": df.to_dict(orient="records")}

@router.get("/sales/category")
def get_sales_by_category():
    query = """
    SELECT category, SUM(total_sales) as total_revenue, AVG(price) as average_price, 
           MAX(day_of_week) as day_with_highest_sales
    FROM transactions
    GROUP BY category
    """
    df = execute_query(query)
    return {"categories": df.to_dict(orient="records")}

@router.get("/sales/outliers")
def get_outliers():
    query = "SELECT transaction_id, date, category, product, z_score FROM outliers"
    df = execute_query(query)
    return {"outliers": df.to_dict(orient="records")}