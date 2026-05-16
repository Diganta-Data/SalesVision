import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta

class DataManager:
    def __init__(self, db_path='data/sales_vision.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        
    def generate_sample_data(self, num_rows=5000):
        """Generates a comprehensive sample superstore dataset."""
        np.random.seed(42)
        
        # Categories and Products
        categories = {
            'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
            'Office Supplies': ['Storage', 'Art', 'Paper', 'Binders', 'Appliances'],
            'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers']
        }
        
        regions = ['North', 'South', 'East', 'West', 'Central']
        segments = ['Consumer', 'Corporate', 'Home Office']
        
        data = []
        start_date = datetime(2022, 1, 1)
        
        for i in range(num_rows):
            order_date = start_date + timedelta(days=np.random.randint(0, 1000))
            category = np.random.choice(list(categories.keys()))
            sub_category = np.random.choice(categories[category])
            
            # Base price and profit logic
            base_sales = np.random.uniform(10, 500)
            if category == 'Technology':
                base_sales *= 2
            
            discount = np.random.choice([0, 0.1, 0.2, 0.4])
            sales = base_sales * (1 - discount)
            profit_margin = np.random.uniform(0.05, 0.3) - (discount * 0.5)
            profit = sales * profit_margin
            
            data.append({
                'Order_ID': f'CA-2024-{10000 + i}',
                'Order_Date': order_date,
                'Customer_ID': f'CU-{100 + np.random.randint(0, 500)}',
                'Segment': np.random.choice(segments),
                'Region': np.random.choice(regions),
                'Category': category,
                'Sub_Category': sub_category,
                'Sales': round(sales, 2),
                'Quantity': np.random.randint(1, 10),
                'Discount': discount,
                'Profit': round(profit, 2)
            })
            
        df = pd.DataFrame(data)
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        return df

    def initialize_db(self):
        """Generates data if it doesn't exist and saves to SQLite."""
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Check if table exists
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales_data'")
        table_exists = cursor.fetchone()
        conn.close()
        
        if not table_exists:
            print("Initializing database with sample data...")
            df = self.generate_sample_data()
            df.to_sql('sales_data', self.engine, if_exists='replace', index=False)
            print(f"Database initialized at {self.db_path}")
        else:
            print("Database already exists.")

    def load_data(self):
        """Loads data from SQLite into a DataFrame."""
        return pd.read_sql('sales_data', self.engine)

if __name__ == "__main__":
    dm = DataManager()
    dm.initialize_db()
    df = dm.load_data()
    print(df.head())
    print(f"Total rows: {len(df)}")
