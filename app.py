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

# --- HEADER (NO EMOJIS, PREMIUM SVG LOGO) ---
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 10px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
            <span style="font-size: 1.4rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.03em;">
                SalesVision <span style="color: #818cf8; font-weight: 800;">Enterprise</span>
            </span>
        </div>
        <div class="header-status-badge">
            Systems Operational
        </div>
    </div>
""", unsafe_allow_html=True)

# Helper function to guess column matches
def guess_column(columns, possible_names, default=""):
    for col in columns:
        if col.lower().replace(" ", "_").strip() in possible_names:
            return col
    # Partial matching
    for col in columns:
        for p in possible_names:
            if p in col.lower() or col.lower() in p:
                return col
    return default if default in columns else (columns[0] if len(columns) > 0 else "")

# --- DATA ENGINE ---
@st.cache_data
def load_sample_data():
    dm = DataManager()
    dm.initialize_db()
    return dm.load_data()

# Session State for Mapping
if 'mapped_df' not in st.session_state:
    st.session_state.mapped_df = None
if 'active_uploader_file' not in st.session_state:
    st.session_state.active_uploader_file = None

# Sidebar Setup
st.sidebar.markdown('<p class="sidebar-title">DATA MANAGEMENT</p>', unsafe_allow_html=True)
data_source = st.sidebar.radio("Data Source Selection", ["System Sample", "Upload CSV"], label_visibility="collapsed")

# Reset states if switching back to system sample
if data_source == "System Sample":
    df = load_sample_data()
    st.session_state.mapped_df = None
    st.session_state.active_uploader_file = None
else:
    uploaded_file = st.sidebar.file_uploader("Upload Transaction Dataset", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        # Check if new file has been uploaded
        if st.session_state.active_uploader_file != uploaded_file.name:
            try:
                raw_df = pd.read_csv(uploaded_file)
                st.session_state.raw_df = raw_df
                st.session_state.active_uploader_file = uploaded_file.name
                st.session_state.mapped_df = None  # Reset mapping to force new mapping
            except Exception as e:
                st.sidebar.error(f"Failed to read CSV: {e}")
                
        if 'raw_df' in st.session_state:
            raw_columns = list(st.session_state.raw_df.columns)
            
            # Check if raw_df already fits the standard schema exactly
            required_cols = ['Order_Date', 'Sales', 'Profit', 'Category', 'Sub_Category', 'Region', 'Customer_ID', 'Order_ID']
            missing_cols = [c for c in required_cols if c not in raw_columns]
            
            if len(missing_cols) == 0 and st.session_state.mapped_df is None:
                # Direct match, no mapping needed
                mapped = st.session_state.raw_df.copy()
                mapped['Order_Date'] = pd.to_datetime(mapped['Order_Date'])
                st.session_state.mapped_df = mapped
                st.sidebar.success("Direct Schema Matched!")
            
            # If mapping is still required
            if st.session_state.mapped_df is None:
                df = None  # Set df to None to force showing mapping screen in the main layout
            else:
                df = st.session_state.mapped_df
        else:
            df = load_sample_data()
    else:
        st.sidebar.info("Awaiting transactional CSV dataset.")
        df = load_sample_data()

# Navigation Sidebar
st.sidebar.markdown('<p class="sidebar-title">PLATFORM NAVIGATION</p>', unsafe_allow_html=True)
page = st.sidebar.selectbox(
    "Menu Options",
    ["Executive Overview", "Product Analytics", "Customer Insights", "Sales Forecasting", "Business Query Engine"],
    label_visibility="collapsed"
)

# --- MAIN CONTENT BODY ---
st.markdown("<br><br><br>", unsafe_allow_html=True) # Spacer for header

# Handle Column Mapping UI if df is None (which means file is uploaded but not mapped yet)
if df is None:
    st.title("Schema Alignment Required")
    st.markdown("Your uploaded CSV columns do not perfectly align with the SalesVision schema. Please map your fields below to enable analytical calculations.")
    
    st.markdown('<div class="glass-card glow-purple">', unsafe_allow_html=True)
    st.subheader("Align CSV Fields")
    
    raw_cols = list(st.session_state.raw_df.columns)
    
    col_a, col_b = st.columns(2)
    with col_a:
        map_date = st.selectbox("Order Date Column (Time axis)", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["order_date", "order date", "date", "timestamp", "time", "tx_date"])))
        map_sales = st.selectbox("Sales/Revenue Column (Value axis)", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["sales", "revenue", "amount", "price", "turnover"])))
        map_profit = st.selectbox("Profit Column (Net earnings)", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["profit", "earnings", "net", "gain"])))
        map_category = st.selectbox("Product Category Column", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["category", "dept", "class"])))
        
    with col_b:
        map_subcat = st.selectbox("Sub-Category Column", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["sub_category", "sub-category", "subcategory", "type", "item"])))
        map_region = st.selectbox("Geographic Region Column", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["region", "state", "city", "location"])))
        map_customer = st.selectbox("Customer Identifier Column", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["customer_id", "customer id", "customer", "client", "cust_id"])))
        map_order = st.selectbox("Order/Transaction Identifier Column", raw_cols, index=raw_cols.index(guess_column(raw_cols, ["order_id", "order id", "order", "tx_id", "invoice"])))

    if st.button("Apply Field Mapping & Initialize"):
        try:
            mapped = pd.DataFrame()
            mapped['Order_Date'] = pd.to_datetime(st.session_state.raw_df[map_date])
            mapped['Sales'] = pd.to_numeric(st.session_state.raw_df[map_sales])
            mapped['Profit'] = pd.to_numeric(st.session_state.raw_df[map_profit])
            mapped['Category'] = st.session_state.raw_df[map_category].astype(str)
            mapped['Sub_Category'] = st.session_state.raw_df[map_subcat].astype(str)
            mapped['Region'] = st.session_state.raw_df[map_region].astype(str)
            mapped['Customer_ID'] = st.session_state.raw_df[map_customer].astype(str)
            mapped['Order_ID'] = st.session_state.raw_df[map_order].astype(str)
            
            # Optional column defaults
            mapped['Quantity'] = pd.to_numeric(st.session_state.raw_df[guess_column(raw_cols, ["quantity", "qty", "count"], raw_cols[0])], errors='coerce').fillna(1)
            mapped['Discount'] = pd.to_numeric(st.session_state.raw_df[guess_column(raw_cols, ["discount", "disc"], raw_cols[0])], errors='coerce').fillna(0)
            
            st.session_state.mapped_df = mapped
            st.rerun()
        except Exception as e:
            st.error(f"Mapping failed. Ensure selected columns contain numeric/datetime data where appropriate. Detail: {e}")
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Uploaded Data Preview")
    st.dataframe(st.session_state.raw_df.head(10), use_container_width=True)

else:
    # Render Mapped Data Source Status in Sidebar
    if data_source == "Upload CSV":
        st.sidebar.markdown(f'<span class="glow-tag glow-tag-success">Data Active: {uploaded_file.name}</span>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<span class="glow-tag glow-tag-primary">Data Active: System Sample</span>', unsafe_allow_html=True)

    # --- PAGES ROUTING ---
    if page == "Executive Overview":
        st.title("Executive Intelligence")
        st.markdown("Global sales performance and operational KPIs.")
        
        # Display mapped state indicator if custom file is active
        if data_source == "Upload CSV":
            st.info("Operating on active user uploaded dataset with standard schema alignment.")
            
        # Top level KPIs
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            st.metric("Gross Revenue", f"${df['Sales'].sum():,.0f}")
        with c2: 
            st.metric("Net Profit", f"${df['Profit'].sum():,.0f}")
        with c3: 
            margin = (df['Profit'].sum() / df['Sales'].sum() * 100) if df['Sales'].sum() != 0 else 0
            st.metric("Operating Margin", f"{margin:.1f}%")
        with c4: 
            st.metric("Order Volume", f"{len(df['Order_ID'].unique()):,}")
        
        st.markdown("---")
        
        import plotly.express as px
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Revenue Timeline")
            # Group sales by Month
            df_copy = df.copy()
            df_copy['Month'] = df_copy['Order_Date'].dt.to_period('M').astype(str)
            monthly = df_copy.groupby('Month')[['Sales', 'Profit']].sum().reset_index()
            
            # Elegant Dual-Trace Area Plot
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Sales'], fill='tozeroy', name='Revenue', line=dict(color='#818cf8', width=2.5)))
            fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Profit'], fill='tozeroy', name='Net Profit', line=dict(color='#c084fc', width=2)))
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Timeline",
                yaxis_title="Amount ($)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.subheader("Regional Mix")
            region = df.groupby('Region')['Sales'].sum().reset_index()
            fig = px.pie(region, values='Sales', names='Region', hole=0.65, template='plotly_dark', color_discrete_sequence=px.colors.sequential.Purp)
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

    elif page == "Business Query Engine":
        from src.ui.query_engine import show_query_engine
        show_query_engine(df)

# --- FOOTER ---
st.markdown("""
    <div class="main-footer">
        &copy; 2024 SalesVision Enterprise | Unified Sales Intelligence Engine | Created by Diganta Maity
    </div>
""", unsafe_allow_html=True)
