import requests
import pandas as pd
import numpy as np
import json
import os
import random
import time
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_stock_data(ticker_symbol, period="1y"):
    """
    Get historical stock data for a specific ticker symbol.
    
    Args:
        ticker_symbol (str): The stock ticker symbol
        period (str): Time period for data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
    Returns:
        pd.DataFrame: DataFrame containing the historical stock data
    """
    try:
        # In a real implementation, you would use yfinance or another API
        # For simulation, we'll generate synthetic data
        logger.info(f"Getting stock data for {ticker_symbol} with period {period}")
        
        # Generate date range
        end_date = datetime.now()
        
        # Determine start date based on period
        if period == "1d":
            start_date = end_date - timedelta(days=1)
            freq = "1H"
        elif period == "5d":
            start_date = end_date - timedelta(days=5)
            freq = "2H"
        elif period == "1mo":
            start_date = end_date - timedelta(days=30)
            freq = "1D"
        elif period == "3mo":
            start_date = end_date - timedelta(days=90)
            freq = "1D"
        elif period == "6mo":
            start_date = end_date - timedelta(days=180)
            freq = "1D"
        elif period == "1y":
            start_date = end_date - timedelta(days=365)
            freq = "1D"
        elif period == "2y":
            start_date = end_date - timedelta(days=730)
            freq = "3D"
        elif period == "5y":
            start_date = end_date - timedelta(days=1825)
            freq = "1W"
        else:  # Default to 1y
            start_date = end_date - timedelta(days=365)
            freq = "1D"
        
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
        
        # Generate synthetic prices based on ticker symbol
        ticker_hash = sum(ord(c) for c in ticker_symbol) % 100
        base_price = 50 + ticker_hash  # Different base price for different tickers
        
        # Generate a random walk
        random_walk = np.random.normal(0, 1, size=len(date_range)).cumsum() * 0.5
        
        # Add a trend component based on ticker
        trend_factor = (ticker_hash % 10 - 5) / 10  # Range: -0.5 to 0.4
        trend = np.linspace(0, len(date_range) * trend_factor, len(date_range))
        
        # Add some seasonality
        seasonality = np.sin(np.linspace(0, 10, len(date_range))) * 2
        
        # Calculate prices
        prices = base_price + random_walk + trend + seasonality
        
        # Create a DataFrame
        df = pd.DataFrame({
            'Date': date_range,
            'Open': prices,
            'High': prices + np.random.uniform(0.1, 1, size=len(date_range)),
            'Low': prices - np.random.uniform(0.1, 1, size=len(date_range)),
            'Close': prices + np.random.uniform(-0.5, 0.5, size=len(date_range)),
            'Volume': np.random.randint(100000, 10000000, size=len(date_range))
        })
        
        # Ensure Open, High, Low, Close make sense
        df['High'] = df[['Open', 'High', 'Close']].max(axis=1)
        df['Low'] = df[['Open', 'Low', 'Close']].min(axis=1)
        
        # Calculate Adjusted Close (simulating dividends and splits)
        df['Adj Close'] = df['Close']
        
        # Ensure all values are positive
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
            df[col] = df[col].apply(lambda x: max(0.1, x))
        
        return df
    except Exception as e:
        logger.error(f"Error in get_stock_data: {str(e)}")
        # Return an empty DataFrame with correct columns
        return pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'])

def get_portfolio_metrics():
    """
    Calculate metrics for a user's portfolio.
    In a production environment, this would use real portfolio data.
    
    Returns:
        dict: Dictionary containing portfolio metrics
    """
    try:
        # In a real implementation, you would fetch this from a database
        # For demonstration, we'll use synthetic data
        
        # Generate a date range for the past year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate portfolio value over time
        initial_value = 1000000  # $1M initial portfolio
        
        # Create a base trend with some growth
        growth_factor = 0.085  # 8.5% annual growth
        trend = np.linspace(0, growth_factor, len(date_range))
        
        # Add random walk component
        random_walk = np.random.normal(0, 0.01, size=len(date_range)).cumsum()
        
        # Add some seasonality
        seasonality = np.sin(np.linspace(0, 12, len(date_range))) * 0.03
        
        # Calculate portfolio values
        values = initial_value * (1 + trend + random_walk + seasonality)
        
        # Create a dataframe
        portfolio_df = pd.DataFrame({
            'date': date_range,
            'value': values
        })
        
        # Calculate metrics
        current_value = portfolio_df['value'].iloc[-1]
        starting_value = portfolio_df['value'].iloc[0]
        growth_pct = ((current_value / starting_value) - 1) * 100
        
        # Daily returns
        portfolio_df['daily_return'] = portfolio_df['value'].pct_change()
        
        # Calculate volatility (annualized)
        volatility = portfolio_df['daily_return'].std() * np.sqrt(252) * 100
        
        result = {
            'date_range': date_range,
            'value_series': values,
            'current_value': int(current_value),
            'growth_rate': round(growth_pct, 1),
            'volatility': round(volatility, 2),
            'date': date_range,
            'value': values
        }
        
        return result
    except Exception as e:
        logger.error(f"Error in get_portfolio_metrics: {str(e)}")
        # Return default values
        return {
            'current_value': 1000000,
            'growth_rate': 5.0,
            'volatility': 12.5,
            'date': [datetime.now()],
            'value': [1000000]
        }

