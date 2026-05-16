import streamlit as st
import plotly.graph_objects as go
from src.models import AnalyticsModels
import pandas as pd

def show_forecasting(df):
    st.title("Predictive Demand Forecasting")
    st.markdown("AI-driven projections for future sales cycles.")
    st.markdown("---")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    forecast_days = st.slider("Select Forecast Horizon (Days)", min_value=7, max_value=90, value=30)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Initialize Forecast Model"):
        with st.spinner(f"Computing demand for the next {forecast_days} days..."):
            forecast = AnalyticsModels.forecast_sales(df, periods=forecast_days)
            
            # Historical Data for Plotting
            daily_sales = df.groupby('Order_Date')['Sales'].sum().reset_index()
            daily_sales.columns = ['ds', 'y']
            
            # Create Plotly Figure
            fig = go.Figure()
            
            # Historical
            fig.add_trace(go.Scatter(x=daily_sales['ds'], y=daily_sales['y'], 
                                    name='Historical Sales', line=dict(color='#94a3b8')))
            
            # Forecast
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], 
                                    name='Predicted Sales', line=dict(color='#818cf8', width=3)))
            
            # Confidence Interval
            fig.add_trace(go.Scatter(
                x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
                y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
                fill='toself',
                fillcolor='rgba(129, 140, 248, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=False,
                name='Confidence Interval'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                xaxis_title="Date",
                yaxis_title="Revenue ($)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Forecast KPIs
            total_forecasted = forecast.tail(forecast_days)['yhat'].sum()
            avg_daily_forecast = forecast.tail(forecast_days)['yhat'].mean()
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Forecasted Gross Revenue", f"${total_forecasted:,.2f}")
            with c2:
                st.metric("Avg Daily Predicted Sales", f"${avg_daily_forecast:,.2f}")
                
            st.markdown("### Projection Dataset")
            st.dataframe(forecast.tail(forecast_days), use_container_width=True)
    else:
        st.info("Execute the model to generate demand projections.")
