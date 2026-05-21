import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.models import AnalyticsModels

def show_customer_analytics(df):
    st.title("Customer Cohort Intelligence")
    st.markdown("Scientific user segmentation using RFM (Recency, Frequency, Monetary) clustering.")
    st.markdown("---")
    
    # Introduce Tabs: Segmentation Analytics vs Cluster Optimization
    tab_cohorts, tab_optimize = st.tabs(["Customer Cohorts Map", "Scientific Cluster Optimization"])
    
    with tab_optimize:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("K-Means WCSS Elbow Curve Solver")
        st.markdown("Verify the mathematical validity of your customer segments. The 'Elbow Point' represents the optimal balance between segmentation detail and grouping generalizability.")
        
        if st.button("Run Scientific Elbow Analysis"):
            with st.spinner("Computing within-cluster variance across parameters (K=1 to 10)..."):
                k_values, wcss_scores = AnalyticsModels.calculate_kmeans_elbow(df)
                
                fig_elbow = go.Figure()
                fig_elbow.add_trace(go.Scatter(x=k_values, y=wcss_scores, mode='lines+markers',
                                             line=dict(color='#818cf8', width=3),
                                             marker=dict(size=8, color='#c084fc')))
                
                fig_elbow.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title="Number of Clusters (K)", tickmode='linear'),
                    yaxis=dict(title="Within-Cluster Sum of Squares (WCSS)")
                )
                st.plotly_chart(fig_elbow, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_cohorts:
        # Cohort tuning slider
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Dynamic Segment Configurator")
        st.markdown("Adjust the slider to dynamically run scikit-learn clustering algorithms with your chosen parameter.")
        n_clusters = st.slider("Select Target Customer Clusters", min_value=2, max_value=6, value=4)
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.spinner("Performing RFM cohort segmentation..."):
            rfm = AnalyticsModels.perform_rfm_segmentation(df, n_clusters=n_clusters)
            
        # Segment counts
        segment_counts = rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        col_metrics, col_pie = st.columns([1, 2])
        
        with col_metrics:
            st.markdown('<div class="glass-card glow-purple" style="height: 100%;">', unsafe_allow_html=True)
            st.subheader("Cohort Volumes")
            for idx, row in segment_counts.iterrows():
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 8px 0;">
                        <span style="font-weight: 600; color: #f8fafc;">{row['Segment']}</span>
                        <span class="glow-tag glow-tag-primary">{row['Count']:,} users</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_pie:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig_pie = px.pie(segment_counts, values='Count', names='Segment', 
                            template='plotly_dark', color_discrete_sequence=px.colors.sequential.Purp)
            fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Group stats (Averages per cluster)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Cohort Averages Profile")
        cohort_stats = rfm.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).reset_index().rename(columns={
            'Recency': 'Avg Recency (Days)',
            'Frequency': 'Avg Frequency (Orders)',
            'Monetary': 'Avg Monetary ($)'
        })
        
        st.dataframe(
            cohort_stats.style.format({
                'Avg Recency (Days)': '{:.1f}',
                'Avg Frequency (Orders)': '{:.1f}',
                'Avg Monetary ($)': '${:,.2f}'
            }),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3D behavioral map
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("3D Behavioral Mapping Space")
        fig_3d = px.scatter_3d(rfm, x='Recency', y='Frequency', z='Monetary',
                              color='Segment', size_max=12, opacity=0.7,
                              template='plotly_dark')
        fig_3d.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, b=0, t=30)
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Customer cohort exporter
        st.subheader("Segment Master Database")
        
        # CSV Export Button
        csv_data = rfm.to_csv(index=True).encode('utf-8')
        st.download_button(
            label="Export Mapped Cohorts CSV",
            data=csv_data,
            file_name="salesvision_cohorts.csv",
            mime="text/csv"
        )
        
        st.dataframe(rfm.sort_values('Monetary', ascending=False).head(50), use_container_width=True)