def get_fund_data(fund_category=None, limit=10):
    """
    Get fund data based on category.
    
    Args:
        fund_category (str): Category of funds (e.g., 'Technology', 'Global', 'ESG')
        limit (int): Maximum number of funds to return
        
    Returns:
        list: List of dictionaries containing fund data
    """
    try:
        # In a real implementation, you would fetch this from an API or database
        # For demonstration, we'll use synthetic data
        
        # Define some fund categories and subcategories
        categories = {
            'Technology': ['Tech Giants', 'Emerging Tech', 'Biotech', 'Fintech', 'AI & Robotics'],
            'Global': ['Developed Markets', 'Emerging Markets', 'Global Diversified', 'International Small Cap'],
            'ESG': ['Clean Energy', 'Sustainable Investments', 'Social Impact', 'Green Bonds'],
            'Fixed Income': ['Government Bonds', 'Corporate Bonds', 'High Yield', 'Municipal Bonds'],
            'Sector': ['Healthcare', 'Real Estate', 'Energy', 'Materials', 'Consumer Goods'],
            'Alternative': ['Commodities', 'Hedge Fund Strategies', 'Private Equity', 'Infrastructure']
        }
        
        # Generate fund names
        prefixes = ['Global', 'Emerging', 'Strategic', 'Enhanced', 'Dynamic', 'Sustainable', 'Prime', 'Select', 'Value']
        core_names = ['Growth', 'Income', 'Balanced', 'Opportunity', 'Leaders', 'Index', 'Capital', 'Alpha', 'Beta']
        suffixes = ['Fund', 'ETF', 'Portfolio', 'Trust', 'Allocation', 'Strategy']
        
        # Generate a list of funds
        all_funds = []
        
        # Seed random for consistent results
        random.seed(42)
        
        for category, subcategories in categories.items():
            for subcategory in subcategories:
                # Generate a few funds for each subcategory
                for _ in range(random.randint(1, 3)):
                    prefix = random.choice(prefixes)
                    core = random.choice(core_names)
                    suffix = random.choice(suffixes)
                    
                    # Generate the fund name
                    fund_name = f"{prefix} {subcategory} {core} {suffix}"
                    
                    # Generate fund ticker (random 3-5 letter combination)
                    ticker_length = random.randint(3, 5)
                    ticker = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=ticker_length))
                    
                    # Generate performance metrics
                    one_year_return = random.uniform(-10, 30)
                    three_year_return = random.uniform(-5, 25)
                    five_year_return = random.uniform(0, 20)
                    ytd_return = random.uniform(-15, 25)
                    
                    # Risk metrics
                    sharpe_ratio = random.uniform(0.5, 2.5)
                    volatility = random.uniform(5, 25)
                    
                    # Fund details
                    expense_ratio = random.uniform(0.05, 1.5)
                    aum = random.uniform(10, 10000)  # Assets under management in millions
                    min_investment = random.choice([0, 1000, 2500, 5000, 10000, 25000, 50000])
                    
                    # Risk score (1-5, higher is riskier)
                    risk_score = random.randint(1, 5)
                    
                    fund = {
                        'name': fund_name,
                        'ticker': ticker,
                        'category': category,
                        'subcategory': subcategory,
                        'one_year_return': round(one_year_return, 2),
                        'three_year_return': round(three_year_return, 2),
                        'five_year_return': round(five_year_return, 2),
                        'ytd_return': round(ytd_return, 2),
                        'sharpe_ratio': round(sharpe_ratio, 2),
                        'volatility': round(volatility, 2),
                        'expense_ratio': round(expense_ratio, 2),
                        'aum': round(aum, 2),
                        'min_investment': min_investment,
                        'risk_score': risk_score,
                        'inception_date': (datetime.now() - timedelta(days=random.randint(365, 7300))).strftime('%Y-%m-%d')
                    }
                    
                    all_funds.append(fund)
        
        # If a category is specified, filter by it
        if fund_category:
            filtered_funds = [f for f in all_funds if f['category'].lower() == fund_category.lower()]
        else:
            filtered_funds = all_funds
        
        # Sort by one_year_return (default sorting)
        sorted_funds = sorted(filtered_funds, key=lambda x: x['one_year_return'], reverse=True)
        
        # Return limited number of funds
        return sorted_funds[:limit]
    except Exception as e:
        logger.error(f"Error in get_fund_data: {str(e)}")
        return []
