"""
Visualization Components
Creates interactive charts using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class Visualizations:
    def __init__(self):
        self.color_positive = '#00C853'
        self.color_negative = '#D32F2F'
        self.color_neutral = '#FFA726'
    
    def create_sentiment_gauge(self, sentiment_score, ticker):
        """
        Create a gauge chart for sentiment score
        """
        # Normalize sentiment score to 0-100 scale
        normalized_score = (sentiment_score + 1) * 50
        
        # Determine color
        if sentiment_score > 0.2:
            color = self.color_positive
        elif sentiment_score < -0.2:
            color = self.color_negative
        else:
            color = self.color_neutral
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=normalized_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{ticker} Sentiment", 'font': {'size': 20}},
            delta={'reference': 50, 'increasing': {'color': self.color_positive}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': '#FFCDD2'},
                    {'range': [30, 70], 'color': '#FFE0B2'},
                    {'range': [70, 100], 'color': '#C8E6C9'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': normalized_score
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_sentiment_vs_price_chart(self, merged_df, ticker):
        """
        Create dual-axis chart comparing sentiment and stock price
        """
        if merged_df.empty:
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{ticker} Stock Price', 'Sentiment Score'),
            row_heights=[0.6, 0.4]
        )
        
        # Stock price line
        fig.add_trace(
            go.Scatter(
                x=merged_df['timestamp'],
                y=merged_df['Close'],
                name='Price',
                line=dict(color='#1976D2', width=2),
                fill='tonexty',
                fillcolor='rgba(25, 118, 210, 0.1)'
            ),
            row=1, col=1
        )
        
        # Sentiment line
        fig.add_trace(
            go.Scatter(
                x=merged_df['timestamp'],
                y=merged_df['avg_sentiment'],
                name='Sentiment',
                line=dict(color=self.color_positive, width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 200, 83, 0.1)'
            ),
            row=2, col=1
        )
        
        # Add zero line for sentiment
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
        
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Sentiment", row=2, col=1)
        
        fig.update_layout(
            height=600,
            showlegend=True,
            hovermode='x unified',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_mention_volume_chart(self, sentiment_df, ticker):
        """
        Create bar chart showing volume of mentions over time
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return go.Figure()
        
        # Aggregate by hour
        ticker_data['timestamp'] = pd.to_datetime(ticker_data['timestamp'])
        ticker_data.set_index('timestamp', inplace=True)
        hourly_counts = ticker_data.resample('1H').size().reset_index()
        hourly_counts.columns = ['timestamp', 'count']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=hourly_counts['timestamp'],
            y=hourly_counts['count'],
            name='Mentions',
            marker_color='#42A5F5',
            hovertemplate='<b>%{x}</b><br>Mentions: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'{ticker} - Volume of Mentions Over Time',
            xaxis_title='Time',
            yaxis_title='Number of Mentions',
            height=400,
            hovermode='x',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_sentiment_distribution_pie(self, sentiment_df, ticker):
        """
        Create pie chart showing sentiment distribution
        """
        ticker_data = sentiment_df[sentiment_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return go.Figure()
        
        # Categorize sentiment
        positive = len(ticker_data[ticker_data['sentiment_score'] > 0.2])
        negative = len(ticker_data[ticker_data['sentiment_score'] < -0.2])
        neutral = len(ticker_data) - positive - negative
        
        fig = go.Figure(data=[go.Pie(
            labels=['Positive', 'Neutral', 'Negative'],
            values=[positive, neutral, negative],
            marker=dict(colors=[self.color_positive, self.color_neutral, self.color_negative]),
            hole=0.4,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title=f'{ticker} - Sentiment Distribution',
            height=400,
            showlegend=True,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_correlation_heatmap(self, correlation_data):
        """
        Create heatmap showing correlation between sentiment and price for multiple stocks
        """
        if not correlation_data:
            return go.Figure()
        
        tickers = list(correlation_data.keys())
        correlations = [correlation_data[t]['price_correlation'] for t in tickers]
        
        # Create matrix for heatmap
        matrix = [[correlations[i]] for i in range(len(tickers))]
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=['Sentiment-Price Correlation'],
            y=tickers,
            colorscale='RdYlGn',
            zmid=0,
            text=[[f'{c:.3f}'] for c in correlations],
            texttemplate='%{text}',
            textfont={"size": 14},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Sentiment-Price Correlation Heatmap',
            height=400,
            margin=dict(l=100, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_candlestick_chart(self, stock_df, ticker):
        """
        Create candlestick chart for stock price
        """
        ticker_data = stock_df[stock_df['Ticker'] == ticker].copy()
        
        if ticker_data.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Candlestick(
            x=ticker_data['Datetime'] if 'Datetime' in ticker_data.columns else ticker_data['Date'],
            open=ticker_data['Open'],
            high=ticker_data['High'],
            low=ticker_data['Low'],
            close=ticker_data['Close'],
            name=ticker
        )])
        
        fig.update_layout(
            title=f'{ticker} - Price Movement (Candlestick)',
            xaxis_title='Time',
            yaxis_title='Price ($)',
            height=500,
            xaxis_rangeslider_visible=False,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_multi_stock_comparison(self, sentiment_summaries):
        """
        Create comparison chart for multiple stocks
        """
        if not sentiment_summaries:
            return go.Figure()
        
        tickers = list(sentiment_summaries.keys())
        avg_sentiments = [sentiment_summaries[t]['avg_sentiment'] for t in tickers]
        correlations = [sentiment_summaries[t]['price_correlation'] for t in tickers]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Average Sentiment', 'Price Correlation'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Average sentiment bars
        colors_sentiment = [self.color_positive if s > 0 else self.color_negative for s in avg_sentiments]
        fig.add_trace(
            go.Bar(x=tickers, y=avg_sentiments, marker_color=colors_sentiment, name='Sentiment'),
            row=1, col=1
        )
        
        # Correlation bars
        colors_corr = [self.color_positive if c > 0 else self.color_negative for c in correlations]
        fig.add_trace(
            go.Bar(x=tickers, y=correlations, marker_color=colors_corr, name='Correlation'),
            row=1, col=2
        )
        
        fig.update_yaxes(title_text="Sentiment Score", row=1, col=1)
        fig.update_yaxes(title_text="Correlation", row=1, col=2)
        
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig