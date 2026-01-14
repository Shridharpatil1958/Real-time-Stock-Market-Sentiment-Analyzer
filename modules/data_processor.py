"""
Data Processing Module
Handles data aggregation, correlation analysis, and feature engineering
"""
import pandas as pd
import numpy as np
from scipy import stats


class DataProcessor:
    def __init__(self):
        pass
    
    def merge_stock_and_sentiment(self, stock_df, sentiment_df, ticker):
        """
        Merge stock price data with aggregated sentiment data
        """
        # Filter for specific ticker
        stock_ticker = stock_df[stock_df['Ticker'] == ticker].copy()
        
        if stock_ticker.empty:
            return pd.DataFrame()
        
        # Ensure datetime format
        if 'Datetime' in stock_ticker.columns:
            stock_ticker['timestamp'] = pd.to_datetime(stock_ticker['Datetime'])
        elif 'Date' in stock_ticker.columns:
            stock_ticker['timestamp'] = pd.to_datetime(stock_ticker['Date'])
        
        stock_ticker.set_index('timestamp', inplace=True)
        
        # Aggregate sentiment by hour to match stock data
        sentiment_ticker = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if sentiment_ticker.empty:
            # Return stock data with null sentiment columns
            stock_ticker['avg_sentiment'] = 0
            stock_ticker['mention_count'] = 0
            stock_ticker.reset_index(inplace=True)
            return stock_ticker
        
        sentiment_ticker['timestamp'] = pd.to_datetime(sentiment_ticker['timestamp'])
        sentiment_ticker.set_index('timestamp', inplace=True)
        
        # Resample sentiment to hourly
        sentiment_hourly = sentiment_ticker.resample('1H').agg({
            'sentiment_score': 'mean',
            'confidence': 'mean'
        })
        sentiment_hourly.columns = ['avg_sentiment', 'avg_confidence']
        sentiment_hourly['mention_count'] = sentiment_ticker.resample('1H').size()
        
        # Merge on timestamp
        merged = stock_ticker.join(sentiment_hourly, how='left')
        
        # Fill missing sentiment values with 0
        merged['avg_sentiment'].fillna(0, inplace=True)
        merged['mention_count'].fillna(0, inplace=True)
        merged['avg_confidence'].fillna(0, inplace=True)
        
        merged.reset_index(inplace=True)
        return merged
    
    def calculate_correlation(self, merged_df):
        """
        Calculate correlation between sentiment and price movement
        """
        if merged_df.empty or len(merged_df) < 2:
            return {
                'price_sentiment_corr': 0,
                'volume_sentiment_corr': 0,
                'p_value': 1.0
            }
        
        # Calculate price change
        merged_df['price_change'] = merged_df['Close'].pct_change()
        
        # Remove NaN values
        valid_data = merged_df[['avg_sentiment', 'price_change', 'Volume']].dropna()
        
        if len(valid_data) < 2:
            return {
                'price_sentiment_corr': 0,
                'volume_sentiment_corr': 0,
                'p_value': 1.0
            }
        
        # Calculate Pearson correlation
        price_corr, price_pval = stats.pearsonr(valid_data['avg_sentiment'], valid_data['price_change'])
        
        # Calculate correlation with volume
        volume_corr, _ = stats.pearsonr(valid_data['avg_sentiment'], valid_data['Volume'])
        
        return {
            'price_sentiment_corr': price_corr,
            'volume_sentiment_corr': volume_corr,
            'p_value': price_pval
        }
    
    def calculate_leading_indicators(self, merged_df, lag_hours=1):
        """
        Check if sentiment is a leading indicator for price movement
        """
        if merged_df.empty or len(merged_df) < lag_hours + 1:
            return 0
        
        merged_df = merged_df.copy()
        merged_df['price_change'] = merged_df['Close'].pct_change()
        
        # Shift sentiment to check if it predicts future price
        merged_df['sentiment_lag'] = merged_df['avg_sentiment'].shift(lag_hours)
        
        valid_data = merged_df[['sentiment_lag', 'price_change']].dropna()
        
        if len(valid_data) < 2:
            return 0
        
        corr, _ = stats.pearsonr(valid_data['sentiment_lag'], valid_data['price_change'])
        return corr
    
    def detect_sentiment_spikes(self, sentiment_df, ticker, threshold=2.0):
        """
        Detect unusual sentiment spikes (anomalies)
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty or len(ticker_data) < 10:
            return []
        
        # Calculate rolling statistics
        ticker_data = ticker_data.sort_values('timestamp')
        ticker_data['rolling_mean'] = ticker_data['sentiment_score'].rolling(window=20, min_periods=1).mean()
        ticker_data['rolling_std'] = ticker_data['sentiment_score'].rolling(window=20, min_periods=1).std()
        
        # Detect spikes (values beyond threshold standard deviations)
        ticker_data['z_score'] = (ticker_data['sentiment_score'] - ticker_data['rolling_mean']) / ticker_data['rolling_std']
        
        spikes = ticker_data[abs(ticker_data['z_score']) > threshold]
        
        return spikes[['timestamp', 'sentiment_score', 'z_score', 'text']].to_dict('records')
    
    def calculate_sentiment_volatility(self, sentiment_df, ticker, window_hours=24):
        """
        Calculate sentiment volatility over time
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return 0
        
        ticker_data = ticker_data.sort_values('timestamp')
        ticker_data.set_index('timestamp', inplace=True)
        
        # Resample to hourly and calculate rolling std
        hourly_sentiment = ticker_data['sentiment_score'].resample('1H').mean()
        volatility = hourly_sentiment.rolling(window=window_hours, min_periods=1).std().mean()
        
        return volatility if not np.isnan(volatility) else 0
    
    def get_sentiment_summary(self, sentiment_df, stock_df, ticker):
        """
        Get comprehensive sentiment summary for a ticker
        """
        # Merge data
        merged = self.merge_stock_and_sentiment(stock_df, sentiment_df, ticker)
        
        # Calculate metrics
        correlation = self.calculate_correlation(merged)
        leading_corr = self.calculate_leading_indicators(merged, lag_hours=1)
        volatility = self.calculate_sentiment_volatility(sentiment_df, ticker)
        spikes = self.detect_sentiment_spikes(sentiment_df, ticker)
        
        # Get latest sentiment
        ticker_sentiment = sentiment_df[sentiment_df['ticker'] == ticker]
        if not ticker_sentiment.empty:
            latest_sentiment = ticker_sentiment.sort_values('timestamp').iloc[-1]['sentiment_score']
            avg_sentiment = ticker_sentiment['sentiment_score'].mean()
        else:
            latest_sentiment = 0
            avg_sentiment = 0
        
        return {
            'ticker': ticker,
            'latest_sentiment': latest_sentiment,
            'avg_sentiment': avg_sentiment,
            'sentiment_volatility': volatility,
            'price_correlation': correlation['price_sentiment_corr'],
            'leading_correlation': leading_corr,
            'p_value': correlation['p_value'],
            'spike_count': len(spikes),
            'merged_data': merged
        }