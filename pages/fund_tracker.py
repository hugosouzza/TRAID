import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add the parent directory to sys.path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.finance import get_fund_data

def app():
    st.title("Fund Tracker")
    
    # Search bar with filter button
    col1, col2 = st.columns([5, 1])
    with col1:
        search_query = st.text_input("Buscar productos", placeholder="Buscar productos")
    with col2:
        st.button("🔍")
    
    # Categories
    st.subheader("Categorías")
    categories_col1, categories_col2, categories_col3, categories_col4 = st.columns(4)
    
    category_filters = {
        "alto_riesgo": categories_col1.button("📈 Alto riesgo"),
        "bajo_riesgo": categories_col2.button("📉 Bajo riesgo"),
        "tecnologia": categories_col3.button("💻 Tecnología"),
        "sectores": categories_col4.button("🏭 Sectores")
    }
    
    # Featured funds
    st.markdown(
        """
        <div style="background-color: #7749F8; color: white; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3>Los Fondos más rentables del mes</h3>
            <p>Echa un vistazo a los fondos que han generado mayor rentabilidad este mes</p>
            <a href="#" style="color: white; text-decoration: underline;">Ver más →</a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Get fund data
    selected_category = None
    if category_filters["alto_riesgo"]:
        selected_category = "Alternative"
    elif category_filters["bajo_riesgo"]:
        selected_category = "Fixed Income"
    elif category_filters["tecnologia"]:
        selected_category = "Technology"
    elif category_filters["sectores"]:
        selected_category = "Sector"
    
    funds = get_fund_data(fund_category=selected_category, limit=10)
    
    # Filter by search query if provided
    if search_query:
        funds = [fund for fund in funds if search_query.lower() in fund['name'].lower() or 
                                           search_query.lower() in fund['ticker'].lower() or
                                           search_query.lower() in fund['category'].lower() or
                                           search_query.lower() in fund['subcategory'].lower()]
    
    # Show top performing funds
    st.subheader("Top Performing Funds")
    
    if funds:
        # Convert to DataFrame for easier display
        funds_df = pd.DataFrame(funds)
        
        # Display top funds in a grid
        num_cols = 3
        rows = (len(funds) + num_cols - 1) // num_cols  # Ceiling division
        
        for row in range(rows):
            cols = st.columns(num_cols)
            for col in range(num_cols):
                idx = row * num_cols + col
                if idx < len(funds):
                    fund = funds[idx]
                    with cols[col]:
                        st.markdown(f"**{fund['name']}**")
                        st.markdown(f"**{fund['ticker']}** | {fund['category']}")
                        st.markdown(f"1Y Return: **{fund['one_year_return']}%**")
                        st.markdown(f"Risk Score: {'⭐' * fund['risk_score']}")
                        st.markdown(f"Expense Ratio: {fund['expense_ratio']}%")
                        st.button("View Details", key=f"view_{idx}")
                        st.markdown("---")
    else:
        st.info("No funds match your criteria. Try adjusting your search or filters.")
    
    # Fund comparison
    st.subheader("Fund Comparison")
    
    if len(funds) >= 2:
        # Allow selecting funds to compare
        fund_options = [fund['name'] for fund in funds]
        selected_funds = st.multiselect("Select funds to compare:", fund_options, default=fund_options[:3] if len(fund_options) >= 3 else fund_options)
        
        if selected_funds:
            # Get data for selected funds
            selected_fund_data = [fund for fund in funds if fund['name'] in selected_funds]
            
            # Create comparison chart for 1-year returns
            returns_data = {
                'Fund': [fund['name'] for fund in selected_fund_data],
                '1Y Return (%)': [fund['one_year_return'] for fund in selected_fund_data],
                '3Y Return (%)': [fund['three_year_return'] for fund in selected_fund_data],
                '5Y Return (%)': [fund['five_year_return'] for fund in selected_fund_data]
            }
            
            returns_df = pd.DataFrame(returns_data)
            
            fig = px.bar(returns_df, x='Fund', y=['1Y Return (%)', '3Y Return (%)', '5Y Return (%)'],
                        title='Performance Comparison',
                        barmode='group',
                        color_discrete_sequence=px.colors.qualitative.Plotly)
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk-return scatter plot
            risk_return_data = {
                'Fund': [fund['name'] for fund in selected_fund_data],
                'Return (%)': [fund['one_year_return'] for fund in selected_fund_data],
                'Risk (Volatility)': [fund['volatility'] for fund in selected_fund_data],
                'Category': [fund['category'] for fund in selected_fund_data],
                'Expense Ratio (%)': [fund['expense_ratio'] for fund in selected_fund_data]
            }
            
            risk_return_df = pd.DataFrame(risk_return_data)
            
            fig2 = px.scatter(risk_return_df, x='Risk (Volatility)', y='Return (%)', 
                             color='Category', size='Expense Ratio (%)',
                             hover_name='Fund', title='Risk-Return Analysis',
                             labels={'Return (%)': 'Return (%)', 'Risk (Volatility)': 'Risk (Volatility)'},
                             color_discrete_sequence=px.colors.qualitative.Plotly)
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Comparison table
            st.subheader("Detailed Comparison")
            
            comparison_table = pd.DataFrame({
                'Fund': [fund['name'] for fund in selected_fund_data],
                'Ticker': [fund['ticker'] for fund in selected_fund_data],
                'Category': [fund['category'] for fund in selected_fund_data],
                'Subcategory': [fund['subcategory'] for fund in selected_fund_data],
                '1Y Return (%)': [fund['one_year_return'] for fund in selected_fund_data],
                '3Y Return (%)': [fund['three_year_return'] for fund in selected_fund_data],
                '5Y Return (%)': [fund['five_year_return'] for fund in selected_fund_data],
                'Expense Ratio (%)': [fund['expense_ratio'] for fund in selected_fund_data],
                'Risk Score': [fund['risk_score'] for fund in selected_fund_data],
                'Min Investment ($)': [fund['min_investment'] for fund in selected_fund_data],
                'AUM ($M)': [fund['aum'] for fund in selected_fund_data]
            })
            
            st.dataframe(comparison_table, use_container_width=True)

if __name__ == "__main__":
    app()
