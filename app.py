"""
Real-time Stock Market Sentiment Analyzer
Main Streamlit Application
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# Import custom modules
from modules.data_collector import DataCollector
from modules.sentiment_analyzer import SentimentAnalyzer
from modules.data_processor import DataProcessor
from modules.visualizations import Visualizations
from utils.helpers import (
    get_sentiment_color, 
    get_sentiment_label, 
    format_large_number,
    calculate_price_change
)

# Page configuration
st.set_page_config(
    page_title="Stock Market Sentiment Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1976D2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1976D2;
    }
    .positive-sentiment {
        color: #00C853;
        font-weight: bold;
    }
    .negative-sentiment {
        color: #D32F2F;
        font-weight: bold;
    }
    .neutral-sentiment {
        color: #FFA726;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state - FIXED: Use get() method to safely access
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
if 'stock_data' not in st.session_state:
    st.session_state['stock_data'] = None
if 'sentiment_data' not in st.session_state:
    st.session_state['sentiment_data'] = None
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = None

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all components (cached)"""
    collector = DataCollector()
    analyzer = SentimentAnalyzer()
    processor = DataProcessor()
    visualizer = Visualizations()
    return collector, analyzer, processor, visualizer

collector, analyzer, processor, visualizer = initialize_components()

# Load data function
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(tickers, num_days=7):
    """Load stock and sentiment data"""
    with st.spinner('Fetching stock data...'):
        stock_data = collector.fetch_multiple_stocks(tickers, period=f'{num_days}d', interval='1h')
    
    with st.spinner('Generating sentiment data...'):
        sentiment_data = collector.generate_sentiment_for_multiple_stocks(tickers, num_days=num_days)
    
    return stock_data, sentiment_data

# Header
st.markdown('<div class="main-header">📈 Real-time Stock Market Sentiment Analyzer</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("### Stock Selection")

# Available tickers
available_tickers = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN']
selected_tickers = st.sidebar.multiselect(
    "Select stocks to analyze:",
    options=available_tickers,
    default=available_tickers
)

# Time range
st.sidebar.markdown("### Time Range")
num_days = st.sidebar.slider("Historical data (days):", min_value=1, max_value=30, value=7)

# Refresh button - FIXED: Use experimental_rerun for older Streamlit versions
if st.sidebar.button("🔄 Refresh Data", type="primary"):
    st.cache_data.clear()
    st.session_state['data_loaded'] = False
    # Use experimental_rerun for compatibility with older Streamlit versions
    if hasattr(st, 'rerun'):
        st.rerun()
    else:
        st.experimental_rerun()

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard analyzes real-time sentiment from simulated social media data "
    "and correlates it with actual stock price movements. "
    "\n\n**Data Sources:**\n"
    "- Stock prices: Yahoo Finance (yfinance) with simulated fallback\n"
    "- Sentiment: Simulated Twitter/Reddit data\n"
    "- Analysis: VADER Sentiment"
)

# Load data
if not selected_tickers:
    st.warning("⚠️ Please select at least one stock ticker from the sidebar.")
    st.stop()

# Load or refresh data - FIXED: Use get() method for safe access
data_loaded = st.session_state.get('data_loaded', False)
last_update = st.session_state.get('last_update', None)

if not data_loaded or last_update is None:
    stock_data, sentiment_data = load_data(selected_tickers, num_days)
    st.session_state['stock_data'] = stock_data
    st.session_state['sentiment_data'] = sentiment_data
    st.session_state['data_loaded'] = True
    st.session_state['last_update'] = datetime.now()
else:
    stock_data = st.session_state.get('stock_data')
    sentiment_data = st.session_state.get('sentiment_data')

# Display last update time
if st.session_state.get('last_update'):
    st.sidebar.markdown(f"**Last updated:** {st.session_state['last_update'].strftime('%Y-%m-%d %H:%M:%S')}")

# Main content
if stock_data is None or sentiment_data is None or stock_data.empty or sentiment_data.empty:
    st.error("❌ Failed to load data. Please try refreshing.")
    st.stop()

# Tab layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Detailed Analysis", "🔍 Correlation", "💬 Top Mentions"])

