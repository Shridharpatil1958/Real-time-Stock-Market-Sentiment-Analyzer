"""
Utility functions for the Stock Market Sentiment Analyzer
"""
import pandas as pd
from datetime import datetime, timedelta


def get_sentiment_color(sentiment_score):
    """
    Return color based on sentiment score
    Args:
        sentiment_score: float between -1 and 1
    Returns:
        color string
    """
    if sentiment_score > 0.2:
        return '#00C853'  # Green for positive
    elif sentiment_score < -0.2:
        return '#D32F2F'  # Red for negative
    else:
        return '#FFA726'  # Orange for neutral


def get_sentiment_label(sentiment_score):
    """
    Return sentiment label based on score
    """
    if sentiment_score > 0.2:
        return 'Positive'
    elif sentiment_score < -0.2:
        return 'Negative'
    else:
        return 'Neutral'


def format_large_number(num):
    """
    Format large numbers with K, M, B suffixes
    """
    if num >= 1_000_000_000:
        return f'${num/1_000_000_000:.2f}B'
    elif num >= 1_000_000:
        return f'${num/1_000_000:.2f}M'
    elif num >= 1_000:
        return f'${num/1_000:.2f}K'
    else:
        return f'${num:.2f}'


def calculate_price_change(current_price, previous_price):
    """
    Calculate percentage change in price
    """
    if previous_price == 0:
        return 0
    return ((current_price - previous_price) / previous_price) * 100


def get_date_range(days=7):
    """
    Get date range for historical data
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def validate_ticker(ticker):
    """
    Validate stock ticker format
    """
    return ticker.isalpha() and len(ticker) <= 5