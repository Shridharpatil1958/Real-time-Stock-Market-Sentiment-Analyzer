"""
Data Collection Module
Fetches stock prices and generates simulated sentiment data
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import time


class DataCollector:
    def __init__(self):
        self.stock_tickers = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN']
        
    def fetch_stock_data(self, ticker, period='7d', interval='1h', max_retries=3):
        """
        Fetch real stock price data using yfinance with retry logic
        """
        for attempt in range(max_retries):
            try:
                stock = yf.Ticker(ticker)
                
                # Try different periods if the first one fails
                periods_to_try = [period, '5d', '1mo', '3mo']
                
                for p in periods_to_try:
                    df = stock.history(period=p, interval=interval)
                    
                    if not df.empty:
                        # Limit to requested period if we got more data
                        if p != period:
                            days = int(period.replace('d', ''))
                            cutoff_date = datetime.now() - timedelta(days=days)
                            df = df[df.index >= cutoff_date]
                        
                        df['Ticker'] = ticker
                        df.reset_index(inplace=True)
                        return df
                
                # If all periods fail, generate simulated data as fallback
                print(f"Warning: Could not fetch real data for {ticker}, using simulated data")
                return self._generate_simulated_stock_data(ticker, period, interval)
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {ticker}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retry
                else:
                    print(f"All attempts failed for {ticker}, using simulated data")
                    return self._generate_simulated_stock_data(ticker, period, interval)
        
        return self._generate_simulated_stock_data(ticker, period, interval)
    
    def _generate_simulated_stock_data(self, ticker, period='7d', interval='1h'):
        """
        Generate simulated stock data as fallback when real data is unavailable
        """
        # Parse period
        days = int(period.replace('d', ''))
        
        # Base prices for different stocks
        base_prices = {
            'AAPL': 180.0,
            'TSLA': 250.0,
            'MSFT': 380.0,
            'GOOGL': 140.0,
            'AMZN': 150.0
        }
        
        base_price = base_prices.get(ticker, 100.0)
        
        # Generate timestamps
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Generate hourly timestamps
        timestamps = []
        current = start_date
        while current <= end_date:
            # Only include market hours (9 AM - 4 PM EST, Mon-Fri)
            if current.weekday() < 5 and 9 <= current.hour <= 16:
                timestamps.append(current)
            current += timedelta(hours=1)
        
        # Generate realistic price movements
        prices = []
        current_price = base_price
        
        for i in range(len(timestamps)):
            # Random walk with slight upward bias
            change_percent = np.random.normal(0.001, 0.01)  # 0.1% mean, 1% std
            current_price *= (1 + change_percent)
            prices.append(current_price)
        
        # Generate OHLCV data
        data = []
        for i, timestamp in enumerate(timestamps):
            price = prices[i]
            volatility = price * 0.005  # 0.5% intraday volatility
            
            open_price = price + np.random.normal(0, volatility)
            high_price = max(price, open_price) + abs(np.random.normal(0, volatility))
            low_price = min(price, open_price) - abs(np.random.normal(0, volatility))
            close_price = price
            volume = int(np.random.uniform(1000000, 10000000))
            
            data.append({
                'Datetime': timestamp,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume,
                'Ticker': ticker
            })
        
        df = pd.DataFrame(data)
        return df
    
    def fetch_multiple_stocks(self, tickers, period='7d', interval='1h'):
        """
        Fetch data for multiple stock tickers
        """
        all_data = []
        for ticker in tickers:
            data = self.fetch_stock_data(ticker, period, interval)
            if data is not None and not data.empty:
                all_data.append(data)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        
        # If all failed, return empty DataFrame
        print("Warning: All stock data fetches failed")
        return pd.DataFrame()
    
    def generate_simulated_sentiment_data(self, ticker, num_days=7, posts_per_day=50):
        """
        Generate simulated sentiment data that mimics social media posts
        This simulates Twitter/Reddit data with realistic patterns
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=num_days)
        
        # Generate timestamps
        timestamps = []
        for day in range(num_days):
            current_date = start_date + timedelta(days=day)
            for _ in range(posts_per_day):
                # Add some randomness to post times (more posts during market hours)
                hour = random.choices(
                    range(24), 
                    weights=[1 if 9 <= h <= 16 else 0.3 for h in range(24)]
                )[0]
                minute = random.randint(0, 59)
                timestamp = current_date.replace(hour=hour, minute=minute, second=0)
                timestamps.append(timestamp)
        
        # Generate sentiment scores with realistic patterns
        sentiment_data = []
        for timestamp in timestamps:
            # Base sentiment with some randomness
            base_sentiment = np.random.normal(0, 0.3)
            
            # Add trend component (stocks generally have positive bias in bull market)
            trend = 0.1 if ticker in ['AAPL', 'MSFT', 'GOOGL'] else 0.05
            
            # Add volatility for certain stocks
            volatility = 0.5 if ticker == 'TSLA' else 0.3
            
            sentiment_score = np.clip(base_sentiment + trend + np.random.normal(0, volatility), -1, 1)
            
            # Generate simulated post text
            sentiment_label = 'positive' if sentiment_score > 0.2 else 'negative' if sentiment_score < -0.2 else 'neutral'
            post_templates = {
                'positive': [
                    f"${ticker} looking strong! 🚀",
                    f"Bullish on ${ticker}",
                    f"${ticker} to the moon!",
                    f"Great earnings from ${ticker}",
                    f"${ticker} is my top pick"
                ],
                'negative': [
                    f"${ticker} overvalued",
                    f"Bearish on ${ticker}",
                    f"${ticker} might drop",
                    f"Selling my ${ticker} position",
                    f"${ticker} concerns me"
                ],
                'neutral': [
                    f"Watching ${ticker}",
                    f"${ticker} holding steady",
                    f"Thoughts on ${ticker}?",
                    f"${ticker} analysis needed",
                    f"${ticker} sideways movement"
                ]
            }
            
            post_text = random.choice(post_templates[sentiment_label])
            
            sentiment_data.append({
                'timestamp': timestamp,
                'ticker': ticker,
                'sentiment_score': sentiment_score,
                'text': post_text,
                'source': random.choice(['Twitter', 'Reddit', 'News']),
                'confidence': abs(sentiment_score)
            })
        
        df = pd.DataFrame(sentiment_data)
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df
    
    def generate_sentiment_for_multiple_stocks(self, tickers, num_days=7):
        """
        Generate sentiment data for multiple stocks
        """
        all_sentiment = []
        for ticker in tickers:
            sentiment_df = self.generate_simulated_sentiment_data(ticker, num_days)
            all_sentiment.append(sentiment_df)
        
        if all_sentiment:
            return pd.concat(all_sentiment, ignore_index=True)
        return pd.DataFrame()
    
    def get_latest_stock_info(self, ticker):
        """
        Get latest stock information including current price and market cap
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Try to get current price from info
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            previous_close = info.get('previousClose', 0)
            
            # If info is empty or prices are 0, use simulated data
            if not info or current_price == 0:
                print(f"Warning: Could not fetch info for {ticker}, using simulated data")
                return self._generate_simulated_stock_info(ticker)
            
            return {
                'ticker': ticker,
                'current_price': current_price,
                'previous_close': previous_close,
                'market_cap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'company_name': info.get('longName', ticker)
            }
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return self._generate_simulated_stock_info(ticker)
    
    def _generate_simulated_stock_info(self, ticker):
        """
        Generate simulated stock info as fallback
        """
        base_prices = {
            'AAPL': 180.0,
            'TSLA': 250.0,
            'MSFT': 380.0,
            'GOOGL': 140.0,
            'AMZN': 150.0
        }
        
        company_names = {
            'AAPL': 'Apple Inc.',
            'TSLA': 'Tesla, Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com, Inc.'
        }
        
        base_price = base_prices.get(ticker, 100.0)
        current_price = base_price * (1 + np.random.normal(0, 0.02))
        previous_close = current_price * (1 + np.random.normal(-0.01, 0.02))
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'previous_close': previous_close,
            'market_cap': int(current_price * 1e9),  # Simulated market cap
            'volume': int(np.random.uniform(50000000, 100000000)),
            'company_name': company_names.get(ticker, ticker)
        }