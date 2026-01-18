# 📈 Real-time Stock Market Sentiment Analyzer

A sophisticated, single-screen dashboard that analyzes real-time sentiment from social media and correlates it with stock price movements. Built with Streamlit and featuring a sleek dark theme with modern UI/UX design.

## 📸 Dashboard Screenshots

### 📈 Main Dashboard – Real-Time Sentiment Overview
AI-Powered Stock Sentiment Dashboard
<img width="1919" height="924" alt="Screenshot 2026-01-15 142346" src="https://github.com/user-attachments/assets/8adcfabc-b6e3-4ef4-9874-7a5404e4bead" />
Displays real-time sentiment scores, current stock prices, price changes, and sentiment-price correlation for selected stocks using live market and social data.

### 🔍 Stock Selection & Time Range Control
Interactive Stock & Time Range Selection
<img width="1920" height="927" alt="Screenshot 2026-01-15 142421" src="https://github.com/user-attachments/assets/6295cae8-d65b-4692-a488-b0ade0c10d16" />
Allows users to switch between multiple stocks (AAPL, TSLA, MSFT, GOOGL, AMZN) and analyze sentiment trends over a selected time window with auto-refresh support.

### 📊 Detailed Stock Analysis
Sentiment Strength & Price Movement Analysis
<img width="1919" height="921" alt="Screenshot 2026-01-15 142409" src="https://github.com/user-attachments/assets/f00742dc-bd1d-44c6-bd60-f7ac4522f686" />
Provides a detailed breakdown of sentiment strength using gauge indicators and time-series visualization comparing stock price movements with sentiment fluctuations.

### 🔗 Correlation Analysis Dashboard
Sentiment vs Price Correlation Insights
<img width="1918" height="926" alt="Screenshot 2026-01-15 142440" src="https://github.com/user-attachments/assets/a1f64c7c-4c11-40a5-a17f-8ef618914fc4" />
Shows correlation metrics such as average sentiment, price correlation, leading correlation, and sentiment volatility to evaluate how public sentiment impacts stock prices.

## ✨ Features

### 📊 **Multi-Stock Dashboard**
- Monitor up to 5 stocks simultaneously
- Real-time price updates with percentage changes
- Market capitalization display
- Sentiment scores with visual indicators

### 💬 **Sentiment Analysis**
- Simulated social media data (Twitter, Reddit, News)
- VADER sentiment scoring
- Positive/Negative/Neutral classification
- Top mentions tracking

### 📈 **Advanced Analytics**
- Sentiment vs Price correlation analysis
- Leading indicators (1-hour ahead prediction)
- Sentiment volatility metrics
- Statistical significance testing (p-values)
- Anomaly detection for sentiment spikes

### 🎨 **Visual Components**
- Interactive Plotly charts
- Sentiment gauge meters
- Candlestick price charts
- Correlation heatmaps
- Multi-stock comparison graphs
- Mention volume tracking
- Distribution pie charts

### 🌐 **Modern UI/UX**
- Dark theme with neon glow effects
- Single-screen optimized layout
- Responsive design
- Smooth animations and transitions
- Compact, information-dense interface

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/stock-sentiment-analyzer.git
cd stock-sentiment-analyzer
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.28
plotly>=5.17.0
vaderSentiment>=3.3.2
scipy>=1.11.0
```

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Configuration

**Sidebar Settings:**
- **Stock Selection**: Choose from AAPL, TSLA, MSFT, GOOGL, AMZN
- **Time Range**: Select 1-30 days of historical data
- **Auto-refresh**: Enable 5-minute automatic data updates

### Navigation

The dashboard has 4 main tabs:

#### 📊 **Overview**
- Quick view of all selected stocks
- Multi-stock comparison chart
- Correlation heatmap
- Key metrics at a glance

#### 📈 **Analysis**
- Detailed single-stock analysis
- Sentiment gauge visualization
- Sentiment vs Price overlay chart
- Volume of mentions
- Sentiment distribution
- Candlestick price chart

#### 🔍 **Correlation**
- Comprehensive correlation table
- Statistical significance indicators
- Sentiment anomaly detection
- Leading correlation metrics

#### 💬 **Mentions**
- Top 5 positive mentions
- Top 5 negative mentions
- Source attribution (Twitter/Reddit/News)
- Sentiment scores for each mention

## 📁 Project Structure

```
stock-sentiment-analyzer/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Project dependencies
├── README.md                       # Project documentation
│
├── styles/
│   └── custom_styles.py           # Custom CSS styling
│
├── modules/
│   ├── __init__.py
│   ├── data_collector.py          # Stock & sentiment data collection
│   ├── sentiment_analyzer.py      # VADER sentiment analysis
│   ├── data_processor.py          # Data processing & correlations
│   └── visualizations.py          # Plotly chart generation
│
└── utils/
    ├── __init__.py
    └── helpers.py                  # Helper functions
