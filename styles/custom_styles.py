import streamlit as st


def get_custom_css():
    """
    Returns comprehensive custom CSS for the Streamlit application
    """
    return """
    <style>
        /* ========================================
           GLOBAL STYLES & IMPORTS
        ======================================== */
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        :root {
            --primary-color: #1f77b4;
            --primary-dark: #1565a8;
            --secondary-color: #2c3e50;
            --success-color: #2ecc71;
            --danger-color: #e74c3c;
            --warning-color: #f39c12;
            --info-color: #17a2b8;
            --bg-light: #f8f9fa;
            --bg-card: #ffffff;
            --border-color: #dee2e6;
            --text-primary: #2c3e50;
            --text-secondary: #6c757d;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 8px rgba(0,0,0,0.12);
            --shadow-lg: 0 8px 16px rgba(0,0,0,0.16);
        }
        
        /* ========================================
           HIDE STREAMLIT BRANDING
        ======================================== */
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ========================================
           MAIN CONTAINER
        ======================================== */
        
        .main {
            background-color: var(--bg-light);
            padding: 0.2rem;
        }
        
        .block-container {
            padding-top: 0.2rem;
            padding-bottom: 0.2rem;
            max-width: 1400px;
        }
        
        /* ========================================
           CUSTOM HEADERS
        ======================================== */
        
        .main-header {
            font-size: 2rem;
            font-weight: 100;
            text-align: center;
            background: linear-gradient(135deg, #1f77b4 0%, #2c3e50 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            padding: 0.5rem 0;
            margin-bottom: 1rem;
            letter-spacing: -1px;
        }
        
        .section-header {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--secondary-color);
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--primary-color);
        }
        
        .subsection-header {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 1.5rem 0 1rem 0;
        }
        
        /* ========================================
           STREAMLIT METRIC CARDS
        ======================================== */
        
        .stMetric {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            border-left: 4px solid var(--primary-color);
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-4px);
        }
        
        .stMetric label {
            font-size: 0.875rem !important;
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
        }
        
        .stMetric [data-testid="stMetricDelta"] {
            font-size: 1rem !important;
            font-weight: 600 !important;
        }
        
        /* ========================================
           CUSTOM METRIC CARDS
        ======================================== */
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
            border-left: 4px solid var(--primary-color);
            margin: 1rem 0;
        }
        
        .metric-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-4px);
        }
        
        .metric-card h3 {
            color: var(--secondary-color);
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .metric-label {
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0.5rem 0;
        }
        
        .metric-delta {
            display: inline-block;
            margin-left: 0.75rem;
            font-size: 1rem;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .metric-delta.positive {
            background-color: #d4edda;
            color: var(--success-color);
        }
        
        .metric-delta.negative {
            background-color: #f8d7da;
            color: var(--danger-color);
        }
        
        /* ========================================
           SENTIMENT BADGES
        ======================================== */
        
        .sentiment-badge {
            display: inline-block;
            padding: 0.5rem 1.25rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 0.5rem 0;
            letter-spacing: 0.3px;
        }
        
        .sentiment-positive, .sentiment-badge.positive {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            border: 2px solid #b1dfbb;
        }
        
        .sentiment-neutral, .sentiment-badge.neutral {
            background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%);
            color: #856404;
            border: 2px solid #ffd966;
        }
        
        .sentiment-negative, .sentiment-badge.negative {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            color: #721c24;
            border: 2px solid #f1b0b7;
        }
        
        /* ========================================
           MENTION CARDS
        ======================================== */
        
        .mention-card {
            background: white;
            border-left: 4px solid var(--primary-color);
            padding: 1.25rem;
            margin: 0.75rem 0;
            border-radius: 8px;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
        }
        
        .mention-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateX(6px);
        }
        
        .mention-card.positive {
            border-left-color: var(--success-color);
            background: linear-gradient(to right, #f0fff4 0%, white 10%);
        }
        
        .mention-card.negative {
            border-left-color: var(--danger-color);
            background: linear-gradient(to right, #fff5f5 0%, white 10%);
        }
        
        .mention-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        
        .mention-source {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .mention-timestamp {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }
        
        .mention-score {
            font-weight: 700;
            color: var(--primary-color);
            font-size: 0.9rem;
            padding: 0.25rem 0.75rem;
            background-color: #e7f3ff;
            border-radius: 12px;
        }
        
        .mention-text {
            font-style: italic;
            color: var(--text-primary);
            line-height: 1.6;
            padding: 0.5rem;
            background-color: #f8f9fa;
            border-radius: 6px;
            font-size: 0.95rem;
        }
        
        /* ========================================
           TABS STYLING
        ======================================== */
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
            padding: 0.5rem 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 10px 10px 0 0;
            padding: 0.875rem 1.75rem;
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-secondary);
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #f8f9fa;
            color: var(--primary-color);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white !important;
            border-color: var(--primary-color);
            box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3);
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 1.5rem;
        }
        
        /* ========================================
           SIDEBAR STYLING
        ======================================== */
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
            box-shadow: 2px 0 12px rgba(0,0,0,0.08);
            padding: 0.5rem 0.5rem;
        }
        
        [data-testid="stSidebar"] .element-container {
            margin-bottom: 1rem;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: var(--primary-color);
            font-weight: 700;
        }
        
        /* ========================================
           BUTTON STYLING
        ======================================== */
        
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.875rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(31, 119, 180, 0.2);
            letter-spacing: 0.3px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(31, 119, 180, 0.35);
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        /* ========================================
           SELECTBOX STYLING
        ======================================== */
        
        .stSelectbox > div > div {
            background-color: white;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:hover {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
        }
        
        /* ========================================
           MULTISELECT STYLING
        ======================================== */
        
        .stMultiSelect > div > div {
            background-color: white;
            border: 2px solid var(--border-color);
            border-radius: 8px;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background-color: var(--primary-color) !important;
            color: white !important;
            border-radius: 6px;
            font-weight: 600;
        }
        
        /* ========================================
           SLIDER STYLING
        ======================================== */
        
        .stSlider > div > div > div {
            background-color: var(--primary-color);
        }
        
        .stSlider [role="slider"] {
            background-color: white;
            border: 3px solid var(--primary-color);
            box-shadow: 0 2px 8px rgba(31, 119, 180, 0.3);
        }
        
        /* ========================================
           CHECKBOX STYLING
        ======================================== */
        
        .stCheckbox {
            padding: 0.5rem;
            border-radius: 6px;
            transition: background-color 0.2s ease;
        }
        
        .stCheckbox:hover {
            background-color: var(--bg-light);
        }
        
        .stCheckbox > label {
            font-weight: 500;
        }
        
        /* ========================================
           DATAFRAME/TABLE STYLING
        ======================================== */
        
        .dataframe {
            border: none !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: var(--shadow-sm);
        }
        
        .dataframe thead tr th {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 1rem !important;
            text-align: left !important;
            font-size: 0.9rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .dataframe tbody tr {
            transition: background-color 0.2s ease;
        }
        
        .dataframe tbody tr:hover {
            background-color: #f8f9fa !important;
        }
        
        .dataframe tbody tr td {
            padding: 0.875rem 1rem !important;
            border-bottom: 1px solid var(--border-color) !important;
        }
        
        /* ========================================
           ALERT/INFO BOXES
        ======================================== */
        
        .info-box {
            background: linear-gradient(135deg, #e7f3ff 0%, #f0f8ff 100%);
            border-left: 4px solid var(--primary-color);
            padding: 1.25rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: var(--shadow-sm);
        }
        
        .info-box strong {
            color: var(--primary-color);
            display: block;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .alert-success {
            background-color: #d4edda;
            border-left: 4px solid var(--success-color);
            padding: 1.25rem;
            border-radius: 8px;
            color: #155724;
            margin: 1rem 0;
            box-shadow: var(--shadow-sm);
            font-weight: 500;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            border-left: 4px solid var(--warning-color);
            padding: 1.25rem;
            border-radius: 8px;
            color: #856404;
            margin: 1rem 0;
            box-shadow: var(--shadow-sm);
            font-weight: 500;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            border-left: 4px solid var(--danger-color);
            padding: 1.25rem;
            border-radius: 8px;
            color: #721c24;
            margin: 1rem 0;
            box-shadow: var(--shadow-sm);
            font-weight: 500;
        }
        
        .alert-info {
            background-color: #d1ecf1;
            border-left: 4px solid var(--info-color);
            padding: 1.25rem;
            border-radius: 8px;
            color: #0c5460;
            margin: 1rem 0;
            box-shadow: var(--shadow-sm);
            font-weight: 500;
        }
        
        /* ========================================
           PLOTLY CHART CONTAINERS
        ======================================== */
        
        .js-plotly-plot {
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            background: white;
            padding: 1rem;
        }
        
        /* ========================================
           FOOTER
        ======================================== */
        
        .footer {
            text-align: center;
            padding: 2.5rem 1rem;
            color: var(--text-secondary);
            border-top: 2px solid var(--border-color);
            margin-top: 4rem;
            background: linear-gradient(180deg, transparent 0%, #f8f9fa 50%);
        }
        
        .footer strong {
            color: var(--primary-color);
            font-size: 1.1rem;
        }
        
        /* ========================================
           LOADING/SPINNER
        ======================================== */
        
        .stSpinner > div {
            border-top-color: var(--primary-color) !important;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* ========================================
           EXPANDER STYLING
        ======================================== */
        
        .streamlit-expanderHeader {
            background-color: white;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: var(--primary-color);
            background-color: #f8f9fa;
        }
        
        /* ========================================
           STOCK GRID LAYOUT
        ======================================== */
        
        .stock-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }
        
        /* ========================================
           RESPONSIVE DESIGN
        ======================================== */
        
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            
            .section-header {
                font-size: 1.5rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
            
            .mention-card {
                margin: 0.5rem 0;
                padding: 1rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 0.625rem 1rem;
                font-size: 0.875rem;
            }
        }
        
        /* ========================================
           CUSTOM SCROLLBAR
        ======================================== */
        
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-dark);
        }
        
        /* ========================================
           ANIMATIONS
        ======================================== */
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(-100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .slide-in {
            animation: slideIn 0.4s ease-out;
        }
    </style>
    """