# Tab 1: Overview
with tab1:
    st.header("Market Overview")
    
    # Create columns for each stock
    cols = st.columns(len(selected_tickers))
    
    for idx, ticker in enumerate(selected_tickers):
        with cols[idx]:
            # Get stock info - FIXED: Add error handling
            stock_info = collector.get_latest_stock_info(ticker)
            
            if stock_info and stock_info.get('current_price') is not None:
                # Get sentiment summary
                summary = processor.get_sentiment_summary(sentiment_data, stock_data, ticker)
                
                # Display metrics
                st.subheader(f"{stock_info.get('company_name', ticker)}")
                
                current_price = stock_info.get('current_price', 0)
                previous_close = stock_info.get('previous_close', current_price)
                
                st.metric(
                    label="Current Price",
                    value=f"${current_price:.2f}",
                    delta=f"{calculate_price_change(current_price, previous_close):.2f}%"
                )
                
                sentiment_score = summary['latest_sentiment']
                sentiment_label = get_sentiment_label(sentiment_score)
                sentiment_color = get_sentiment_color(sentiment_score)
                
                st.markdown(f"**Sentiment:** <span style='color:{sentiment_color}'>{sentiment_label} ({sentiment_score:.3f})</span>", unsafe_allow_html=True)
                st.metric(label="Market Cap", value=format_large_number(stock_info.get('market_cap', 0)))
                st.metric(label="Correlation", value=f"{summary['price_correlation']:.3f}")
            else:
                st.error(f"Unable to load data for {ticker}")
    
    st.markdown("---")
    
    # Multi-stock comparison
    st.subheader("📊 Multi-Stock Comparison")
    
    sentiment_summaries = {}
    for ticker in selected_tickers:
        summary = processor.get_sentiment_summary(sentiment_data, stock_data, ticker)
        sentiment_summaries[ticker] = summary
    
    comparison_fig = visualizer.create_multi_stock_comparison(sentiment_summaries)
    st.plotly_chart(comparison_fig, use_container_width=True)
    
    # Correlation heatmap
    st.subheader("🔥 Sentiment-Price Correlation Heatmap")
    correlation_data = {ticker: sentiment_summaries[ticker] for ticker in selected_tickers}
    heatmap_fig = visualizer.create_correlation_heatmap(correlation_data)
    st.plotly_chart(heatmap_fig, use_container_width=True)

# Tab 2: Detailed Analysis
with tab2:
    st.header("Detailed Stock Analysis")
    
    # Stock selector for detailed view
    selected_stock = st.selectbox("Select a stock for detailed analysis:", selected_tickers)
    
    if selected_stock:
        # Get data for selected stock
        summary = processor.get_sentiment_summary(sentiment_data, stock_data, selected_stock)
        merged_data = summary['merged_data']
        
        # Sentiment gauge
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Current Sentiment")
            gauge_fig = visualizer.create_sentiment_gauge(summary['latest_sentiment'], selected_stock)
            st.plotly_chart(gauge_fig, use_container_width=True)
            
            # Key metrics
            st.markdown("### Key Metrics")
            st.metric("Average Sentiment", f"{summary['avg_sentiment']:.3f}")
            st.metric("Sentiment Volatility", f"{summary['sentiment_volatility']:.3f}")
            st.metric("Price Correlation", f"{summary['price_correlation']:.3f}")
            st.metric("Leading Correlation", f"{summary['leading_correlation']:.3f}")
            
            if summary['p_value'] < 0.05:
                st.success("✅ Statistically significant correlation")
            else:
                st.info("ℹ️ Correlation not statistically significant")
        
        with col2:
            # Sentiment vs Price chart
            st.subheader("Sentiment vs Price Movement")
            sentiment_price_fig = visualizer.create_sentiment_vs_price_chart(merged_data, selected_stock)
            st.plotly_chart(sentiment_price_fig, use_container_width=True)
        
        # Additional charts
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Volume of Mentions")
            volume_fig = visualizer.create_mention_volume_chart(sentiment_data, selected_stock)
            st.plotly_chart(volume_fig, use_container_width=True)
        
        with col4:
            st.subheader("Sentiment Distribution")
            pie_fig = visualizer.create_sentiment_distribution_pie(sentiment_data, selected_stock)
            st.plotly_chart(pie_fig, use_container_width=True)
        
        # Candlestick chart
        st.subheader("Price Movement (Candlestick)")
        candlestick_fig = visualizer.create_candlestick_chart(stock_data, selected_stock)
        st.plotly_chart(candlestick_fig, use_container_width=True)

