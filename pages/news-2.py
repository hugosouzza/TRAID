import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to sys.path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.news import get_financial_news, get_market_summary

def app():
    st.title("Noticias del Mercado")
    
    # Market summary in sidebar
    market_summary = get_market_summary()
    
    st.sidebar.subheader("Market Summary")
    
    # Display major indices
    for index_name, index_data in market_summary.get('major_indices', {}).items():
        change = index_data.get('change', 0)
        change_str = f"{'+' if change > 0 else ''}{change}%"
        # For Streamlit metrics, delta_color can only be 'normal', 'inverse', or 'off'
        delta_color = "normal"
        
        st.sidebar.metric(
            index_name,
            f"{index_data.get('value', 0):,.2f}",
            change_str,
            delta_color=delta_color
        )
    
    # Display cryptocurrencies
    st.sidebar.markdown("---")
    st.sidebar.subheader("Cryptocurrencies")
    
    for crypto_name, crypto_data in market_summary.get('cryptocurrencies', {}).items():
        change = crypto_data.get('change', 0)
        change_str = f"{'+' if change > 0 else ''}{change}%"
        # For Streamlit metrics, delta_color can only be 'normal', 'inverse', or 'off'
        delta_color = "normal"
        
        st.sidebar.metric(
            crypto_name,
            f"${crypto_data.get('value', 0):,.2f}",
            change_str,
            delta_color=delta_color
        )
    
    # News categories
    tab1, tab2 = st.tabs(["General News", "Fyp"])
    
    with tab1:
        news = get_financial_news(10)
        
        for i, item in enumerate(news):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    # Create a colored placeholder based on sentiment
                    sentiment = item.get('sentiment', 0)
                    color = "#7749F8" if sentiment > 0.2 else "#DC3545" if sentiment < -0.2 else "#FFC107"
                    
                    st.markdown(
                        f"""
                        <div style="width:100%; height:100px; background-color:{color}; opacity:0.7; 
                                  border-radius:5px; display:flex; align-items:center; 
                                  justify-content:center; color:white; font-weight:bold;">
                            {item['source']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
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
                "date": "Today",
                "sentiment": 0.75
            },
            {
                "title": "El mercado se prepara para un cambio",
                "summary": "Con la reciente volatilidad, los inversores están atentos a las próximas decisiones de la Fed...",
                "source": "Bloomberg",
                "date": "Yesterday",
                "sentiment": -0.2
            },
            {
                "title": "Nuevo ETF de tecnología emergente",
                "summary": "Un nuevo fondo centrado en empresas de IA y computación cuántica ha sido lanzado esta semana.",
                "source": "Reuters",
                "date": "2 days ago",
                "sentiment": 0.6
            }
        ]
        
        for i, item in enumerate(personalized_news):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    # Create a colored placeholder based on sentiment
                    sentiment = item.get('sentiment', 0)
                    color = "#7749F8" if sentiment > 0.2 else "#DC3545" if sentiment < -0.2 else "#FFC107"
                    
                    if i == 0:
                        st.markdown(
                            f"""
                            <div style="width:100%; height:100px; background-color:{color}; 
                                      border-radius:5px; display:flex; align-items:center; 
                                      justify-content:center; color:white; font-weight:bold;">
                                <div style="font-size:40px;">₿</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="width:100%; height:100px; background-color:{color}; 
                                      border-radius:5px; display:flex; align-items:center; 
                                      justify-content:center; color:white; font-weight:bold;">
                                {item['source']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                with col2:
                    st.subheader(item['title'])
                    st.markdown(item['summary'])
                    st.markdown(f"*{item['source']} - {item['date']}*")
                st.markdown("---")
    
    # Market Insights
    st.header("Market Insights")
    
    # Market mood
    mood = market_summary.get('market_mood', 'Neutral')
    mood_color = "#28A745" if mood in ['Bullish', 'Optimistic'] else "#DC3545" if mood in ['Bearish'] else "#FFC107"
    
    st.markdown(
        f"""
        <div style="background-color:#f8f9fa; padding:15px; border-radius:5px; margin-bottom:20px;">
            <h3>Market Mood: <span style="color:{mood_color};">{mood}</span></h3>
            <p>VIX Volatility Index: {market_summary.get('volatility_index', 15)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Market analysis
    st.subheader("Weekly Market Analysis")
    
    st.markdown("""
    ### Key Market Drivers This Week:
    
    1. **Federal Reserve Policy**: Interest rate expectations are shifting as new economic data suggests possible policy changes.
    
    2. **Earnings Season**: Major tech companies reported mixed results, with some exceeding expectations while others disappointed.
    
    3. **Inflation Data**: Recent inflation readings show signs of moderation, potentially easing pressure on central banks.
    
    4. **Geopolitical Tensions**: Ongoing conflicts continue to create uncertainty in energy and commodity markets.
    
    5. **Economic Indicators**: Manufacturing and service sector data showed resilience despite challenging conditions.
    """)
    
    # Industry performance
    st.subheader("Industry Performance (Weekly)")
    
    industries = pd.DataFrame({
        'Industry': ['Technology', 'Healthcare', 'Energy', 'Financials', 'Consumer Discretionary', 
                    'Communication Services', 'Utilities', 'Materials', 'Industrials', 'Real Estate'],
        'Performance': [2.5, 1.8, -1.2, 0.9, 1.5, 2.1, -0.8, 0.3, 1.1, -1.5]
    })
    
    # Sort by performance
    industries = industries.sort_values('Performance', ascending=False)
    
    # Color code based on performance
    def get_color(performance):
        if performance >= 2.0:
            return "#28A745"  # Strong green
        elif performance > 0:
            return "#7749F8"  # Purple
        elif performance > -1.0:
            return "#FFC107"  # Yellow
        else:
            return "#DC3545"  # Red
    
    industries['Color'] = industries['Performance'].apply(get_color)
    
    # Display as horizontal bars
    for i, row in industries.iterrows():
        col1, col2, col3 = st.columns([3, 6, 1])
        
        with col1:
            st.markdown(f"**{row['Industry']}**")
        
        with col2:
            # Create a bar
            width = abs(row['Performance']) * 10  # Scale for visibility
            if row['Performance'] >= 0:
                st.markdown(
                    f"""
                    <div style="background-color:{row['Color']}; width:{width}%; height:20px; border-radius:3px;"></div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="display:flex; justify-content:flex-end; width:100%;">
                        <div style="background-color:{row['Color']}; width:{width}%; height:20px; border-radius:3px;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        with col3:
            perf_str = f"+{row['Performance']}%" if row['Performance'] > 0 else f"{row['Performance']}%"
            st.markdown(f"**{perf_str}**")

if __name__ == "__main__":
    app()
