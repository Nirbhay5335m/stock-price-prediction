import streamlit as st
import pandas as pd
import joblib
import yfinance as yf

st.set_page_config(page_title="Stock Price Prediction", layout="centered")
st.title("📈 Stock Price Prediction App")

ticker = st.text_input("Stock Ticker", "AAPL")
start = st.date_input("Start Date", pd.to_datetime("2018-01-01"))
end = st.date_input("End Date", pd.to_datetime("2025-01-01"))

if st.button("Analyze"):
    df = yf.download(ticker, start=start, end=end)
    df.columns = df.columns.get_level_values(0)
    df.reset_index(inplace=True)

    df['Prev_Close'] = df['Close'].shift(1)
    df = df.dropna()

    model = joblib.load("models/model.pkl")

    X = df[['Open','High','Low','Volume','Prev_Close']]
    df['Predicted_Close'] = model.predict(X)

    st.subheader("Last 10 Predictions")
    st.dataframe(df[['Date','Close','Predicted_Close']].tail(10))

    st.subheader("Price Trend")
    st.line_chart(df.set_index("Date")[['Close','Predicted_Close']])
