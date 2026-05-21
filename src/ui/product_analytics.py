import streamlit as st
import plotly.express as px
import pandas as pd

def show_product_analytics(df):
    st.title("Product Performance")
    st.markdown("In-depth analysis of inventory, category hierarchy, and product profitability.")
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.multiselect("Select Categories", options=df['Category'].unique(), default=df['Category'].unique())
    with col2:
        region_filter = st.multiselect("Select Regions", options=df['Region'].unique(), default=df['Region'].unique())
        
    filtered_df = df[df['Category'].isin(category_filter) & df['Region'].isin(region_filter)]
    
    if filtered_df.empty:
        st.warning("No records matched the selected category and region filters.")
        return
        
    # Treemap hierarchy (Instead of just simple sunburst, Treemap is much cleaner for standard dashboard layout)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Category Revenue Share (Treemap)")
    fig_tree = px.treemap(filtered_df, path=['Category', 'Sub_Category'], values='Sales',
                         template='plotly_dark', color='Sales', color_continuous_scale='Purp')
    fig_tree.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig_tree, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Profitability Quadrant Matrix
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Sub-Category Profitability Matrix")
    st.markdown("This matrix segments sub-categories based on their average Discount (X) and average Profit Margin (Y).")
    
    # Group by sub-category
    sub_perf = filtered_df.groupby('Sub_Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Discount': 'mean'
    }).reset_index()
    sub_perf['Margin'] = (sub_perf['Profit'] / sub_perf['Sales']) * 100
    
    # Identify quadrants
    median_disc = sub_perf['Discount'].median()
    median_margin = sub_perf['Margin'].median()
    
    def assign_quadrant(row):
        if row['Margin'] >= median_margin and row['Discount'] < median_disc:
            return "Star Performers"
        elif row['Margin'] >= median_margin and row['Discount'] >= median_disc:
            return "Promo-Driven"
        elif row['Margin'] < median_margin and row['Discount'] < median_disc:
            return "Underperformers"
        else:
            return "Discounted Drag"
            
    sub_perf['Quadrant'] = sub_perf.apply(assign_quadrant, axis=1)
    
    fig_scatter = px.scatter(sub_perf, x='Discount', y='Margin', color='Quadrant',
                            size='Sales', text='Sub_Category', template='plotly_dark',
                            title="Strategic Positioning Map (Size corresponds to Sales Volume)",
                            color_discrete_map={
                                "Star Performers": "#34d399",
                                "Promo-Driven": "#818cf8",
                                "Underperformers": "#fbbf24",
                                "Discounted Drag": "#f87171"
                            })
    fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Dynamic Profit Target Tracker
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Dynamic Profit Target Threshold Tracker")
    st.markdown("Set your custom target profit margin to immediately filter out and highlight products and sub-categories meeting expectations.")
    
    target_margin = st.slider("Select Target Profit Margin (%)", min_value=-50, max_value=50, value=15, step=1)
    
    # Highlight sub-categories meeting the target
    sub_perf['Status'] = sub_perf['Margin'].apply(lambda m: "Achieved Target" if m >= target_margin else "Below Target")
    
    # Style the output table
    def style_status(val):
        color = '#10b981' if val == 'Achieved Target' else '#ef4444'
        return f'color: {color}; font-weight: 700;'
        
    styled_df = sub_perf[['Sub_Category', 'Sales', 'Profit', 'Margin', 'Status']].sort_values('Margin', ascending=False)
    
    # Render with custom column styling
    st.dataframe(
        styled_df.style.format({
            'Sales': '${:,.2f}',
            'Profit': '${:,.2f}',
            'Margin': '{:.2f}%'
        }).map(style_status, subset=['Status']),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
