import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from prophet import Prophet
import warnings

warnings.filterwarnings('ignore')

class AnalyticsModels:
    @staticmethod
    def perform_rfm_segmentation(df, n_clusters=4):
        """
        Performs RFM (Recency, Frequency, Monetary) analysis and K-Means clustering.
        """
        # Calculate RFM metrics
        snapshot_date = df['Order_Date'].max() + pd.Timedelta(days=1)
        
        rfm = df.groupby('Customer_ID').agg({
            'Order_Date': lambda x: (snapshot_date - x.max()).days,
            'Order_ID': 'count',
            'Sales': 'sum'
        }).rename(columns={
            'Order_Date': 'Recency',
            'Order_ID': 'Frequency',
            'Sales': 'Monetary'
        })
        
        # Scale the data
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm)
        
        # K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        rfm['Cluster'] = kmeans.fit_transform(rfm_scaled).argmin(axis=1) # Simplified cluster mapping
        
        # Map clusters to meaningful names (logic based on centers)
        centers = rfm.groupby('Cluster').mean()
        # Sort clusters by Monetary value
        sorted_clusters = centers.sort_values('Monetary').index.tolist()
        cluster_map = {
            sorted_clusters[0]: 'At Risk',
            sorted_clusters[1]: 'Potential Loyalists',
            sorted_clusters[2]: 'Loyal Customers',
            sorted_clusters[3]: 'Champions'
        }
        rfm['Segment'] = rfm['Cluster'].map(cluster_map)
        
        return rfm

    @staticmethod
    def forecast_sales(df, periods=30):
        """
        Forecasts daily sales using Prophet.
        """
        # Prepare data for Prophet
        daily_sales = df.groupby('Order_Date')['Sales'].sum().reset_index()
        daily_sales.columns = ['ds', 'y']
        
        model = Prophet(yearly_seasonality=True, daily_seasonality=False)
        model.fit(daily_sales)
        
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

if __name__ == "__main__":
    from data_manager import DataManager
    dm = DataManager()
    df = dm.load_data()
    
    # Test RFM
    rfm = AnalyticsModels.perform_rfm_segmentation(df)
    print("RFM Head:")
    print(rfm.head())
    
    # Test Forecast
    forecast = AnalyticsModels.forecast_sales(df)
    print("\nForecast Head:")
    print(forecast.tail())
