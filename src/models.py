import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from prophet import Prophet
import warnings

warnings.filterwarnings('ignore')

class AnalyticsModels:
    @staticmethod
    def calculate_kmeans_elbow(df, max_clusters=10):
        """
        Computes WCSS (Within-Cluster Sum of Squares) for K-Means elbow plot.
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
        
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm)
        
        wcss = []
        # Support datasets with fewer samples than max_clusters
        limit = min(max_clusters + 1, len(rfm))
        for k in range(1, limit):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(rfm_scaled)
            wcss.append(float(kmeans.inertia_))
            
        return list(range(1, len(wcss) + 1)), wcss

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
        if len(sorted_clusters) == 4:
            cluster_map = {
                sorted_clusters[0]: 'At Risk',
                sorted_clusters[1]: 'Potential Loyalists',
                sorted_clusters[2]: 'Loyal Customers',
                sorted_clusters[3]: 'Champions'
            }
        else:
            cluster_map = {}
            for rank, cluster_id in enumerate(sorted_clusters):
                if rank == 0:
                    cluster_map[cluster_id] = 'At Risk'
                elif rank == len(sorted_clusters) - 1:
                    cluster_map[cluster_id] = 'Champions'
                elif rank == 1:
                    cluster_map[cluster_id] = 'Potential Loyalists'
                else:
                    cluster_map[cluster_id] = f'Cohort {rank + 1}'
        rfm['Segment'] = rfm['Cluster'].map(cluster_map)
        
        return rfm

    @staticmethod
    def forecast_sales(df, periods=30, freq='D'):
        """
        Forecasts sales using Prophet with configurable frequency ('D', 'W', 'M').
        """
        # Prepare data for Prophet
        df_copy = df.copy()
        df_copy['Order_Date'] = pd.to_datetime(df_copy['Order_Date']).dt.tz_localize(None)
        
        if freq == 'W':
            resampled = df_copy.set_index('Order_Date').resample('W')['Sales'].sum().reset_index()
        elif freq == 'M':
            resampled = df_copy.set_index('Order_Date').resample('MS')['Sales'].sum().reset_index()
        else:
            resampled = df_copy.groupby('Order_Date')['Sales'].sum().reset_index()
            
        resampled.columns = ['ds', 'y']
        
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True if freq == 'D' else False,
            daily_seasonality=False
        )
        model.fit(resampled)
        
        future = model.make_future_dataframe(periods=periods, freq=freq)
        forecast = model.predict(future)
        
        cols = ['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend']
        if 'weekly' in forecast.columns:
            cols.append('weekly')
        if 'yearly' in forecast.columns:
            cols.append('yearly')
            
        return forecast[cols]

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
