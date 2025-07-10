import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
from datetime import datetime

st.set_page_config(
       page_title = "CAPM",
       page_icon = ":chart_with_upwards_trend:",
       layout = "wide"
)

st.title("CAPM - Capital Asset Pricing Model")

#Getting input for stock list and year

col1,col2 = st.columns([1,1])

with col1:
    stocks_list = st.multiselect("Choose 5 Stocks",
                   options=["AAPL", "MSFT", "GOOGL", "AMZN","TSLA","NVDA","META"])
with col2:
    Year = st.number_input("Number of Years", min_value=1, max_value=10, value=5 )

#download data from yfinance

start = datetime(2020, 1, 1)
end = datetime(2025, 1, 1)
SP500 = yf.download("SPY", start, end)
print(SP500.tail())

stocks_df = pd.DataFrame()

for stock in stocks_list:
    data = yf.download(stock, period = f'{Year}y')
    stocks_df[f'{stock}'] = data['Close']
    
    data['Return'] = data['Adj Close'].pct_change()
    SP500['Return'] = SP500['Adj Close'].pct_change()
    
    # Merge the stock data with SP500 data
    merged_data = pd.merge(data[['Return']], SP500[['Return']], left_index=True, right_index=True, suffixes=('', '_SP500'))
    
    # Calculate beta
    covariance = merged_data.cov().iloc[0, 1]
    variance = merged_data['Return_SP500'].var()
    beta = covariance / variance
    
    st.write(f"Beta for {stock}: {beta:.2f}")