mport streamlit as st
import os
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
from utils.finance import get_stock_data, get_portfolio_metrics
from utils.scraper import get_website_text_content
from utils.sentiment import analyze_sentiment
from utils.news import get_financial_news

# Page configuration
st.set_page_config(
    page_title="Traid - Financial Data Tool for Creatives",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = "6789"  # Example verification code
if 'user_input' not in st.session_state:
    st.session_state.user_input = ['', '', '', '']
if 'current_digit' not in st.session_state:
    st.session_state.current_digit = 0

def verify_code():
    """Verify the entered code against the stored verification code"""
    user_code = ''.join(st.session_state.user_input)
    if user_code == st.session_state.verification_code:
        st.session_state.authenticated = True
        st.experimental_rerun()
    else:
        st.error("Invalid verification code. Please try again.")

def update_digit(i, value):
    """Update a specific digit in the code input"""
    if 0 <= i < 4:
        st.session_state.user_input[i] = value
        if i < 3 and value != '':
            st.session_state.current_digit = i + 1

def show_welcome_screen():
    """Display the welcome screen with logo and introduction"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding: 20px;">
                <svg width="80" height="80" viewBox="0 0 100 100" style="margin-bottom: 20px;">
                    <circle cx="50" cy="50" r="40" fill="#7749F8" />
                    <path d="M50 20 L30 50 L50 65 L70 50 L50 20 Z" fill="white" />
                    <path d="M40 50 L50 65 L60 50 L50 35 Z" fill="#7749F8" />
                </svg>
                <h1 style="color: #333;">Bienvenido a Traid</h1>
                <p style="color: #666; margin-bottom: 30px;">
                    Invertir sin saber, ahora es posible.<br>
                    Un gusto saludarte desde donde el futuro de tus finanzas está cuidado, 
                    sin complicación y fuera de comisiones.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Empecemos a crecer juntos", use_container_width=True):
                st.session_state.show_verification = True
                st.experimental_rerun()
        with col_b:
            if st.button("Iniciar sesión", use_container_width=True):
                st.session_state.show_verification = True
                st.experimental_rerun()

def show_verification_screen():
    """Display the verification code input screen"""
    st.markdown(
        """
        <div style="padding: 20px 0;">
            <h2>Introduce el código de 4 dígitos que le hemos enviado</h2>
            <p style="color: #666; margin-bottom: 20px;">+123 000 111 222 333</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Create 4 digit input boxes
    with col1:
        digit1 = st.text_input("", max_chars=1, key="digit1", value=st.session_state.user_input[0])
        if digit1 and len(digit1) == 1 and digit1.isdigit():
            update_digit(0, digit1)
    
    with col2:
        digit2 = st.text_input("", max_chars=1, key="digit2", value=st.session_state.user_input[1])
        if digit2 and len(digit2) == 1 and digit2.isdigit():
            update_digit(1, digit2)
    
    with col3:
        digit3 = st.text_input("", max_chars=1, key="digit3", value=st.session_state.user_input[2])
        if digit3 and len(digit3) == 1 and digit3.isdigit():
            update_digit(2, digit3)
    
    with col4:
        digit4 = st.text_input("", max_chars=1, key="digit4", value=st.session_state.user_input[3])
        if digit4 and len(digit4) == 1 and digit4.isdigit():
            update_digit(3, digit4)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.button("Enviar a otro número")
    
    with col_b:
        st.button("Volver a enviar")
    
    if st.button("Únete y toma el control de tus finanzas", use_container_width=True):
        verify_code()

def show_main_app():
    """Display the main application after authentication"""
    # Sidebar navigation
    with st.sidebar:
        st.image("assets/traid_logo.svg", width=50)
        st.title("Traid")
        
        st.markdown("### Herramientas de Datos")
        tools = ["Dashboard", "Fund Tracker", "Portfolio", "News", "Sofia Assistant", "Data Scraper"]
        selected_tool = st.radio("", tools, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### User Profile")
        st.text("José Mª Olazábal")
        st.text("Investor Risk: 4/7")
    
    if selected_tool == "Dashboard":
        show_dashboard()
    elif selected_tool == "Fund Tracker":
        show_fund_tracker()
    elif selected_tool == "Portfolio":
        show_portfolio()
    elif selected_tool == "News":
        show_news()
    elif selected_tool == "Sofia Assistant":
        show_assistant()
    elif selected_tool == "Data Scraper":
        show_data_scraper()

def show_dashboard():
    """Display the dashboard with portfolio overview and recent operations"""
    st.title("Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Tu Portfolio")
        
        # Get portfolio data
        portfolio_data = get_portfolio_metrics()
        
        # Create portfolio chart
        fig = px.line(portfolio_data, x='date', y='value', 
                    title='Portfolio Value Over Time', 
                    labels={'value': 'Value ($)', 'date': 'Date'})
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
            'Sentiment': [sentiment_data['AAPL'], sentiment_data['MSFT'], sentiment_data['GOOGL']]
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

def show_fund_tracker():
    """Display the fund tracker with search and recommendations"""
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
    categories_col1.button("📈 Alto riesgo")
    categories_col2.button("📉 Bajo riesgo")
    categories_col3.button("💻 Tecnología")
    categories_col4.button("🏭 Sectores")
    
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
    
    # Recommendations
    st.subheader("Recomendaciones para ti")
    
    funds = [
        {"name": "Global Equity Fund", "risk": "Moderate", "return": "8.2%", "desc": "Broad exposure to global equity markets"},
        {"name": "Tech Innovators ETF", "risk": "High", "return": "12.5%", "desc": "Focused on cutting-edge technology companies"},
        {"name": "Sustainable Future Fund", "risk": "Moderate", "return": "7.8%", "desc": "Environmentally and socially responsible investments"}
    ]
    
    cols = st.columns(3)
    for i, fund in enumerate(funds):
        with cols[i]:
            st.markdown(f"**{fund['name']}**")
            st.markdown(f"Risk: {fund['risk']} | Return: {fund['return']}")
            st.markdown(fund['desc'])
            st.button("View Details", key=f"view_{i}")

def show_portfolio():
    """Display the portfolio page with user's investments"""
    st.title("Portfolio")
    
    # User profile
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/150", width=150)
    with col2:
        st.header("José Mª Olazábal")
        st.subheader("Inversor Riesgo 4/7")
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        metrics_col1.metric("Activos Totales", "$150,000")
        metrics_col2.metric("Tasa de Rentabilidad", "12.5%")
        metrics_col3.metric("Rendimiento Reciente MTD", "2.11%")
    
    st.markdown("---")
    
    # Portfolio breakdown
    st.subheader("Portfolio Breakdown")
    
    # Asset allocation chart
    allocation_data = {
        'Asset Type': ['Stocks', 'Bonds', 'Cash', 'Alternatives', 'Real Estate'],
        'Allocation': [45, 25, 15, 10, 5]
    }
    allocation_df = pd.DataFrame(allocation_data)
    
    fig = px.pie(allocation_df, values='Allocation', names='Asset Type', 
                title='Asset Allocation', hole=0.4,
                color_discrete_sequence=px.colors.sequential.Purples)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # Holdings table
    st.subheader("Current Holdings")
    
    holdings = pd.DataFrame({
        'Symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'ORCL', 'NVO'],
        'Name': ['Apple Inc.', 'Microsoft Corp', 'Alphabet Inc', 'Amazon.com', 'NVIDIA Corp', 'Oracle Corp', 'Novo Nordisk'],
        'Shares': [100, 50, 20, 15, 40, 50, 75],
        'Price': [170.29, 325.46, 138.72, 175.80, 840.35, 148.42, 135.67],
        'Value': [17029.00, 16273.00, 2774.40, 2637.00, 33614.00, 7421.00, 10175.25],
        'Return': [24.5, 18.3, 15.2, 10.8, 35.7, 8.9, 12.4]
    })
    
    st.dataframe(holdings, use_container_width=True)
    
    # Performance chart
    st.subheader("Portfolio Performance")
    
    # Create date range for last 12 months
    dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
    performance = pd.DataFrame({
        'Date': dates,
        'Portfolio': [8.2, 8.7, 9.1, 7.8, 8.5, 9.3, 10.1, 11.2, 10.8, 11.5, 12.2, 12.5],
        'Benchmark': [7.5, 7.8, 8.2, 7.1, 7.9, 8.5, 9.0, 9.8, 9.5, 10.1, 10.5, 10.8]
    })
    
    fig = px.line(performance, x='Date', y=['Portfolio', 'Benchmark'],
                title='Portfolio vs Benchmark (12 Months)',
                labels={'value': 'Return (%)', 'Date': 'Date', 'variable': 'Legend'},
                color_discrete_sequence=['#7749F8', '#33B5E5'])
    st.plotly_chart(fig, use_container_width=True)

def show_news():
    """Display financial news and market updates"""
    st.title("Noticias del Mercado")
    
    # News categories
    tab1, tab2 = st.tabs(["General News", "Fyp"])
    
    with tab1:
        news = get_financial_news(10)
        
        for i, item in enumerate(news):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(f"https://via.placeholder.com/150x100?text=News+{i+1}", width=150)
                with col2:
                    st.subheader(item['title'])
                    st.markdown(item['summary'])
                    st.markdown(f"*{item['source']} - {item['date']}*")
                st.markdown("---")
    
    with tab2:
        # Show personalized news feed
        st.subheader("Your Personalized News")
        
        personalized_news = [
            {
                "title": "Criptomonedas en alza",
                "summary": "Bitcoin y Ethereum lideran el incremento con ganancias significativas en la última semana.",
                "source": "CoinDesk",
                "date": "Today"
            },
            {
                "title": "El mercado se prepara para un cambio",
                "summary": "Con la reciente volatilidad, los inversores están atentos a las próximas decisiones de la Fed...",
                "source": "Bloomberg",
                "date": "Yesterday"
            },
            {
                "title": "Nuevo ETF de tecnología emergente",
                "summary": "Un nuevo fondo centrado en empresas de IA y computación cuántica ha sido lanzado esta semana.",
                "source": "Reuters",
                "date": "2 days ago"
            }
        ]
        
        for i, item in enumerate(personalized_news):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if i == 0:
                        st.image("https://via.placeholder.com/150x100?text=Bitcoin", width=150)
                    else:
                        st.image(f"https://via.placeholder.com/150x100?text=News+{i+1}", width=150)
                with col2:
                    st.subheader(item['title'])
                    st.markdown(item['summary'])
                    st.markdown(f"*{item['source']} - {item['date']}*")
                st.markdown("---")
    
    # Market summary
    st.sidebar.subheader("Market Summary")
    st.sidebar.metric("S&P 500", "4,587.64", "+0.57%")
    st.sidebar.metric("NASDAQ", "14,261.50", "+0.83%")
    st.sidebar.metric("DOW", "37,404.35", "+0.38%")
    st.sidebar.metric("Bitcoin", "$68,432.18", "+2.14%")
    st.sidebar.metric("Gold", "$2,348.76", "-0.23%")

def show_assistant():
    """Display the Sofia AI assistant chat interface"""
    st.title("Sofia - Tu Asesora Financiera")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Hola! Soy Sofía, tu nueva asesora financiera. ¿En qué puedo ayudarte hoy con tus inversiones en fondos?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("Type a message..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            response = get_assistant_response(prompt)
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def get_assistant_response(prompt):
    """Generate a response from the Sofia assistant based on user prompt"""
    # Simple response logic based on keywords in the prompt
    prompt_lower = prompt.lower()
    
    if "recomendaciones" in prompt_lower or "fondos" in prompt_lower:
        return """
        Claro, tengo algunas opciones que podrían interesarte. Por ejemplo, el fondo de inversión en tecnología emergente.

        Es un fondo que cuadra mucho con tu perfil de riesgo, aquí tienes la evolución histórica, si quieres más datos dímelo.

        ```
        █▁▄█▃▂▅█▂▃▄▂█▄▅▁█▃
        ```
        """
    
    elif "riesgo" in prompt_lower:
        return "Tu perfil de riesgo actual es 4/7, lo que indica una tolerancia moderada. Esto nos permite explorar fondos con un equilibrio entre crecimiento y estabilidad. ¿Quieres que te muestre algunas opciones que se alinean con este perfil?"
    
    elif "rentabilidad" in prompt_lower:
        return "Basado en tu perfil y las condiciones actuales del mercado, podemos apuntar a una rentabilidad anual entre el 7% y 8%. ¿Te gustaría explorar estrategias específicas para alcanzar este objetivo?"
    
    elif "mercado" in prompt_lower or "tendencias" in prompt_lower:
        return "Las tendencias actuales del mercado muestran un fuerte desempeño en el sector tecnológico y energías renovables. Los mercados emergentes también están mostrando señales positivas. ¿Quieres que profundice en alguno de estos sectores?"
    
    else:
        return "Entiendo. ¿Puedes darme más detalles sobre lo que estás buscando en términos de inversión? Puedo ayudarte con recomendaciones de fondos, análisis de riesgo, o estrategias de diversificación."

def show_data_scraper():
    """Display the data scraping and analysis tool"""
    st.title("Data Scraper & Analysis Tool")
    
    with st.expander("About This Tool", expanded=True):
        st.markdown("""
        This tool allows you to scrape financial data from websites, analyze market sentiment, 
        and export the results for further analysis. Perfect for creatives who want to make 
        data-driven investment decisions.
        """)
    
    # Create tabs for different scraping options
    tab1, tab2, tab3 = st.tabs(["Web Content Scraper", "Stock Data Scraper", "News Scraper"])
    
    # Tab 1: General Web Content Scraper
    with tab1:
        st.header("Web Content Scraper")
        st.write("Extract text content from any website for analysis.")
        
        scrape_col1, scrape_col2 = st.columns([3, 1])
        
        with scrape_col1:
            url = st.text_input("Enter website URL to scrape:", placeholder="https://finance.yahoo.com/quote/AAPL", key="general_url")
        
        with scrape_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            scrape_button = st.button("Scrape Data", use_container_width=True, key="general_scrape")
        
        if scrape_button and url:
            with st.spinner("Scraping data..."):
                try:
                    scraped_content = get_website_text_content(url)
                    st.success("Data scraped successfully!")
                    
                    with st.expander("Raw Scraped Content", expanded=False):
                        st.text_area("Content", scraped_content, height=200)
                    
                    # Simple content analysis
                    word_count = len(scraped_content.split())
                    st.metric("Word Count", word_count)
                    
                    # Sentiment analysis of the content
                    sentiment = analyze_sentiment(scraped_content)
                    sentiment_score = sentiment.get('overall', 0)
                    
                    sentiment_color = "red"
                    if sentiment_score > 0.3:
                        sentiment_color = "green"
                    elif sentiment_score > -0.3:
                        sentiment_color = "yellow"
                        
                    st.markdown(f"<h3>Content Sentiment: <span style='color:{sentiment_color};'>{sentiment_score:.2f}</span></h3>", unsafe_allow_html=True)
                    
                    # Export options
                    st.subheader("Export Options")
                    export_col1, export_col2 = st.columns(2)
                    with export_col1:
                        st.download_button(
                            label="Export as TXT",
                            data=scraped_content,
                            file_name="scraped_data.txt",
                            mime="text/plain"
                        )
                    with export_col2:
                        # Convert to JSON
                        json_data = json.dumps({
                            "url": url,
                            "date_scraped": str(datetime.now()),
                            "content": scraped_content,
                            "word_count": word_count,
                            "sentiment": sentiment_score
                        })
                        st.download_button(
                            label="Export as JSON",
                            data=json_data,
                            file_name="scraped_data.json",
                            mime="application/json"
                        )
                
                except Exception as e:
                    st.error(f"Error scraping data: {str(e)}")
    
    # Tab 2: Stock Data Scraper
    with tab2:
        st.header("Stock Data Scraper")
        st.write("Extract financial data for specific stock tickers.")
        
        ticker_input_col1, ticker_input_col2 = st.columns([3, 1])
        
        with ticker_input_col1:
            ticker_input = st.text_input("Enter stock ticker symbol:", placeholder="AAPL", key="ticker_input")
        
        with ticker_input_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            ticker_scrape_button = st.button("Get Stock Data", use_container_width=True, key="ticker_scrape")
        
        if ticker_scrape_button and ticker_input:
            with st.spinner("Fetching stock data..."):
                try:
                    # Get data using the enhanced scraper function
                    from utils.scraper import scrape_financial_data
                    stock_data = scrape_financial_data(ticker_input.strip().upper())
                    
                    if 'error' in stock_data:
                        st.error(f"Error fetching data: {stock_data['error']}")
                    else:
                        st.success(f"Successfully fetched data for {stock_data.get('company_name', ticker_input)}")
                        
                        # Create columns for key metrics
                        metric_cols = st.columns(3)
                        
                        # Current price with change
                        price_change_color = "green" if not stock_data.get('change', '').startswith('-') else "red"
                        metric_cols[0].metric(
                            "Current Price", 
                            f"${stock_data.get('price', 'N/A')}", 
                            stock_data.get('change_percent', 'N/A'),
                            delta_color=price_change_color
                        )
                        
                        # Volume
                        metric_cols[1].metric("Volume", stock_data.get('Volume', 'N/A'))
                        
                        # Market Cap
                        metric_cols[2].metric("Market Cap", stock_data.get('Market Cap', 'N/A'))
                        
                        # Create a table with all the data
                        st.subheader("Stock Details")
                        
                        # Transform dictionary to a more display-friendly format
                        display_data = []
                        for key, value in stock_data.items():
                            if key not in ['ticker', 'error']:
                                display_data.append({"Metric": key, "Value": value})
                        
                        # Convert to DataFrame and display
                        display_df = pd.DataFrame(display_data)
                        st.dataframe(display_df, use_container_width=True)
                        
                        # Export option
                        st.download_button(
                            label="Export Stock Data",
                            data=json.dumps(stock_data, indent=2),
                            file_name=f"{ticker_input}_stock_data.json",
                            mime="application/json"
                        )
                
                except Exception as e:
                    st.error(f"Error processing stock data: {str(e)}")
    
    # Tab 3: News Scraper
    with tab3:
        st.header("Stock News Scraper")
        st.write("Get the latest news for a specific stock ticker.")
        
        news_col1, news_col2 = st.columns([3, 1])
        
        with news_col1:
            news_ticker = st.text_input("Enter stock ticker symbol:", placeholder="AAPL", key="news_ticker")
        
        with news_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            news_scrape_button = st.button("Get Latest News", use_container_width=True, key="news_scrape")
        
        if news_scrape_button and news_ticker:
            with st.spinner("Fetching latest news..."):
                try:
                    # Get news using our new scraper function
                    from utils.scraper import scrape_ticker_news
                    news_items = scrape_ticker_news(news_ticker.strip().upper(), limit=10)
                    
                    if not news_items:
                        st.warning(f"No news found for {news_ticker.upper()}")
                    else:
                        st.success(f"Found {len(news_items)} news articles for {news_ticker.upper()}")
                        
                        # Display each news item with sentiment analysis
                        for i, item in enumerate(news_items):
                            with st.container():
                                col1, col2 = st.columns([1, 4])
                                
                                # Analyze sentiment for the news title and summary
                                title_and_summary = f"{item['title']} {item['summary']}"
                                sentiment = analyze_sentiment(title_and_summary)
                                sentiment_score = sentiment.get('overall', 0)
                                
                                # Determine color based on sentiment
                                sentiment_color = "#7749F8"  # Default purple
                                if sentiment_score > 0.3:
                                    sentiment_color = "#28A745"  # Green
                                elif sentiment_score < -0.3:
                                    sentiment_color = "#DC3545"  # Red
                                
                                # Display source with color-coded sentiment background
                                with col1:
                                    st.markdown(
                                        f"""
                                        <div style="width:100%; height:100px; background-color:{sentiment_color}; 
                                                  border-radius:5px; display:flex; align-items:center; 
                                                  justify-content:center; color:white; font-weight:bold;">
                                            {item['source']}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                                
                                # Display news details
                                with col2:
                                    st.subheader(item['title'])
                                    st.markdown(item['summary'])
                                    st.markdown(f"*{item['source']} - {item['date']}*")
                                    
                                    if item['url']:
                                        st.markdown(f"[Read full article]({item['url']})")
                                
                                st.markdown("---")
                        
                        # Export option for all news items
                        st.download_button(
                            label="Export News Data",
                            data=json.dumps(news_items, indent=2),
                            file_name=f"{news_ticker}_news.json",
                            mime="application/json"
                        )
                
                except Exception as e:
                    st.error(f"Error fetching news: {str(e)}")
    
    # Social Media Sentiment Analysis
    st.header("Social Media Sentiment Analysis")
    
    sentiment_tab1, sentiment_tab2 = st.tabs(["Ticker Analysis", "Custom Query"])
    
    with sentiment_tab1:
        ticker_col1, ticker_col2 = st.columns([3, 1])
        
        with ticker_col1:
            tickers = st.text_input("Enter stock tickers (comma separated):", placeholder="AAPL,MSFT,GOOGL", key="sentiment_tickers")
        
        with ticker_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            analyze_button = st.button("Analyze Sentiment", use_container_width=True, key="sentiment_analyze")
        
        if analyze_button and tickers:
            with st.spinner("Analyzing sentiment..."):
                try:
                    ticker_list = [t.strip() for t in tickers.split(',')]
                    sentiment_results = {}
                    
                    for ticker in ticker_list:
                        sentiment_results[ticker] = round(float(analyze_sentiment(f"${ticker}").get(ticker, 0)), 2)
                    
                    # Display results
                    sentiment_df = pd.DataFrame({
                        'Ticker': list(sentiment_results.keys()),
                        'Sentiment Score': list(sentiment_results.values())
                    })
                    
                    # Create sentiment chart
                    fig = px.bar(sentiment_df, x='Ticker', y='Sentiment Score',
                               title='Social Media Sentiment by Ticker',
                               color='Sentiment Score',
                               color_continuous_scale=['red', 'yellow', 'green'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Export options
                    st.download_button(
                        label="Export Sentiment Data",
                        data=sentiment_df.to_csv(index=False),
                        file_name="sentiment_analysis.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Error analyzing sentiment: {str(e)}")
    
    with sentiment_tab2:
        query = st.text_input("Enter custom search query:", placeholder="Bitcoin price prediction 2023", key="custom_query")
        custom_analyze_button = st.button("Analyze Custom Query", use_container_width=True, key="custom_analyze")
        
        if custom_analyze_button and query:
            with st.spinner("Analyzing custom query..."):
                try:
                    # Simulate analysis of custom query
                    sentiment_score = analyze_sentiment(query).get('overall', 0)
                    
                    # Display results
                    st.metric("Overall Sentiment", f"{sentiment_score:.2f}")
                    
                    # Create visual representation
                    if sentiment_score > 0.3:
                        st.success("Positive sentiment detected! This topic is being discussed favorably.")
                    elif sentiment_score < -0.3:
                        st.error("Negative sentiment detected! This topic is being discussed unfavorably.")
                    else:
                        st.info("Neutral sentiment detected. This topic has mixed or balanced discussions.")
                
                except Exception as e:
                    st.error(f"Error analyzing custom query: {str(e)}")

# Main app flow
if st.session_state.authenticated:
    show_main_app()
elif 'show_verification' in st.session_state and st.session_state.show_verification:
    show_verification_screen()
else:
    show_welcome_screen()
