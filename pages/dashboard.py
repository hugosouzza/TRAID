import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.finance import get_portfolio_metrics, get_stock_data
from utils.news import get_financial_news
from utils.sentiment import analyze_sentiment

def app():
    st.title("Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Tu Portfolio")
        
        # Get portfolio data
        portfolio_data = get_portfolio_metrics()
        
        # Create portfolio chart
        fig = px.line(
            x=portfolio_data['date'], 
            y=portfolio_data['value'], 
            title='Portfolio Value Over Time', 
            labels={'x': 'Date', 'y': 'Value ($)'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Portfolio metrics
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Net Worth", f"${portfolio_data['current_value']:,}")
        metric_col2.metric("Growth Rate", f"{portfolio_data['growth_rate']}% YTD")
        
        # Recent operations
        st.subheader("Operaciones")
        
        operations = [
            {"type": "Compra", "ticker": "NVO", "shares": "75,183", "price": "-39 $", "time": "14:30"},
            {"type": "Compra", "ticker": "ORCL", "shares": "1", "price": "-148.42 $", "time": "16:20"},
            {"type": "Compra", "ticker": "ORCL", "shares": "3", "price": "-445.26 $", "time": "18:20"}
        ]
        
        for op in operations:
            with st.container():
                cols = st.columns([1, 4, 2])
                with cols[0]:
                    st.markdown("📈")
                with cols[1]:
                    st.markdown(f"**{op['type']} {op['ticker']}**")
                    st.markdown(f"{op['shares']} acciones")
                with cols[2]:
                    st.markdown(f"**{op['price']}**")
                    st.markdown(f"{op['time']}")
                st.markdown("---")
    
    with col2:
        st.subheader("Market Sentiment")
        
        # Get sentiment data
        sentiment_data = analyze_sentiment("$AAPL $MSFT $GOOGL")
        
        # Display sentiment chart
        sentiment_df = pd.DataFrame({
            'Ticker': ['AAPL', 'MSFT', 'GOOGL'],
            'Sentiment': [sentiment_data.get('AAPL', 0), sentiment_data.get('MSFT', 0), sentiment_data.get('GOOGL', 0)]
        })
        
        fig = px.bar(sentiment_df, x='Ticker', y='Sentiment', 
                   title='Market Sentiment Analysis',
                   color='Sentiment',
                   color_continuous_scale=['red', 'yellow', 'green'])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Latest news
        st.subheader("Latest Market News")
        news = get_financial_news(5)
        
        for item in news[:3]:
            st.markdown(f"**{item['title']}**")
            st.markdown(f"{item['summary'][:100]}...")
            st.markdown(f"*{item['source']} - {item['date']}*")
            st.markdown("---")

if __name__ == "__main__":
    app()