# Tab 3: Correlation Analysis
with tab3:
    st.header("Correlation Analysis")
    
    st.markdown("""
    This section analyzes the relationship between social media sentiment and stock price movements.
    
    **Interpretation:**
    - **Positive correlation**: Sentiment and price move in the same direction
    - **Negative correlation**: Sentiment and price move in opposite directions
    - **Leading correlation**: Sentiment predicts future price movement
    """)
    
    # Create correlation summary table
    correlation_summary = []
    for ticker in selected_tickers:
        summary = processor.get_sentiment_summary(sentiment_data, stock_data, ticker)
        correlation_summary.append({
            'Ticker': ticker,
            'Avg Sentiment': f"{summary['avg_sentiment']:.3f}",
            'Price Correlation': f"{summary['price_correlation']:.3f}",
            'Leading Correlation (1h)': f"{summary['leading_correlation']:.3f}",
            'Sentiment Volatility': f"{summary['sentiment_volatility']:.3f}",
            'P-Value': f"{summary['p_value']:.4f}",
            'Significant': '✅' if summary['p_value'] < 0.05 else '❌'
        })
    
    correlation_df = pd.DataFrame(correlation_summary)
    st.dataframe(correlation_df, use_container_width=True)
    
    st.markdown("---")
    
    # Sentiment spikes detection
    st.subheader("🚨 Sentiment Anomalies & Spikes")
    
    selected_spike_stock = st.selectbox("Select stock for anomaly detection:", selected_tickers, key='spike_stock')
    
    if selected_spike_stock:
        spikes = processor.detect_sentiment_spikes(sentiment_data, selected_spike_stock, threshold=2.0)
        
        if spikes:
            st.warning(f"⚠️ Detected {len(spikes)} sentiment anomalies for {selected_spike_stock}")
            
            spikes_df = pd.DataFrame(spikes)
            spikes_df['timestamp'] = pd.to_datetime(spikes_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(spikes_df, use_container_width=True)
        else:
            st.success(f"✅ No significant sentiment anomalies detected for {selected_spike_stock}")

# Tab 4: Top Mentions
with tab4:
    st.header("💬 Top Mentions")
    
    selected_mention_stock = st.selectbox("Select stock:", selected_tickers, key='mention_stock')
    
    if selected_mention_stock:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🟢 Top Positive Mentions")
            positive_mentions = analyzer.get_top_mentions(sentiment_data, selected_mention_stock, top_n=10, sentiment_type='positive')
            
            if positive_mentions:
                for mention in positive_mentions:
                    timestamp = pd.to_datetime(mention['timestamp']).strftime('%Y-%m-%d %H:%M')
                    st.markdown(f"""
                    <div class="metric-card">
                        <strong>{mention['source']}</strong> - {timestamp}<br>
                        <span class="positive-sentiment">Score: {mention['sentiment_score']:.3f}</span><br>
                        "{mention['text']}"
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("No positive mentions found")
        
        with col2:
            st.subheader("🔴 Top Negative Mentions")
            negative_mentions = analyzer.get_top_mentions(sentiment_data, selected_mention_stock, top_n=10, sentiment_type='negative')
            
            if negative_mentions:
                for mention in negative_mentions:
                    timestamp = pd.to_datetime(mention['timestamp']).strftime('%Y-%m-%d %H:%M')
                    st.markdown(f"""
                    <div class="metric-card">
                        <strong>{mention['source']}</strong> - {timestamp}<br>
                        <span class="negative-sentiment">Score: {mention['sentiment_score']:.3f}</span><br>
                        "{mention['text']}"
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("No negative mentions found")

# Auto-refresh logic - FIXED: Use experimental_rerun for compatibility
if auto_refresh:
    time.sleep(300)  # Wait 5 minutes
    if hasattr(st, 'rerun'):
        st.rerun()
    else:
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Real-time Stock Market Sentiment Analyzer | Data updates every 5 minutes</p>
    <p>⚠️ This is a demo using simulated sentiment data. Not for actual trading decisions.</p>
</div>
""", unsafe_allow_html=True)