import requests
from bs4 import BeautifulSoup
import trafilatura
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_website_text_content(url):
    """
    Extract the main text content from a website using trafilatura.
    
    Args:
        url (str): The URL of the website to scrape
        
    Returns:
        str: The main text content of the website
    """
    try:
        # Send a request to the website
        logger.info(f"Fetching content from: {url}")
        downloaded = trafilatura.fetch_url(url)
        
        if downloaded is None:
            logger.warning(f"Failed to download content from {url}")
            # Fallback to requests
            return fallback_scraper(url)
        
        # Extract the text content
        text = trafilatura.extract(downloaded)
        
        if text is None or text.strip() == "":
            logger.warning(f"No text content extracted from {url}")
            return fallback_scraper(url)
            
        return text
    except Exception as e:
        logger.error(f"Error in get_website_text_content: {str(e)}")
        return fallback_scraper(url)

def fallback_scraper(url):
    """
    Fallback scraper using BeautifulSoup when trafilatura fails.
    
    Args:
        url (str): The URL of the website to scrape
        
    Returns:
        str: The extracted text content
    """
    try:
        # Set a user agent to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Send a request to the website
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        
        # Get text and clean it
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        logger.error(f"Error in fallback_scraper: {str(e)}")
        return f"Failed to scrape content: {str(e)}"

def scrape_financial_data(ticker_symbol):
    """
    Scrape financial data for a specific ticker symbol.
    
    Args:
        ticker_symbol (str): The stock ticker symbol
        
    Returns:
        dict: Dictionary containing the scraped financial data
    """
    try:
        url = f"https://finance.yahoo.com/quote/{ticker_symbol}"
        logger.info(f"Scraping financial data for {ticker_symbol} from {url}")
        
        # Set a user agent to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://finance.yahoo.com/',
            'DNT': '1'
        }
        
        # Send a request to the website
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract price data
        price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        price = price_element.text if price_element else "N/A"
        
        # Try to get price change and percentage
        change_element = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
        change = change_element.text if change_element else "N/A"
        
        change_percent_element = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
        change_percent = change_percent_element.text if change_percent_element else "N/A"
        
        # Extract additional data
        data = {
            'ticker': ticker_symbol,
            'price': price,
            'change': change,
            'change_percent': change_percent,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Additional data elements to try to extract
        data_elements = {
            'Previous Close': 'PREV_CLOSE-value',
            'Open': 'OPEN-value',
            'Day Range': 'DAYS_RANGE-value',
            'Volume': 'TD_VOLUME-value',
            'Market Cap': 'MARKET_CAP-value',
            '52 Week Range': 'FIFTY_TWO_WK_RANGE-value',
            'Avg Volume': 'AVERAGE_VOLUME_3MONTH-value',
            'PE Ratio': 'PE_RATIO-value',
            'EPS': 'EPS_RATIO-value',
            'Dividend': 'DIVIDEND_AND_YIELD-value'
        }
        
        for key, value_id in data_elements.items():
            element = soup.find('td', {'data-test': value_id})
            data[key] = element.text if element else "N/A"
        
        # Try to extract company name
        try:
            company_name_element = soup.find('h1', {'class': 'D(ib)'})
            if company_name_element:
                full_text = company_name_element.text
                data['company_name'] = full_text.split('(')[0].strip()
        except:
            data['company_name'] = ticker_symbol
            
        return data
    except Exception as e:
        logger.error(f"Error in scrape_financial_data: {str(e)}")
        return {'error': str(e), 'ticker': ticker_symbol}

def scrape_multiple_tickers(ticker_list):
    """
    Scrape financial data for multiple ticker symbols.
    
    Args:
        ticker_list (list): List of stock ticker symbols
        
    Returns:
        list: List of dictionaries containing the scraped financial data
    """
    results = []
    
    for ticker in ticker_list:
        try:
            # Add a random delay to avoid hitting rate limits
            time.sleep(random.uniform(1, 3))
            data = scrape_financial_data(ticker)
            results.append(data)
        except Exception as e:
            logger.error(f"Error scraping {ticker}: {str(e)}")
            results.append({'error': str(e), 'ticker': ticker})
    
    return results

def scrape_ticker_news(ticker_symbol, limit=5):
    """
    Scrape latest news for a specific ticker symbol.
    
    Args:
        ticker_symbol (str): The stock ticker symbol
        limit (int): Maximum number of news items to return
        
    Returns:
        list: List of dictionaries containing news data
    """
    try:
        url = f"https://finance.yahoo.com/quote/{ticker_symbol}/news"
        logger.info(f"Scraping news for {ticker_symbol} from {url}")
        
        # Set a user agent to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://finance.yahoo.com/',
            'DNT': '1'
        }
        
        # Send a request to the website
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find news items
        news_items = []
        news_elements = soup.find_all('li', {'class': 'js-stream-content'})
        
        for i, element in enumerate(news_elements):
            if i >= limit:
                break
                
            try:
                # Extract title
                title_element = element.find('h3')
                title = title_element.text.strip() if title_element else "No title"
                
                # Extract link
                link_element = element.find('a')
                link = link_element.get('href') if link_element else ""
                if link and not link.startswith('http'):
                    link = f"https://finance.yahoo.com{link}"
                
                # Extract source and date
                source_element = element.find('div', {'class': 'C(#959595)'}) or element.find('div', {'class': 'C(#5b5b5b)'})
                source_text = source_element.text.strip() if source_element else ""
                
                # Try to split source and date
                if "·" in source_text:
                    source, date = source_text.split("·", 1)
                    source = source.strip()
                    date = date.strip()
                else:
                    source = source_text
                    date = "N/A"
                
                # Extract summary if available
                summary_element = element.find('p')
                summary = summary_element.text.strip() if summary_element else "No summary available"
                
                news_items.append({
                    'title': title,
                    'source': source,
                    'date': date,
                    'summary': summary,
                    'url': link
                })
                
            except Exception as e:
                logger.error(f"Error parsing news item: {str(e)}")
                continue
        
        return news_items
    except Exception as e:
        logger.error(f"Error in scrape_ticker_news: {str(e)}")
        return []