def inject_custom_css():
    """
    Inject custom CSS into the Streamlit application.
    Call this function once at the beginning of your app.
    """
    st.markdown(get_custom_css(), unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS FOR CUSTOM HTML COMPONENTS
# ============================================================================

def create_metric_card(title, value, delta=None, sentiment=None):
    """
    Create a custom metric card with optional delta and sentiment
    
    Args:
        title: Card title
        value: Main metric value
        delta: Optional change value (e.g., "+2.34%")
        sentiment: Optional sentiment badge text
    """
    delta_html = ""
    if delta:
        delta_class = "positive" if "+" in str(delta) else "negative"
        delta_html = f'<span class="metric-delta {delta_class}">{delta}</span>'
    
    sentiment_html = ""
    if sentiment:
        sentiment_html = f'<div class="sentiment-badge">{sentiment}</div>'
    
    return f"""
    <div class="metric-card">
        <h3>{title}</h3>
        <div class="metric-value">{value}{delta_html}</div>
        {sentiment_html}
    </div>
    """


def create_mention_card(source, timestamp, score, text, sentiment_type="positive"):
    """
    Create a mention card for social media posts
    
    Args:
        source: Source platform (e.g., "Twitter", "Reddit")
        timestamp: Timestamp string
        score: Sentiment score
        text: Mention text
        sentiment_type: "positive" or "negative"
    """
    return f"""
    <div class="mention-card {sentiment_type}">
        <div class="mention-header">
            <div>
                <span class="mention-source">{source}</span>
                <span class="mention-timestamp"> - {timestamp}</span>
            </div>
            <span class="mention-score">Score: {score:.3f}</span>
        </div>
        <div class="mention-text">"{text}"</div>
    </div>
    """


def create_alert(message, alert_type="info"):
    """
    Create an alert box
    
    Args:
        message: Alert message
        alert_type: "success", "warning", "danger", or "info"
    """
    icons = {
        "success": "✅",
        "warning": "⚠️",
        "danger": "❌",
        "info": "ℹ️"
    }
    
    icon = icons.get(alert_type, "ℹ️")
    
    return f"""
    <div class="alert-{alert_type}">
        {icon} {message}
    </div>
    """


def create_sentiment_badge(sentiment_score, label=None):
    """
    Create a sentiment badge
    
    Args:
        sentiment_score: Numerical sentiment score
        label: Optional custom label
    """
    if sentiment_score > 0.3:
        sentiment_class = "positive"
        default_label = "Positive"
    elif sentiment_score < -0.3:
        sentiment_class = "negative"
        default_label = "Negative"
    else:
        sentiment_class = "neutral"
        default_label = "Neutral"
    
    display_label = label or default_label
    
    return f"""
    <span class="sentiment-badge {sentiment_class}">
        {display_label} ({sentiment_score:.3f})
    </span>
    """


# Example usage in app.py:
"""
from styles.custom_styles import (
    inject_custom_css, 
    create_metric_card, 
    create_mention_card,
    create_alert,
    create_sentiment_badge
)

# Inject CSS at the beginning
inject_custom_css()

# Use custom components
st.markdown(create_metric_card("Apple Inc.", "$178.52", "+2.34%"), unsafe_allow_html=True)
st.markdown(create_alert("Data loaded successfully!", "success"), unsafe_allow_html=True)
st.markdown(create_mention_card("Twitter", "2026-01-14 15:30", 0.856, 
                                "Great stock!", "positive"), unsafe_allow_html=True)
"""