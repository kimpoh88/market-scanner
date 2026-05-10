import yfinance as yf
import pandas as pd

# Define your tickers (e.g., tech-heavy for pre-market action)
TICKERS = ["AAPL", "TSLA", "NVDA", "AMD", "MSFT", "AMZN", "GOOGL", "META"] 
VOLUME_THRESHOLD = 50000  # Minimum shares traded pre-market
CHANGE_THRESHOLD = 1.5    # Minimum % change to trigger news fetch

def scan_market():
    print(f"Scanning {len(TICKERS)} tickers...")
    
    for symbol in TICKERS:
        ticker = yf.Ticker(symbol)
        
        # Get the most recent 1-minute data for the pre-market session
        data = ticker.history(period="1d", interval="1m", prepost=True)
        
        if data.empty:
            continue

        # Calculate metrics
        latest_price = data['Close'].iloc[-1]
        prev_close = ticker.info.get('previousClose', latest_price)
        pct_change = ((latest_price - prev_close) / prev_close) * 100
        current_volume = data['Volume'].sum() # Total pre-market volume so far

        # Filter: Volume threshold and significant price move
        if current_volume > VOLUME_THRESHOLD and abs(pct_change) > CHANGE_THRESHOLD:
            print(f"\n🚀 {symbol} | Price: ${latest_price:.2f} | Change: {pct_change:.2f}% | Vol: {current_volume}")
            
            # Fetch Related News
            news = ticker.news[:3] # Get top 3 headlines
            for item in news:
                title = item.get('title') or item.get('content', {}).get('title')
                link = item.get('link') or item.get('content', {}).get('pubDate') # Simplification for display
                print(f"  - NEWS: {title}")

if __name__ == "__main__":
    scan_market()