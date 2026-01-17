// Mock data for demonstration
const mockStockData = {
    AAPL: { name: 'Apple Inc.', price: 182.45, change: 2.34, sentiment: 0.65, correlation: 0.72 },
    TSLA: { name: 'Tesla, Inc.', price: 248.92, change: -1.23, sentiment: 0.45, correlation: 0.58 },
    MSFT: { name: 'Microsoft Corporation', price: 378.15, change: 1.87, sentiment: 0.58, correlation: 0.68 },
    GOOGL: { name: 'Alphabet Inc.', price: 142.67, change: 0.95, sentiment: 0.52, correlation: 0.61 },
    AMZN: { name: 'Amazon.com, Inc.', price: 151.34, change: -0.67, sentiment: 0.48, correlation: 0.55 }
};

let selectedStocks = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN'];
let autoRefreshEnabled = false;
let autoRefreshInterval = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updateStockGrid();
    updateLastUpdate();
    initializeCharts();
});

// Toggle stock selection
function toggleStock(element) {
    const ticker = element.getAttribute('data-ticker');
    element.classList.toggle('active');
    
    if (selectedStocks.includes(ticker)) {
        selectedStocks = selectedStocks.filter(t => t !== ticker);
    } else {
        selectedStocks.push(ticker);
    }
    
    updateStockGrid();
    updateCharts();
}

// Update time range
function updateTimeRange(value) {
    document.getElementById('timeRangeValue').textContent = value + ' days';
}

// Refresh data
function refreshData() {
    const btn = event.target.closest('.btn');
    btn.innerHTML = '<span class="loading"></span> Refreshing...';
    btn.disabled = true;
    
    setTimeout(() => {
        updateStockGrid();
        updateCharts();
        updateLastUpdate();
        btn.innerHTML = '<span class="icon">🔄</span> Refresh Data';
        btn.disabled = false;
    }, 1500);
}

// Toggle auto-refresh
function toggleAutoRefresh() {
    autoRefreshEnabled = document.getElementById('autoRefresh').checked;
    
    if (autoRefreshEnabled) {
        autoRefreshInterval = setInterval(() => {
            refreshData();
        }, 300000); // 5 minutes
    } else {
        if (autoRefreshInterval) {
            clearInterval(autoRefreshInterval);
        }
    }
}

