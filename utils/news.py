import requests
import json
import random
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_financial_news(limit=5):
    """
    Get financial news articles.
    
    Args:
        limit (int): Maximum number of news articles to return
        
    Returns:
        list: List of dictionaries containing news data
    """
    try:
        # In a real implementation, you would use an API like News API
        # For demonstration, we'll create synthetic news data
        logger.info(f"Getting financial news, limit={limit}")
        
        # Sample news sources
        sources = ['Bloomberg', 'CNBC', 'Reuters', 'The Wall Street Journal', 'Financial Times',
                  'MarketWatch', 'Barron\'s', 'Forbes', 'The Economist', 'Investopedia']
        
        # Sample news topics
        topics = [
            'Federal Reserve', 'Interest Rates', 'Inflation', 'GDP Growth', 'Unemployment',
            'Stock Market', 'Crypto', 'Bitcoin', 'IPO', 'Tech Stocks', 'Earnings Season', 
            'Oil Prices', 'Gold', 'Bond Market', 'Housing Market', 'Supply Chain', 
            'Banking Sector', 'Global Trade', 'Climate Investment', 'AI in Finance'
        ]
        
        # Sample title templates
        title_templates = [
            "{topic} Shows Signs of {direction}",
            "Experts Predict {direction} in {topic} for Coming Months",
            "{topic}: What Investors Need to Know",
            "New Report Reveals {direction} Trends in {topic}",
            "{topic} Reaches {superlative} Level Since {timeframe}",
            "Is {topic} the Next Big Investment Opportunity?",
            "How {topic} is Changing the Financial Landscape",
            "Understanding the Impact of {topic} on Your Portfolio",
            "{topic} Faces Uncertainty Amid Market Volatility",
            "The Rise and Fall of {topic}: A Market Analysis"
        ]
        
        # Direction terms
        directions = ['Growth', 'Decline', 'Recovery', 'Volatility', 'Stability', 'Transformation']
        
        # Superlative terms
        superlatives = ['Highest', 'Lowest', 'Most Volatile', 'Most Stable', 'Most Promising']
        
        # Timeframe terms
        timeframes = ['2008', '2020', 'the Pandemic', 'a Decade', 'Five Years']
        
        # Generate random news articles
        news_articles = []
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        for i in range(limit):
            # Choose random elements
            topic = random.choice(topics)
            source = random.choice(sources)
            title_template = random.choice(title_templates)
            direction = random.choice(directions)
            superlative = random.choice(superlatives)
            timeframe = random.choice(timeframes)
            
            # Generate a title
            title = title_template.format(
                topic=topic, 
                direction=direction, 
                superlative=superlative, 
                timeframe=timeframe
            )
            
            # Generate a summary
            summary_templates = [
                f"Recent developments in {topic} show signs of {direction.lower()}. Analysts from various firms have weighed in on what this means for investors.",
                f"A comprehensive look at the current state of {topic} and its potential impact on financial markets in the coming quarters.",
                f"Understanding the implications of {topic} is crucial for investors looking to navigate the current economic landscape.",
                f"As {topic} continues to evolve, experts are divided on its long-term implications for global markets and economic stability.",
                f"This analysis breaks down the key factors driving changes in {topic} and provides insights for strategic investment decisions."
            ]
            
            summary = random.choice(summary_templates)
            
            # Generate a random date within the last week
            random_days = random.randint(0, 6)
            article_date = end_date - timedelta(days=random_days)
            date_str = article_date.strftime('%b %d, %Y')
            
            # Create article object
            article = {
                'title': title,
                'summary': summary,
                'source': source,
                'date': date_str,
                'url': f"https://example.com/financial-news/{i}",
                'sentiment': random.uniform(-1, 1)  # Random sentiment score
            }
            
            news_articles.append(article)
        
        return news_articles
    except Exception as e:
        logger.error(f"Error in get_financial_news: {str(e)}")
        return []

def get_market_summary():
    """
    Get a summary of current market conditions.
    
    Returns:
        dict: Dictionary containing market summary data
    """
    try:
        # In a real implementation, you would fetch this from an API
        # For demonstration, we'll use synthetic data
        
        major_indices = {
            'S&P 500': {
                'value': round(random.uniform(4500, 4600), 2),
                'change': round(random.uniform(-0.5, 1.0), 2)
            },
            'NASDAQ': {
                'value': round(random.uniform(14000, 14500), 2),
                'change': round(random.uniform(-0.5, 1.2), 2)
            },
            'Dow Jones': {
                'value': round(random.uniform(37000, 38000), 2),
                'change': round(random.uniform(-0.4, 0.8), 2)
            },
            'Russell 2000': {
                'value': round(random.uniform(1900, 2000), 2),
                'change': round(random.uniform(-0.7, 0.9), 2)
            }
        }
        
        commodities = {
            'Gold': {
                'value': round(random.uniform(2300, 2400), 2),
                'change': round(random.uniform(-0.6, 0.7), 2)
            },
            'Silver': {
                'value': round(random.uniform(28, 31), 2),
                'change': round(random.uniform(-1.0, 1.2), 2)
            },
            'Crude Oil': {
                'value': round(random.uniform(75, 85), 2),
                'change': round(random.uniform(-1.5, 1.8), 2)
            },
            'Natural Gas': {
                'value': round(random.uniform(2.0, 2.5), 2),
                'change': round(random.uniform(-2.0, 2.5), 2)
            }
        }
        
        cryptocurrencies = {
            'Bitcoin': {
                'value': round(random.uniform(65000, 70000), 2),
                'change': round(random.uniform(-3.0, 4.0), 2)
            },
            'Ethereum': {
                'value': round(random.uniform(3500, 4000), 2),
                'change': round(random.uniform(-2.5, 3.5), 2)
            },
            'Solana': {
                'value': round(random.uniform(150, 180), 2),
                'change': round(random.uniform(-4.0, 5.0), 2)
            }
        }
        
        # Generate a market summary
        summary = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'major_indices': major_indices,
            'commodities': commodities,
            'cryptocurrencies': cryptocurrencies,
            'market_mood': random.choice(['Bullish', 'Bearish', 'Neutral', 'Cautious', 'Optimistic']),
            'volatility_index': round(random.uniform(12, 22), 1)
        }
        
        return summary
    except Exception as e:
        logger.error(f"Error in get_market_summary: {str(e)}")
        return {}
