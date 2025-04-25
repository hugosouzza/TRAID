import requests
import re
import json
import time
import logging
import random
from textblob import TextBlob
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_sentiment(text):
    """
    Analyze the sentiment of the provided text.
    
    Args:
        text (str): Text to analyze for sentiment
        
    Returns:
        dict: Dictionary with sentiment analysis results
    """
    try:
        # Use TextBlob for sentiment analysis
        analysis = TextBlob(text)
        
        # TextBlob sentiment: polarity is between -1 (negative) and 1 (positive)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        # Normalize polarity to -1 to 1 scale
        normalized_sentiment = polarity
        
        # If analyzing ticker symbols, extract them and provide per-ticker sentiment
        tickers = extract_ticker_symbols(text)
        result = {'overall': normalized_sentiment}
        
        # If tickers are found, break down sentiment by ticker
        if tickers:
            for ticker in tickers:
                # For simulation, assign a sentiment value for each ticker
                # In a real system, you would analyze content specific to each ticker
                ticker_sentiment = simulate_ticker_sentiment(ticker, normalized_sentiment)
                result[ticker] = ticker_sentiment
        
        return result
    except Exception as e:
        logger.error(f"Error in analyze_sentiment: {str(e)}")
        return {'error': str(e), 'overall': 0}

def extract_ticker_symbols(text):
    """
    Extract stock ticker symbols from text.
    
    Args:
        text (str): Text to search for ticker symbols
        
    Returns:
        list: List of found ticker symbols
    """
    # Look for ticker patterns like $AAPL or $BTC
    ticker_pattern = r'\$([A-Z]{1,5})'
    tickers = re.findall(ticker_pattern, text)
    
    # Also look for tickers written without $ but in all caps
    # This is less reliable, so we filter by common ticker length
    word_pattern = r'\b([A-Z]{2,5})\b'
    word_tickers = re.findall(word_pattern, text)
    
    # Combine both lists, removing duplicates
    all_tickers = list(set(tickers + word_tickers))
    
    # Filter out common words that might be mistaken for tickers
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'ANY', 
                   'CAN', 'HAD', 'HAS', 'HER', 'HIS', 'ONE', 'OUR', 'OUT', 'WHO']
    filtered_tickers = [t for t in all_tickers if t not in common_words]
    
    return filtered_tickers

def simulate_ticker_sentiment(ticker, baseline_sentiment):
    """
    Simulate sentiment analysis for a specific ticker.
    In a production environment, this would analyze ticker-specific content.
    
    Args:
        ticker (str): The ticker symbol
        baseline_sentiment (float): Base sentiment to build upon
        
    Returns:
        float: Simulated sentiment score for the ticker
    """
    # Add some randomness to the baseline sentiment
    random_factor = random.uniform(-0.3, 0.3)
    
    # Use the ticker itself to add a deterministic factor
    # This ensures the same ticker gets similar results in a session
    ticker_hash = sum(ord(c) for c in ticker) % 100 / 100  # 0 to 1 range
    ticker_factor = (ticker_hash - 0.5) * 0.4  # -0.2 to 0.2 range
    
    # Combine factors, ensuring result stays in -1 to 1 range
    simulated_sentiment = baseline_sentiment + random_factor + ticker_factor
    simulated_sentiment = max(-1, min(1, simulated_sentiment))
    
    return round(simulated_sentiment, 2)

def analyze_social_media_sentiment(query, platform="twitter"):
    """
    Analyze sentiment from social media for a specific query.
    This is a simulated version - in production you would use APIs.
    
    Args:
        query (str): Search query
        platform (str): Social media platform to analyze
        
    Returns:
        dict: Dictionary with sentiment analysis results
    """
    # In a real application, you would use the Twitter API or other social media APIs
    # For simulation purposes, we'll generate synthetic results
    
    logger.info(f"Analyzing social media sentiment for '{query}' on {platform}")
    
    # Generate simulated results based on the query
    query_hash = sum(ord(c) for c in query) % 100 / 100  # 0 to 1 range
    base_sentiment = (query_hash - 0.5) * 1.4  # Range of -0.7 to 0.7
    
    # Add some randomness
    sentiment_score = base_sentiment + random.uniform(-0.3, 0.3)
    sentiment_score = max(-1, min(1, sentiment_score))  # Ensure range is -1 to 1
    
    # Create a simulated distribution of posts
    total_posts = random.randint(50, 500)
    positive_pct = (sentiment_score + 1) * 50  # Convert to percentage (0-100)
    negative_pct = 100 - positive_pct
    
    results = {
        'query': query,
        'platform': platform,
        'sentiment_score': round(sentiment_score, 2),
        'total_posts_analyzed': total_posts,
        'positive_percentage': round(positive_pct, 1),
        'negative_percentage': round(negative_pct, 1),
        'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return results
