"""
Sentiment Analysis Engine
Analyzes text sentiment using VADER
"""
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def preprocess_text(self, text):
        """
        Clean and preprocess text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Keep emojis and special characters as they're important for sentiment
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of a single text using VADER
        Returns compound score between -1 and 1
        """
        cleaned_text = self.preprocess_text(text)
        scores = self.analyzer.polarity_scores(cleaned_text)
        
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu']
        }
    
    def analyze_batch(self, texts):
        """
        Analyze sentiment for multiple texts
        """
        results = []
        for text in texts:
            sentiment = self.analyze_sentiment(text)
            results.append(sentiment)
        return results
    
    def aggregate_sentiment_by_ticker(self, sentiment_df, ticker):
        """
        Aggregate sentiment scores for a specific ticker
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return None
        
        # Calculate aggregate metrics
        avg_sentiment = ticker_data['sentiment_score'].mean()
        sentiment_std = ticker_data['sentiment_score'].std()
        total_mentions = len(ticker_data)
        
        # Count sentiment categories
        positive_count = len(ticker_data[ticker_data['sentiment_score'] > 0.2])
        negative_count = len(ticker_data[ticker_data['sentiment_score'] < -0.2])
        neutral_count = total_mentions - positive_count - negative_count
        
        return {
            'ticker': ticker,
            'avg_sentiment': avg_sentiment,
            'sentiment_std': sentiment_std,
            'total_mentions': total_mentions,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_ratio': positive_count / total_mentions if total_mentions > 0 else 0,
            'negative_ratio': negative_count / total_mentions if total_mentions > 0 else 0
        }
    
    def calculate_sentiment_momentum(self, sentiment_df, ticker, window_hours=24):
        """
        Calculate sentiment momentum (rate of change)
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return 0
        
        ticker_data = ticker_data.sort_values('timestamp')
        
        # Split into recent and previous periods
        cutoff_time = ticker_data['timestamp'].max() - pd.Timedelta(hours=window_hours)
        recent_data = ticker_data[ticker_data['timestamp'] > cutoff_time]
        previous_data = ticker_data[ticker_data['timestamp'] <= cutoff_time]
        
        if recent_data.empty or previous_data.empty:
            return 0
        
        recent_sentiment = recent_data['sentiment_score'].mean()
        previous_sentiment = previous_data['sentiment_score'].mean()
        
        # Calculate momentum as percentage change
        if previous_sentiment != 0:
            momentum = ((recent_sentiment - previous_sentiment) / abs(previous_sentiment)) * 100
        else:
            momentum = 0
        
        return momentum
    
    def get_top_mentions(self, sentiment_df, ticker, top_n=5, sentiment_type='positive'):
        """
        Get top positive or negative mentions for a ticker
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return []
        
        if sentiment_type == 'positive':
            sorted_data = ticker_data.sort_values('sentiment_score', ascending=False)
        else:
            sorted_data = ticker_data.sort_values('sentiment_score', ascending=True)
        
        top_mentions = sorted_data.head(top_n)[['timestamp', 'text', 'sentiment_score', 'source']].to_dict('records')
        return top_mentions
    
    def aggregate_by_time_window(self, sentiment_df, ticker, window='1H'):
        """
        Aggregate sentiment by time windows (hourly, daily, etc.)
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return pd.DataFrame()
        
        ticker_data.set_index('timestamp', inplace=True)
        
        # Resample and aggregate
        aggregated = ticker_data.resample(window).agg({
            'sentiment_score': ['mean', 'std', 'count'],
            'confidence': 'mean'
        })
        
        aggregated.columns = ['avg_sentiment', 'sentiment_std', 'mention_count', 'avg_confidence']
        aggregated.reset_index(inplace=True)
        aggregated['ticker'] = ticker
        
        return aggregated