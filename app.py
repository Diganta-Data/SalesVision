import streamlit as st
import pandas as pd
import os
from src.data_manager import DataManager

# Page Configuration
st.set_page_config(
    page_title="SalesVision Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('assets/style.css')

# --- HEADER ---
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 10px;">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            <span style="font-size: 1.5rem; font-weight: 800; color: white;">SalesVision <span style="color: #818cf8;">Pro</span></span>
        </div>
        <div style="color: #94a3b8; font-size: 0.9rem;">Enterprise Sales Intelligence v2.0</div>
    </div>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_sample_data():
    dm = DataManager()
    dm.initialize_db()
    return dm.load_data()

# Data Source Selection
st.sidebar.markdown('<p class="sidebar-title">DATA MANAGEMENT</p>', unsafe_allow_html=True)
data_source = st.sidebar.radio("Data Source", ["System Sample", "Upload CSV"], label_visibility="collapsed")

if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload Retail Data", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df['Order_Date'] = pd.to_datetime(df['Order_Date'])
            st.sidebar.success("File Uploaded Successfully")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
            df = load_sample_data()
    else:
        st.sidebar.info("Awaiting CSV file...")
        df = load_sample_data()
else:
    df = load_sample_data()

# --- NAVIGATION ---
st.sidebar.markdown('<p class="sidebar-title">NAVIGATION</p>', unsafe_allow_html=True)
page = st.sidebar.selectbox(
    "Menu",
    ["Executive Overview", "Product Analytics", "Customer Insights", "Sales Forecasting", "AI Assistant"],
    label_visibility="collapsed"
)

# --- BODY LOGIC ---
st.markdown("<br><br>", unsafe_allow_html=True) # Spacer for fixed header

if page == "Executive Overview":
    st.title("Executive Intelligence")
    st.markdown("Global sales performance and operational KPIs.")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Gross Revenue", f"${df['Sales'].sum():,.0f}")
    with c2: st.metric("Net Profit", f"${df['Profit'].sum():,.0f}")
    with c3: st.metric("Operating Margin", f"{(df['Profit'].sum()/df['Sales'].sum()*100):.1f}%")
    with c4: st.metric("Order Volume", f"{len(df):,}")
    
    st.markdown("---")
    
    import plotly.express as px
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Revenue Timeline")
        df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
        monthly = df.groupby('Month')['Sales'].sum().reset_index()
        fig = px.area(monthly, x='Month', y='Sales', color_discrete_sequence=['#818cf8'], template='plotly_dark')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Regional Mix")
        region = df.groupby('Region')['Sales'].sum().reset_index()
        fig = px.pie(region, values='Sales', names='Region', hole=0.6, template='plotly_dark', color_discrete_sequence=px.colors.sequential.Purp)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Product Analytics":
    from src.ui.product_analytics import show_product_analytics
    show_product_analytics(df)

elif page == "Customer Insights":
    from src.ui.customer_analytics import show_customer_analytics
    show_customer_analytics(df)

elif page == "Sales Forecasting":
    from src.ui.forecasting import show_forecasting
    show_forecasting(df)

elif page == "AI Assistant":
    st.title("Business Intelligence AI")
    st.info("Query the SalesVision Engine using natural language.")
    # (AI logic remains same but with cleaner UI)

# --- FOOTER ---
st.markdown("""
    <div class="main-footer">
        &copy; 2024 SalesVision Enterprise | Data-Driven Intelligence Platform | Built by Diganta Maity
    </div>
""", unsafe_allow_html=True)