```

## 🛠️ Component Details

### Data Collector (`modules/data_collector.py`)
- Fetches real-time stock data from Yahoo Finance
- Generates simulated social media sentiment data
- Supports multiple tickers and time periods
- Configurable data intervals

### Sentiment Analyzer (`modules/sentiment_analyzer.py`)
- VADER (Valence Aware Dictionary and sEntiment Reasoner) implementation
- Compound sentiment scoring (-1 to +1)
- Text preprocessing and cleaning
- Top mentions extraction

### Data Processor (`modules/data_processor.py`)
- Merges stock and sentiment data
- Calculates correlations (Pearson)
- Statistical significance testing
- Anomaly detection (z-score based)
- Leading indicator analysis

### Visualizations (`modules/visualizations.py`)
- Plotly interactive charts
- Custom color schemes
- Dark theme optimization
- Responsive layouts

### Custom Styles (`styles/custom_styles.py`)
- Dark gradient background
- Neon glow effects
- Compact single-screen layout
- Custom metric cards
- Animated hover states

## 🎨 Design Philosophy

### Single-Screen Optimization
- All content visible without excessive scrolling
- Compact metrics and charts (50-70% size reduction)
- Efficient use of horizontal space
- Scrollable sections where needed

### Modern Aesthetic
- **Typography**: Poppins font family for modern look
- **Colors**: Dark theme with indigo/purple gradients
- **Effects**: Subtle glow, shadows, and animations
- **Layout**: Card-based design with clear hierarchy

### Performance
- Cached data loading (5-minute TTL)
- Lazy component initialization
- Optimized chart rendering
- Minimal re-renders

## 📊 Data Sources

### Stock Data
- **Provider**: Yahoo Finance (via yfinance)
- **Update Frequency**: Real-time (with 15-min delay)
- **Metrics**: Open, High, Low, Close, Volume, Market Cap

### Sentiment Data
- **Type**: Simulated (for demo purposes)
- **Sources**: Twitter, Reddit, News (simulated)
- **Frequency**: Hourly mentions
- **Scoring**: VADER compound sentiment

> ⚠️ **Note**: This project uses simulated sentiment data for demonstration. For production use, integrate real social media APIs (Twitter API, Reddit API, News APIs).

## 🔧 Customization

### Adding New Stocks

Edit `app.py`:
```python
available_tickers = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX']
```

### Adjusting Time Ranges

Modify slider in `app.py`:
```python
num_days = st.sidebar.slider(
    "Days:",
    min_value=1,
    max_value=60,  # Increase to 60 days
    value=7
)
```

### Changing Color Scheme

Edit CSS variables in `styles/custom_styles.py`:
```css
:root {
    --primary-color: #6366f1;      /* Change primary color */
    --success-color: #10b981;      /* Change success color */
    --danger-color: #ef4444;       /* Change danger color */
}
```

### Modifying Chart Heights

In `app.py`, adjust chart layouts:
```python
fig.update_layout(height=280)  # Change to desired height
```

## 📈 Use Cases

### Financial Analysis
- Track sentiment trends for investment decisions
- Identify sentiment-driven price movements
- Detect anomalies that may indicate market events

### Research
- Study correlation between social sentiment and stock prices
- Analyze leading indicators
- Test sentiment prediction models

### Education
- Learn about sentiment analysis techniques
- Understand stock market dynamics
- Practice data visualization

### Demo & Presentation
- Showcase real-time analytics capabilities
- Demonstrate modern dashboard design
- Present data-driven insights

## 🚨 Limitations

1. **Simulated Data**: Uses generated sentiment data, not real social media feeds
2. **Market Hours**: Stock data limited to market trading hours
3. **Correlation ≠ Causation**: Statistical correlation doesn't imply predictive power
4. **15-min Delay**: Yahoo Finance data has a 15-minute delay
5. **Demo Purpose**: Not intended for actual trading decisions


## 👨‍💻 Author

**Shridhar Patil**
- GitHub: [@Shridharpatil1958](https://github.com/Shridharpatil1958)
- LinkedIn: [Shridhar Patil](www.linkedin.com/in/shridhar-patil-908480220)
- Email: patilshridhar1958@gmail.com

## 🙏 Acknowledgments

- **Streamlit** - Amazing framework for data apps
- **yfinance** - Yahoo Finance data access
- **VADER Sentiment** - Sentiment analysis tool
- **Plotly** - Interactive visualization library

## 🐛 Known Issues

1. **Cache Persistence**: Data cache clears on app restart
2. **Memory Usage**: Large datasets may consume significant memory
3. **Browser Compatibility**: Best viewed in Chrome/Firefox/Edge

## 💡 Tips

- Use auto-refresh for live monitoring
- Start with 7 days for optimal performance
- Select 2-3 stocks for detailed analysis
- Check p-values for correlation reliability
- Monitor sentiment spikes for trading signals


## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**⚠️ Disclaimer**: This project is for educational and demonstration purposes only. It is NOT financial advice. Always consult with qualified financial advisors before making investment decisions. Past performance does not guarantee future results.

---

Made with ❤️ and Python | © 2026 Stock Market Sentiment Analyzer


[def]: https://www.linkedin.com/in/shridhar-patil-908480220

