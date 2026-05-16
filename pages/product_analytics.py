import streamlit as st
import plotly.express as px

def show_product_analytics(df):
    st.title("Product Performance Analytics")
    st.markdown("---")
    
    # Filters for this page
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.multiselect("Select Categories", options=df['Category'].unique(), default=df['Category'].unique())
    with col2:
        region_filter = st.multiselect("Select Regions", options=df['Region'].unique(), default=df['Region'].unique())
        
    filtered_df = df[df['Category'].isin(category_filter) & df['Region'].isin(region_filter)]
    
    # Category Comparison
    st.subheader("Sales by Category & Sub-Category")
    fig_sun = px.sunburst(filtered_df, path=['Category', 'Sub_Category'], values='Sales',
                         template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_sun, use_container_width=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Top 10 Products by Sales")
        top_products = filtered_df.groupby('Sub_Category')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(top_products, x='Sales', y='Sub_Category', orientation='h',
                        template='plotly_dark', color='Sales', color_continuous_scale='Viridis')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        st.subheader("Discount vs. Profitability")
        fig_scatter = px.scatter(filtered_df, x='Discount', y='Profit', color='Category',
                                size='Sales', hover_data=['Sub_Category'], template='plotly_dark')
        st.plotly_chart(fig_scatter, use_container_width=True)
