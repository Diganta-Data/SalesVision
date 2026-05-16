# SalesVision Enterprise – AI-Powered Retail Sales Analytics Platform

SalesVision is a professional-grade retail analytics platform built with Streamlit and Python. It provides businesses with actionable insights into their sales performance, customer behavior, and future demand through advanced data visualization and machine learning models.

## 🚀 Features

- **Executive Dashboard**: High-level KPIs (Total Sales, Profit, Margin) with interactive trend charts.
- **Product Analytics**: Deep dive into category performance and top-selling products.
- **Customer Insights**: RFM (Recency, Frequency, Monetary) analysis and K-Means clustering for customer segmentation.
- **Sales Forecasting**: AI-powered demand forecasting using Facebook Prophet.
- **Interactive UI**: Premium glassmorphism design with responsive components.
- **SQL Integration**: Persistent data storage using SQLite.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy, SQL Alchemy
- **Visualization**: Plotly, Seaborn
- **Machine Learning**: Scikit-learn, Prophet, Statsmodels
- **Database**: SQLite

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SalesVision
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run src/app.py
   ```

## 📂 Project Structure

```text
SalesVision/
├── data/               # SQLite database and raw data
├── src/
│   ├── app.py          # Main entry point
│   ├── data_manager.py # Data ingestion & cleaning
│   ├── models.py       # ML model implementations
│   ├── styles.css      # Custom UI styling
│   └── pages/          # Dashboard sub-pages
├── requirements.txt    # Dependency list
└── README.md           # Documentation
```
