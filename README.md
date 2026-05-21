# SalesVision Enterprise – AI-Powered Retail Sales Analytics Platform

SalesVision is a professional-grade corporate analytics platform built with Streamlit and Python. It provides executives and analysts with actionable insights into global sales performance, customer cohorts, and future demand through advanced interactive visualizations, scikit-learn clustering models, and Prophet forecasting.

## 🚀 Key Modules & Capabilities

- **Executive Intelligence**: High-level KPIs (Gross Revenue, Net Profit, Operating Margin, Order Volume) with dynamic area timeline charts and regional share analysis.
- **Universal CSV Schema Mapper**: Drag-and-drop column aligning system to analyze *any* transactional CSV dataset instantly with custom column matching.
- **Product Strategy & Matrix**: Treemap category hierarchy, Profitability Quadrant positioning matrix, and dynamic Target Margin threshold tracking.
- **Customer Cohort Segmentation**: Dynamic K-Means clustering configuration on RFM (Recency, Frequency, Monetary) vectors with interactive Elbow Curve mathematical solver.
- **Predictive Demand Forecasting**: Dynamic daily, weekly, or monthly Prophet model projections with trend breaks, seasonality components, and dynamic operational supply chain Safety Stock / Reorder Point (ROP) guidelines.
- **Business Query NLP Engine**: Secure, offline rule-based natural language processing bar that executes business queries instantly into data and visualizations.

## 🛠️ Tech Stack & Requirements

- **Framework**: Streamlit (Advanced Custom Glassmorphism Theme)
- **Data Engineering**: Pandas, NumPy, SQLAlchemy
- **Interactive Visuals**: Plotly Express & Plotly Graph Objects
- **Algorithms**: Scikit-Learn (K-Means, StandardScaler), Facebook Prophet (Time Series Forecasting)
- **Data Engine**: SQLite (Local persistent database storage)

## 📦 Deployment & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Diganta-Data/SalesVision.git
   cd SalesVision
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application locally**:
   ```bash
   streamlit run app.py
   ```

## 📂 Architecture

```text
SalesVision/
├── assets/
│   └── style.css            # Custom Glassmorphism Style Tokens
├── data/
│   └── sales_vision.db      # Local SQLite database
├── src/
│   ├── ui/
│   │   ├── customer_analytics.py
│   │   ├── forecasting.py
│   │   ├── product_analytics.py
│   │   └── query_engine.py  # NLP Business Query Engine
│   ├── data_manager.py      # Database initialization & loading
│   └── models.py            # K-Means & Prophet prediction algorithms
├── app.py                   # Platform Core Router & Universal Mapper
└── requirements.txt         # Package dependencies list
```
