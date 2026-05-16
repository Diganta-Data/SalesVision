import streamlit as st
import pandas as pd
import os
from src.data_manager import DataManager

# Page Configuration
st.set_page_config(
    page_title="SalesVision - AI Retail Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if os.path.exists('assets/style.css'):
    local_css('assets/style.css')

# Initialize Data
@st.cache_data
def get_cached_data():
    dm = DataManager()
    dm.initialize_db()
    return dm.load_data()

df = get_cached_data()

# Sidebar Navigation
st.sidebar.title("🚀 SalesVision")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Executive Overview", "📦 Product Analytics", "👥 Customer Insights", "📈 Sales Forecasting", "🤖 Ask AI"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**SalesVision AI**  
Empowering retail decisions with predictive intelligence.
""")

# Home Page / Executive Overview logic
if page == "🏠 Executive Overview":
    st.title("Executive Sales Overview")
    st.markdown("---")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_margin = (total_profit / total_sales) * 100
    total_orders = df['Order_ID'].nunique()
    
    with col1:
        st.metric("Total Revenue", f"${total_sales:,.0f}", "+12%")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.0f}", "+8%")
    with col3:
        st.metric("Profit Margin", f"{avg_margin:.1f}%", "-2%")
    with col4:
        st.metric("Total Orders", f"{total_orders:,}", "+15%")
        
    st.markdown("---")
    
    # Main Dashboard Visuals
    import plotly.express as px
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Sales Trend (Monthly)")
        df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
        monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()
        fig_trend = px.line(monthly_sales, x='Month', y='Sales', template='plotly_dark',
                           color_discrete_sequence=['#818cf8'])
        fig_trend.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🌎 Sales by Region")
        region_sales = df.groupby('Region')['Sales'].sum().reset_index()
        # FIX: Changed sequential color name to a valid one (ice)
        fig_pie = px.pie(region_sales, values='Sales', names='Region', hole=0.5,
                        template='plotly_dark', color_discrete_sequence=px.colors.sequential.ice)
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                             margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📦 Product Analytics":
    from src.ui.product_analytics import show_product_analytics
    show_product_analytics(df)

elif page == "👥 Customer Insights":
    from src.ui.customer_analytics import show_customer_analytics
    show_customer_analytics(df)

elif page == "📈 Sales Forecasting":
    from src.ui.forecasting import show_forecasting
    show_forecasting(df)

elif page == "🤖 Ask AI":
    st.title("AI Assistant")
    st.markdown("Ask anything about your retail data.")
    
    user_query = st.text_input("Enter your query (e.g., 'What was the top category in North region?')")
    if user_query:
        st.info("I am analyzing the data for you...")
        # Simple rule-based/regex mock for AI
        if "top category" in user_query.lower():
            top_cat = df.groupby('Category')['Sales'].sum().idxmax()
            st.success(f"The top category is **{top_cat}**.")
        elif "profit" in user_query.lower():
            st.success(f"The total profit across all regions is **${total_profit:,.2f}**.")
        else:
            st.warning("That's an interesting question! Based on the current dataset, I'm still learning to answer complex queries.")
