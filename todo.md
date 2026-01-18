# Real-time Stock Market Sentiment Analyzer - Development Plan

## Project Overview
A Streamlit-based dashboard for analyzing real-time sentiment from social media and news sources, correlating it with stock price movements.

## Technical Stack
- **Backend**: Python, Pandas, NLTK/VADER for sentiment analysis
- **Data Sources**: yfinance for stock data, simulated social media data (Twitter/Reddit APIs require authentication)
- **Frontend**: Streamlit with Plotly for interactive visualizations
- **Storage**: In-memory caching with session state

## MVP Implementation Strategy
For this MVP, we'll focus on:
1. Real stock price data using yfinance (no API key needed)
2. Simulated sentiment data (Twitter/Reddit APIs require complex authentication)
3. Core sentiment analysis using VADER (lightweight, no model download needed)
4. Real-time dashboard with 5 popular stocks: AAPL, TSLA, MSFT, GOOGL, AMZN
5. Historical data for last 7 days

## File Structure
```
/workspace/app/frontend/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── modules/
│   ├── __init__.py
│   ├── data_collector.py          # Stock price and sentiment data collection
│   ├── sentiment_analyzer.py      # Sentiment analysis engine
│   ├── data_processor.py          # Data aggregation and correlation
│   └── visualizations.py          # Chart and visualization components
└── utils/
    ├── __init__.py
    └── helpers.py                  # Utility functions
```

## Development Tasks

### 1. Setup & Dependencies
- Create requirements.txt with all necessary packages
- Set up project structure with modules and utils folders

### 2. Data Collection Module (modules/data_collector.py)
- Implement stock price fetching using yfinance
- Create simulated sentiment data generator (mimicking Twitter/Reddit data)
- Add caching mechanism for API calls
- Implement error handling and rate limiting

### 3. Sentiment Analysis Engine (modules/sentiment_analyzer.py)
- Integrate VADER sentiment analyzer
- Implement text preprocessing functions
- Create sentiment scoring system (positive, negative, neutral)
- Calculate confidence scores and aggregate metrics

### 4. Data Processing (modules/data_processor.py)
- Aggregate sentiment by stock ticker and time windows
- Calculate sentiment momentum and trends
- Implement correlation analysis between sentiment and price
- Create data structures for dashboard consumption

### 5. Visualization Components (modules/visualizations.py)
- Live sentiment gauge charts
- Time-series comparison (sentiment vs price)
- Volume of mentions bar charts
- Sentiment distribution pie charts
- Stock price candlestick charts
- Correlation heatmaps

### 6. Main Dashboard (app.py)
- Streamlit page configuration and layout
- Sidebar for stock selection and time range
- Real-time data refresh mechanism
- Display all visualization components
- Add metrics cards for key statistics

### 7. Utility Functions (utils/helpers.py)
- Date/time formatting
- Color schemes for sentiment
- Data validation functions
- Cache management

## Features Implemented
✅ Track 5 popular stocks (AAPL, TSLA, MSFT, GOOGL, AMZN)
✅ Real-time stock price data
✅ Simulated sentiment data with realistic patterns
✅ Sentiment analysis using VADER
✅ Interactive dashboard with multiple visualizations
✅ Historical data (last 7 days)
✅ Correlation analysis
✅ Sentiment momentum tracking

## Future Enhancements (Not in MVP)
- Real Twitter/X API integration
- Real Reddit API integration
- News API integration
- FinBERT model for advanced sentiment
- Database storage (PostgreSQL/MongoDB)
- WebSocket for true real-time updates
- Alert system for sentiment spikes
- User authentication
- Custom stock watchlists