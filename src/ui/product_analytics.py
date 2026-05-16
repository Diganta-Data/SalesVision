import streamlit as st
import plotly.express as px

def show_product_analytics(df):
    st.title("Product Performance")
    st.markdown("In-depth analysis of inventory and category profitability.")
    st.markdown("---")
    
    # Filters for this page
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.multiselect("Select Categories", options=df['Category'].unique(), default=df['Category'].unique())
    with col2:
        region_filter = st.multiselect("Select Regions", options=df['Region'].unique(), default=df['Region'].unique())
        
    filtered_df = df[df['Category'].isin(category_filter) & df['Region'].isin(region_filter)]
    
    # Category Comparison
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Category Hierarchy")
    fig_sun = px.sunburst(filtered_df, path=['Category', 'Sub_Category'], values='Sales',
                         template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_sun.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sun, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Top Product Sub-Categories")
        top_products = filtered_df.groupby('Sub_Category')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(top_products, x='Sales', y='Sub_Category', orientation='h',
                        template='plotly_dark', color='Sales', color_continuous_scale='Purp')
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Profitability Matrix")
        fig_scatter = px.scatter(filtered_df, x='Discount', y='Profit', color='Category',
                                size='Sales', hover_data=['Sub_Category'], template='plotly_dark')
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
