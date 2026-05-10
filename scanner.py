import yfinance as yf
import pandas as pd
import pandas_ta as ta  # Technical Analysis library

TICKERS = ["POET", "CRDO", "NVDA", "MRVL", "AMD", "TSLA"]
VOL_THRESHOLD = 50000
GAP_THRESHOLD = 3.0 # 3% Gap

def scan_for_trading():
    for symbol in TICKERS:
        ticker = yf.Ticker(symbol)
        # Fetch 60 days of data for reliable Moving Averages
        df = ticker.history(period="60d", interval="1d")
        
        if len(df) < 20: continue

        # 1. Calculate Technical Indicators
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        # 2. Check Pre-market Data
        # Get latest 1-min data (includes pre-market)
        intraday = ticker.history(period="1d", interval="1m", prepost=True)
        if intraday.empty: continue
        
        current_price = intraday['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-1]
        current_vol = intraday['Volume'].sum()
        gap_pct = ((current_price - prev_close) / prev_close) * 100
        
        # 3. Strategy Logic (The "Buy Signal")
        is_above_sma = current_price > df['SMA_20'].iloc[-1]
        is_not_overbought = df['RSI'].iloc[-1] < 70
        
        if gap_pct > GAP_THRESHOLD and current_vol > VOL_THRESHOLD:
            print(f"\n🎯 SIGNAL FOUND: {symbol}")
            print(f"Gap: {gap_pct:.2f}% | Vol: {current_vol} | RSI: {df['RSI'].iloc[-1]:.1f}")
            
            if is_above_sma and is_not_overbought:
                print("✅ STATUS: Bullish Trend (Above 20-SMA) & Room to Run.")
            else:
                print("⚠️ WARNING: Stock is in a downtrend or currently overbought.")
            
            # Fetch News headlines
            news = ticker.news[:2]
            for n in news:
                print(f"  - News: {n.get('title')}")

if __name__ == "__main__":
    scan_for_trading()