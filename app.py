import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.markdown("""
<style>
/* Page background */
.main {
    background-color: #0f172a;
}

/* Text colors */
h1, h2, h3 {
    color: #e5e7eb;
}

/* Inputs */
.stTextInput > div > div > input,
.stDateInput > div > div > input {
    background-color: #020617;
    color: white;
}

/* GLOW BUTTON STYLE */
.stButton > button {
    width: 100%;
    height: 50px;
    border: none;
    outline: none;
    color: #fff;
    background: #111;
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 14px;
    font-size: 18px;
    font-weight: 600;
}

.stButton > button:before {
    content: '';
    background: linear-gradient(
        45deg,
        #00ffd5,
        #00b7ff,
        #7a00ff,
        #ff00c8,
        #ff0000,
        #ff7300,
        #fffb00,
        #48ff00
    );
    position: absolute;
    top: -2px;
    left: -2px;
    background-size: 400%;
    z-index: -1;
    filter: blur(5px);
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    animation: glowing 20s linear infinite;
    border-radius: 14px;
}

.stButton > button:after {
    z-index: -1;
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: #111;
    left: 0;
    top: 0;
    border-radius: 14px;
}

@keyframes glowing {
    0% { background-position: 0 0; }
    50% { background-position: 400% 0; }
    100% { background-position: 0 0; }
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


st.title("📈 AI Stock Analyzer")
st.caption("Educational tool • Not financial advice")

ticker = st.text_input("Enter Stock Symbol", "AAPL")
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", pd.to_datetime("2019-01-01"))
end_date = col2.date_input("End Date", pd.to_datetime("today"))

# ----------------- Helpers -----------------

def classify_trend(df):
    recent = df["Close"].tail(10)
    if len(recent) < 2:
        return "Not enough data"
    change = float((recent.iloc[-1] - recent.iloc[0]) / recent.iloc[0] * 100)
    if change > 2:
        return "Uptrend 📈"
    elif change < -2:
        return "Downtrend 📉"
    else:
        return "Stable ➖"

def calculate_risk(df):
    returns = df["Close"].pct_change().dropna()
    if len(returns) == 0:
        return "Not enough data"
    vol = float(returns.std() * 100)
    if vol > 2:
        return "High Risk 🔴"
    elif vol > 1:
        return "Medium Risk 🟠"
    else:
        return "Low Risk 🟢"

def get_ai_insight(trend, risk):
    if "Uptrend" in trend and "Low" in risk:
        return "The stock shows a positive upward trend with relatively low volatility, indicating stable growth potential."
    elif "Uptrend" in trend and "High" in risk:
        return "The stock is trending upward but has high volatility, meaning potential gains come with increased risk."
    elif "Downtrend" in trend:
        return "The stock is currently in a downward trend, which may indicate weakening performance or market correction."
    else:
        return "The stock is showing stable movement without a strong upward or downward trend."

# ----------------- App Logic -----------------

if "data" not in st.session_state:
    st.session_state.data = None

b1, b2 = st.columns(2)

with b1:
    fetch = st.button("📥 Fetch Stock Data")
with b2:
    analyze = st.button("🔍 Analyze Stock")

if fetch:
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        st.error("No data found for this stock.")
    else:
        df.reset_index(inplace=True)
        st.session_state.data = df
        st.success("Stock data loaded successfully.")
        st.dataframe(df.tail())

if analyze:
    if st.session_state.data is None:
        st.warning("Please fetch stock data first.")
    else:
        df = st.session_state.data.copy()

        trend = classify_trend(df)
        risk = calculate_risk(df)
        insight = get_ai_insight(trend, risk)

        st.subheader("Trend Summary")
        st.write(trend)

        st.subheader("Risk Indicator")
        st.write(risk)

        st.subheader("📊 Intelligent Analysis")
        st.write(insight)

        st.subheader("Price Trend")
        st.line_chart(df.set_index("Date")["Close"])

        st.caption("⚠ This tool is for educational or college project use only.")

