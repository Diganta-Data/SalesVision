import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from src.models import AnalyticsModels

def show_forecasting(df):
    st.title("Predictive Demand Forecasting")
    st.markdown("AI-driven projections for future sales cycles using Facebook Prophet.")
    st.markdown("---")
    
    # Configure forecasting settings
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Model Configuration Panel")
    
    col_hz, col_fq = st.columns(2)
    with col_fq:
        freq_opt = st.selectbox("Forecast Model Frequency", ["Daily", "Weekly", "Monthly"])
        freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}
        freq = freq_map[freq_opt]
        
    with col_hz:
        # Match horizon depending on frequency
        if freq == "D":
            forecast_periods = st.slider("Select Forecast Horizon (Days)", min_value=7, max_value=90, value=30)
        elif freq == "W":
            forecast_periods = st.slider("Select Forecast Horizon (Weeks)", min_value=4, max_value=26, value=12)
        else:
            forecast_periods = st.slider("Select Forecast Horizon (Months)", min_value=2, max_value=12, value=6)
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Initialize Forecasting Engine"):
        with st.spinner(f"Training Prophet model and projecting next {forecast_periods} {freq_opt.lower()} periods..."):
            forecast = AnalyticsModels.forecast_sales(df, periods=forecast_periods, freq=freq)
            
            # Prepare historical daily sales for plotting and stats
            df_copy = df.copy()
            df_copy['Order_Date'] = pd.to_datetime(df_copy['Order_Date']).dt.tz_localize(None)
            
            if freq == 'W':
                historical = df_copy.set_index('Order_Date').resample('W')['Sales'].sum().reset_index()
            elif freq == 'M':
                historical = df_copy.set_index('Order_Date').resample('MS')['Sales'].sum().reset_index()
            else:
                historical = df_copy.groupby('Order_Date')['Sales'].sum().reset_index()
                
            historical.columns = ['ds', 'y']
            
            # Setup Tabs for Forecast Breakdown
            tab_main, tab_trend, tab_season = st.tabs(["Projection Overview", "Long-term Trend", "Seasonality Profile"])
            
            # Tab 1: Combined Projection Overview
            with tab_main:
                fig = go.Figure()
                
                # Historical Line
                fig.add_trace(go.Scatter(x=historical['ds'], y=historical['y'], 
                                        name='Historical Sales', line=dict(color='#94a3b8', width=1.5)))
                
                # Forecast Line
                fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], 
                                        name='Predicted Demand', line=dict(color='#818cf8', width=3)))
                
                # Confidence Envelope
                fig.add_trace(go.Scatter(
                    x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
                    y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
                    fill='toself',
                    fillcolor='rgba(129, 140, 248, 0.12)',
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip",
                    showlegend=False,
                    name='Confidence Interval'
                ))
                
                fig.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Date Timeline",
                    yaxis_title="Gross Amount ($)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            # Tab 2: Prophet Trend Component
            with tab_trend:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(x=forecast['ds'], y=forecast['trend'], 
                                             name='Trend Component', line=dict(color='#c084fc', width=2.5)))
                fig_trend.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Timeline",
                    yaxis_title="Base Trend ($)"
                )
                st.plotly_chart(fig_trend, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            # Tab 3: Seasonality Breakdowns
            with tab_season:
                has_weekly = 'weekly' in forecast.columns
                has_yearly = 'yearly' in forecast.columns
                
                if not has_weekly and not has_yearly:
                    st.info("Seasonality profile components are calculated only when daily data models are fitted.")
                else:
                    if has_weekly:
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("Weekly Demand Volatility Pattern")
                        # Sort weekly values by day of week
                        forecast['day_of_week'] = forecast['ds'].dt.day_name()
                        weekly_pattern = forecast.groupby('day_of_week')['weekly'].mean().reindex([
                            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
                        ]).reset_index()
                        
                        fig_weekly = go.Figure()
                        fig_weekly.add_trace(go.Scatter(x=weekly_pattern['day_of_week'], y=weekly_pattern['weekly'], 
                                                       mode='lines+markers', line=dict(color='#34d399', width=2.5)))
                        fig_weekly.update_layout(
                            template='plotly_dark',
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_title="Day of the Week",
                            yaxis_title="Deviation ($)"
                        )
                        st.plotly_chart(fig_weekly, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    if has_yearly:
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("Yearly Seasonal Pattern")
                        forecast['month_name'] = forecast['ds'].dt.month_name()
                        yearly_pattern = forecast.groupby('month_name')['yearly'].mean().reindex([
                            'January', 'February', 'March', 'April', 'May', 'June', 
                            'July', 'August', 'September', 'October', 'November', 'December'
                        ]).reset_index()
                        
                        fig_yearly = go.Figure()
                        fig_yearly.add_trace(go.Scatter(x=yearly_pattern['month_name'], y=yearly_pattern['yearly'], 
                                                       mode='lines+markers', line=dict(color='#f87171', width=2.5)))
                        fig_yearly.update_layout(
                            template='plotly_dark',
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_title="Month of the Year",
                            yaxis_title="Deviation ($)"
                        )
                        st.plotly_chart(fig_yearly, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
            # --- ACTIONABLE OPERATIONS & INVENTORY RECOMMENDATIONS (INNOVATIVE) ---
            st.markdown("### Inventory & Operational Intelligence")
            st.markdown("Supply chain decisions calculated dynamically based on forecasted demand volatility.")
            
            # Forecast KPIs
            total_forecasted = forecast.tail(forecast_periods)['yhat'].sum()
            avg_period_forecast = forecast.tail(forecast_periods)['yhat'].mean()
            
            # Calculate standard deviation of historical sales to estimate demand volatility
            hist_std = historical['y'].std() if len(historical) > 1 else 0
            
            # Operational formulas (Safety Stock & Reorder Point)
            lead_time = 7  # assume 7-day standard shipping lead time
            service_level_z = 1.65  # 95% service level z-score
            safety_stock = service_level_z * hist_std * np.sqrt(lead_time) if hist_std > 0 else 0
            
            # ROP depends on average daily sales. If weekly or monthly, adjust avg accordingly
            if freq == 'W':
                daily_avg = avg_period_forecast / 7
            elif freq == 'M':
                daily_avg = avg_period_forecast / 30
            else:
                daily_avg = avg_period_forecast
                
            reorder_point = (daily_avg * lead_time) + safety_stock
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Forecasted Gross Revenue", f"${total_forecasted:,.2f}")
            with c2:
                st.metric("Avg Predicted Demand", f"${avg_period_forecast:,.2f}")
            with c3:
                st.metric("Suggested Safety Stock Value", f"${safety_stock:,.2f}")
            with c4:
                st.metric("Reorder Point (ROP) Value", f"${reorder_point:,.2f}")
                
            st.markdown('<div class="glass-card glow-emerald">', unsafe_allow_html=True)
            st.write(f"**Supply Chain Insight:** To maintain a **95% customer service level** (preventing stockouts) during the standard **7-day lead time**, the operations team should hold **${safety_stock:,.2f}** worth of inventory as Safety Stock. Initiate replenishment orders when inventory levels of forecasted categories drop below the **${reorder_point:,.2f}** Reorder Point.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### Model Projection Outputs")
            # Format output dates
            display_forecast = forecast.tail(forecast_periods).copy()
            display_forecast['ds'] = display_forecast['ds'].dt.strftime('%Y-%m-%d')
            st.dataframe(
                display_forecast.style.format({
                    'yhat': '${:,.2f}',
                    'yhat_lower': '${:,.2f}',
                    'yhat_upper': '${:,.2f}',
                    'trend': '${:,.2f}'
                }),
                use_container_width=True
            )
    else:
        st.info("Adjust the model configuration above and initialize the engine to compile predictions.")