// Update stock grid
function updateStockGrid() {
    const grid = document.getElementById('stockGrid');
    grid.innerHTML = '';
    
    selectedStocks.forEach(ticker => {
        const stock = mockStockData[ticker];
        const changeClass = stock.change >= 0 ? 'positive' : 'negative';
        const changeSymbol = stock.change >= 0 ? '▲' : '▼';
        const sentimentClass = stock.sentiment > 0.2 ? 'positive' : stock.sentiment < -0.2 ? 'negative' : 'neutral';
        const sentimentLabel = stock.sentiment > 0.2 ? 'Bullish' : stock.sentiment < -0.2 ? 'Bearish' : 'Neutral';
        
        const card = document.createElement('div');
        card.className = 'stock-card';
        card.innerHTML = `
            <h3>${stock.name}</h3>
            <div class="metric">
                <span class="metric-label">Current Price</span>
                <div>
                    <span class="metric-value">$${stock.price.toFixed(2)}</span>
                    <span class="metric-delta ${changeClass}">${changeSymbol} ${Math.abs(stock.change).toFixed(2)}%</span>
                </div>
            </div>
            <div class="metric">
                <span class="metric-label">Sentiment</span>
                <div>
                    <span class="metric-value ${sentimentClass}">${sentimentLabel}</span>
                    <span class="metric-delta">(${stock.sentiment.toFixed(3)})</span>
                </div>
            </div>
            <div class="metric">
                <span class="metric-label">Correlation</span>
                <span class="metric-value">${stock.correlation.toFixed(3)}</span>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Switch tabs
function switchTab(tabName) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab
    event.target.classList.add('active');
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Update charts for the active tab
    if (tabName === 'overview') {
        updateOverviewCharts();
    } else if (tabName === 'analysis') {
        updateDetailedAnalysis();
    } else if (tabName === 'correlation') {
        updateCorrelationTable();
    } else if (tabName === 'mentions') {
        updateMentions();
    }
}

// Initialize charts
function initializeCharts() {
    updateOverviewCharts();
}

// Update overview charts
function updateOverviewCharts() {
    // Multi-stock comparison
    const sentiments = selectedStocks.map(t => mockStockData[t].sentiment);
    const correlations = selectedStocks.map(t => mockStockData[t].correlation);
    
    const comparisonData = [
        {
            x: selectedStocks,
            y: sentiments,
            type: 'bar',
            name: 'Sentiment',
            marker: { color: sentiments.map(s => s > 0 ? '#00C853' : '#D32F2F') }
        }
    ];
    
    const comparisonLayout = {
        title: 'Average Sentiment by Stock',
        paper_bgcolor: '#1A1A1A',
        plot_bgcolor: '#0A0A0A',
        font: { color: '#FFFFFF' },
        xaxis: { gridcolor: '#333333' },
        yaxis: { gridcolor: '#333333', title: 'Sentiment Score' }
    };
    
    Plotly.newPlot('comparisonChart', comparisonData, comparisonLayout, {responsive: true});
    
    // Correlation heatmap
    const heatmapData = [{
        z: [correlations],
        x: selectedStocks,
        y: ['Correlation'],
        type: 'heatmap',
        colorscale: 'RdYlGn',
        zmid: 0
    }];
    
    const heatmapLayout = {
        title: 'Sentiment-Price Correlation',
        paper_bgcolor: '#1A1A1A',
        plot_bgcolor: '#0A0A0A',
        font: { color: '#FFFFFF' }
    };
    
    Plotly.newPlot('heatmapChart', heatmapData, heatmapLayout, {responsive: true});
}

// Update detailed analysis
function updateDetailedAnalysis() {
    const ticker = document.getElementById('stockSelector').value;
    const stock = mockStockData[ticker];
    
    // Update metrics
    document.getElementById('avgSentiment').textContent = stock.sentiment.toFixed(3);
    document.getElementById('sentimentVol').textContent = (Math.random() * 0.3).toFixed(3);
    document.getElementById('priceCorr').textContent = stock.correlation.toFixed(3);
    
    // Sentiment gauge
    const gaugeData = [{
        type: 'indicator',
        mode: 'gauge+number',
        value: (stock.sentiment + 1) * 50,
        gauge: {
            axis: { range: [0, 100] },
            bar: { color: stock.sentiment > 0.2 ? '#00C853' : stock.sentiment < -0.2 ? '#D32F2F' : '#FFA726' },
            steps: [
                { range: [0, 30], color: '#FFCDD2' },
                { range: [30, 70], color: '#FFE0B2' },
                { range: [70, 100], color: '#C8E6C9' }
            ]
        }
    }];
    
    const gaugeLayout = {
        paper_bgcolor: '#1A1A1A',
        font: { color: '#FFFFFF' },
        height: 300
    };
    
    Plotly.newPlot('sentimentGauge', gaugeData, gaugeLayout, {responsive: true});
    
    // Generate mock time series data
    const timestamps = [];
    const prices = [];
    const sentiments = [];
    const now = new Date();
    
    for (let i = 168; i >= 0; i--) {
        timestamps.push(new Date(now.getTime() - i * 3600000));
        prices.push(stock.price * (1 + (Math.random() - 0.5) * 0.05));
        sentiments.push(stock.sentiment + (Math.random() - 0.5) * 0.4);
    }
    
    // Sentiment vs Price chart
    const sentimentPriceData = [
        {
            x: timestamps,
            y: prices,
            type: 'scatter',
            name: 'Price',
            yaxis: 'y',
            line: { color: '#1976D2' }
        },
        {
            x: timestamps,
            y: sentiments,
            type: 'scatter',
            name: 'Sentiment',
            yaxis: 'y2',
            line: { color: '#00C853' }
        }
    ];
    
    const sentimentPriceLayout = {
        title: ticker + ' - Sentiment vs Price',
        paper_bgcolor: '#1A1A1A',
        plot_bgcolor: '#0A0A0A',
        font: { color: '#FFFFFF' },
        xaxis: { gridcolor: '#333333' },
        yaxis: { title: 'Price ($)', gridcolor: '#333333' },
        yaxis2: { title: 'Sentiment', overlaying: 'y', side: 'right', gridcolor: '#333333' },
        height: 400
    };
    
    Plotly.newPlot('sentimentPriceChart', sentimentPriceData, sentimentPriceLayout, {responsive: true});
}

// Update correlation table
function updateCorrelationTable() {
    const table = document.getElementById('correlationTable');
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Avg Sentiment</th>
                    <th>Price Correlation</th>
                    <th>Leading Correlation</th>
                    <th>Sentiment Volatility</th>
                    <th>Significant</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    selectedStocks.forEach(ticker => {
        const stock = mockStockData[ticker];
        const significant = Math.random() > 0.3;
        html += `
            <tr>
                <td><strong>${ticker}</strong></td>
                <td>${stock.sentiment.toFixed(3)}</td>
                <td>${stock.correlation.toFixed(3)}</td>
                <td>${(stock.correlation * 0.9).toFixed(3)}</td>
                <td>${(Math.random() * 0.3).toFixed(3)}</td>
                <td>${significant ? '✅' : '❌'}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    table.innerHTML = html;
}

// Update mentions
function updateMentions() {
    const ticker = document.getElementById('mentionStockSelector').value;
    
    const positiveMentions = [
        { source: 'Twitter', time: '2 hours ago', score: 0.856, text: `$${ticker} looking strong! 🚀 Great earnings report.` },
        { source: 'Reddit', time: '3 hours ago', score: 0.782, text: `Bullish on $${ticker}. This is my top pick for 2024.` },
        { source: 'News', time: '5 hours ago', score: 0.721, text: `${mockStockData[ticker].name} announces new product line.` }
    ];
    
    const negativeMentions = [
        { source: 'Twitter', time: '1 hour ago', score: -0.654, text: `$${ticker} overvalued at current levels IMO.` },
        { source: 'Reddit', time: '4 hours ago', score: -0.587, text: `Bearish on $${ticker}. Selling my position.` },
        { source: 'News', time: '6 hours ago', score: -0.523, text: `Analysts express concerns about ${mockStockData[ticker].name}.` }
    ];
    
    let positiveHTML = '';
    positiveMentions.forEach(mention => {
        positiveHTML += `
            <div class="mention-card positive">
                <div class="mention-header">
                    <strong>${mention.source}</strong>
                    <span>${mention.time}</span>
                </div>
                <div class="mention-score positive">Score: ${mention.score.toFixed(3)}</div>
                <div class="mention-text">"${mention.text}"</div>
            </div>
        `;
    });
    
    let negativeHTML = '';
    negativeMentions.forEach(mention => {
        negativeHTML += `
            <div class="mention-card negative">
                <div class="mention-header">
                    <strong>${mention.source}</strong>
                    <span>${mention.time}</span>
                </div>
                <div class="mention-score negative">Score: ${mention.score.toFixed(3)}</div>
                <div class="mention-text">"${mention.text}"</div>
            </div>
        `;
    });
    
    document.getElementById('positiveMentions').innerHTML = positiveHTML;
    document.getElementById('negativeMentions').innerHTML = negativeHTML;
}

// Update last update time
function updateLastUpdate() {
    const now = new Date();
    document.getElementById('lastUpdate').textContent = now.toLocaleString();
}

// Update all charts
function updateCharts() {
    updateOverviewCharts();
}