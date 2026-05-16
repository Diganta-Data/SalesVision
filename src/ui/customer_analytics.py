import streamlit as st
import plotly.express as px
from src.models import AnalyticsModels

def show_customer_analytics(df):
    st.title("Customer Intelligence")
    st.markdown("Segmentation and behavioral analysis.")
    st.markdown("---")
    
    with st.spinner("Analyzing customer cohorts..."):
        rfm = AnalyticsModels.perform_rfm_segmentation(df)
        
    # Segment Distribution
    st.subheader("Cohort Distribution")
    segment_counts = rfm['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("### Segment Summary")
        for idx, row in segment_counts.iterrows():
            st.write(f"**{row['Segment']}**: {row['Count']} users")
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_pie = px.pie(segment_counts, values='Count', names='Segment', 
                        template='plotly_dark', color_discrete_sequence=px.colors.sequential.Purp)
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    # RFM Scatter
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("3D Behavioral Mapping")
    fig_3d = px.scatter_3d(rfm, x='Recency', y='Frequency', z='Monetary',
                          color='Segment', size_max=18, opacity=0.7,
                          template='plotly_dark')
    fig_3d.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_3d, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed Table
    st.subheader("Customer Master Record")
    st.dataframe(rfm.sort_values('Monetary', ascending=False).head(50), use_container_width=True)
