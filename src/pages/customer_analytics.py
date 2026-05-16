import streamlit as st
import plotly.express as px
from models import AnalyticsModels

def show_customer_analytics(df):
    st.title("Customer Insights & Segmentation")
    st.markdown("---")
    
    with st.spinner("Performing RFM Segmentation..."):
        rfm = AnalyticsModels.perform_rfm_segmentation(df)
        
    # Segment Distribution
    st.subheader("Customer Segment Distribution")
    segment_counts = rfm['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Segment Summary")
        for idx, row in segment_counts.iterrows():
            st.write(f"**{row['Segment']}**: {row['Count']} customers")
            
    with col2:
        fig_pie = px.pie(segment_counts, values='Count', names='Segment', 
                        template='plotly_dark', color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    
    # RFM Scatter
    st.subheader("Recency vs. Frequency vs. Monetary")
    fig_3d = px.scatter_3d(rfm, x='Recency', y='Frequency', z='Monetary',
                          color='Segment', size_max=18, opacity=0.7,
                          template='plotly_dark', title="3D Customer Clusters")
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Detailed Table
    st.subheader("Detailed Customer Data")
    st.dataframe(rfm.sort_values('Monetary', ascending=False).head(50), use_container_width=True)
