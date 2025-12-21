import streamlit as st
import pandas as pd
import joblib
import yfinance as yf

st.set_page_config(page_title="Stock Price Prediction App", layout="centered")

st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
}
.main {
    background: transparent;
}
.glass-card {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 0 30px rgba(34, 197, 94, 0.3);
}
.title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: white;
}
.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 25px;
}
.stButton>button {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: black;
    font-size: 18px;
    border-radius: 12px;
    padding: 10px 0;
    width: 100%;
}
.footer {
    text-align: center;
    color: #9ca3af;
    margin-top: 20px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📈 Stock Price Prediction App</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered insights for smarter investing</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    ticker = st.text_input("Stock Ticker", "AAPL")
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Start Date", pd.to_datetime("2018-01-01"))
    with col2:
        end = st.date_input("End Date", pd.to_datetime("2025-01-01"))

    analyze = st.button("Analyze")

    st.markdown("</div>", unsafe_allow_html=True)

if analyze:
    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty or len(df) < 30:
            st.warning("Not enough data available for this stock.")
            st.stop()

        df.columns = df.columns.get_level_values(0)
        df.reset_index(inplace=True)

        df['Prev_Close'] = df['Close'].shift(1)
        df = df.dropna()

        features = ['Open', 'High', 'Low', 'Volume', 'Prev_Close']
        df[features] = df[features].apply(pd.to_numeric, errors='coerce')
        df = df.dropna()

        model = joblib.load("models/model.pkl")
        df['Predicted_Close'] = model.predict(df[features])

        st.subheader("📊 Last 10 Predictions")
        st.dataframe(df[['Date','Close','Predicted_Close']].tail(10))

        st.subheader("📈 Price Trend")
        st.line_chart(df.set_index("Date")[['Close','Predicted_Close']])

    except Exception:
        st.error("Unable to analyze this stock. Please try another ticker.")

st.markdown("<div class='footer'>⚠️ This is not financial advice</div>", unsafe_allow_html=True)
