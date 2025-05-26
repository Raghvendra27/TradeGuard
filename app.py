# app.py
import datetime
import streamlit as st
import streamlit as st
import requests

@st.cache_data(ttl=300)
def fetch_live_rates():
    # Your API call logic
    url = f"https://open.er-api.com/v6/latest/INR"
    response = requests.get(url)
    data = response.json()
    return data

@st.cache_data(ttl=300)
def fetch_gold_prices():
    # gold price API logic
    ...

@st.cache_data(ttl=300)
def fetch_crude_prices():
    ...


# Page setup
st.set_page_config(page_title="TradeGuard - SME Export Risk Monitor", layout="wide")

# Sidebar navigation
st.sidebar.title("🔍 TradeGuard Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Trade Alerts", "SME Risk Score"])

# Dashboard page
# Dashboard page
if page == "Dashboard":
    from utils.news_fetcher import get_newsapi_articles
    news_items = get_newsapi_articles()
   
    import requests
    import plotly.graph_objs as go
    import pandas as pd

    st.title("📊 Export Risk Dashboard")
    st.markdown("### Real-time Global Trade Insights for Indian SMEs")

    # === 🌐 LIVE DATA SECTION (Forex, Crude, Gold) ===
    st.subheader("📈 Market Indicators")

    col1, col2, col3 = st.columns(3)

    def fetch_live_data():
        headers = {"X-API-KEY": "DFizFdNE0lNhaq2T2CGimNjPSyr6JEHS"}  # Replace with your actual API key
        try:
            fx = requests.get("https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols=INR", headers=headers).json()
            usd_inr = fx["rates"]["INR"]

            gold = requests.get("https://api.metalpriceapi.com/v1/latest?base=USD&symbols=XAU", headers={"apikey": "4178c11dadade33e10b3647114c26078"}).json()
            gold_price = gold["rates"]["XAU"]

            crude = requests.get("https://api.api-ninjas.com/v1/commodities?name=crude oil", headers={"X-Api-Key": "hEIYlxl/kxtFk+a2qv/stg==tG5uQw3imTpSixce"}).json()
            crude_price = crude[0]["price"]

            return usd_inr, gold_price, crude_price
        except:
            return 83.0, 2350.0, 90.0  # fallback values

    usd_inr, gold_price, crude_price = fetch_live_data()

    col1.metric("💱 USD/INR", f"{usd_inr:.2f}")
    col2.metric("🪙 Gold (USD/Oz)", f"{gold_price:.2f}")
    col3.metric("🛢 Crude Oil (USD/barrel)", f"{crude_price:.2f}")

    st.markdown("---")

    # === 📦 SECTOR RISK CHART ===
    st.subheader("📌 Top Export Sectors vs Risk Exposure")
    sectors = ['Textiles', 'Pharma', 'Automobile', 'Electronics', 'Agriculture']
    risk_scores = [70, 55, 85, 60, 40]

    sector_chart = go.Figure(
        data=[go.Bar(x=sectors, y=risk_scores, marker_color='indianred')],
        layout=go.Layout(
            template='plotly_dark',
            title='Sectoral Risk Scores (Higher is Riskier)',
            yaxis=dict(title='Risk Score (out of 100)')
        )
    )
    st.plotly_chart(sector_chart, use_container_width=True)

    # === 🌍 COUNTRY RISK CHART ===
    st.subheader("🌍 Trade Partner Country Risk")
    countries = ['USA', 'China', 'Germany', 'UAE', 'UK']
    country_risks = [65, 75, 50, 45, 55]

    country_chart = go.Figure(
        data=[go.Bar(x=country_risks, y=countries, orientation='h', marker_color='darkorange')],
        layout=go.Layout(
            template='plotly_dark',
            title='Country Risk Exposure',
            xaxis=dict(title='Risk Score')
        )
    )
    st.plotly_chart(country_chart, use_container_width=True)

    # === 📈 EXPORT TREND (Static Sample) ===
    st.subheader("📊 India Export Trend YoY")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    export_vals = [31.5, 34.2, 32.8, 36.0, 35.5, 37.0]

    trend_chart = go.Figure(
        data=[go.Scatter(x=months, y=export_vals, mode='lines+markers', line=dict(color='cyan'))],
        layout=go.Layout(
            template='plotly_dark',
            title='India’s Monthly Export Value (in Billion USD)',
            yaxis=dict(title='Export Value (B USD)')
        )
    )
    st.plotly_chart(trend_chart, use_container_width=True)

    # === 🧠 TRADE SENTIMENT SCORE ===
    st.subheader("🧠 Trade Sentiment Index (Beta)")
    st.markdown("**Composite score based on news trends, market indicators, and sector analysis**")
    st.success("📊 Sentiment Score: 72.5 / 100 (Moderate Risk)")

    # === 📅 LAST UPDATED ===
    st.markdown(f"🔄 Last Updated: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

    st.markdown("---")


    if news_items:
        for item in news_items[:3]:  # show only 3 latest
            st.markdown(f"**🔗 [{item['title']}]({item['link']})**")
            st.markdown(f"*{item['summary']}*")
            st.markdown("---")
    else:
        st.warning("⚠️ Could not fetch live news at the moment.")

# Trade alerts page
elif page == "Trade Alerts":
    from utils.news_fetcher import get_newsapi_articles

    st.title("📰 Latest Trade Policy News")
    st.markdown("Stay updated on global trade regulations, tariff changes, and economic shifts affecting Indian SMEs.")

    news_items = get_newsapi_articles()

    if news_items:
        for item in news_items:
            st.markdown(f"### 🔗 [{item['title']}]({item['link']})")
            st.markdown(f"*{item['summary']}*\n")
            st.markdown("---")
    else:
        st.warning("⚠️ Could not fetch live news at the moment. Here's some recent static news instead.")
        st.markdown("### 🔗 [India to Respond to US Tariff Hike on Steel Products](https://www.example.com)")
        st.markdown("*Government exploring alternate markets for Indian steel exporters.*")
        st.markdown("---")

# Risk score page
elif page == "SME Risk Score":
    st.title("📉 Calculate Your Export Risk Score")
    st.markdown("Use this tool to assess the trade risk for a particular product in a specific country.")

    st.markdown("---")
    st.markdown("## 🧮 Trade Risk Calculator")

    with st.form("risk_form"):
        country = st.selectbox("🌍 Export Destination", ["USA", "China", "Germany", "Russia", "Iran", "Sri Lanka", "Nepal"])
        product = st.selectbox("📦 Product Category", ["Pharmaceuticals", "Electronics", "Agriculture", "Textiles", "Defense Equipment", "Software Services"])
        size = st.selectbox("🏢 Business Size", ["Small", "Medium", "Large"])
        
        submitted = st.form_submit_button("Calculate Risk")

    if submitted:
        # Simple risk calculation logic
        base_risk = 50
        risky_countries = {"Russia": 30, "Iran": 40, "Sri Lanka": 20}
        base_risk += risky_countries.get(country, -10)

        if product == "Defense Equipment":
            base_risk += 25
        elif product == "Agriculture":
            base_risk += 5
        elif product == "Software Services":
            base_risk -= 10

        if size == "Small":
            base_risk += 10
        elif size == "Large":
            base_risk -= 5

        risk_score = max(0, min(100, base_risk))

        if risk_score < 40:
            risk_level = "🟢 Low"
        elif risk_score < 70:
            risk_level = "🟠 Medium"
        else:
            risk_level = "🔴 High"

        if risk_score > 75:
            recommendation = "⚠️ High risk detected. Explore alternative markets or delay exports."
        elif risk_score > 50:
            recommendation = "Proceed with caution. Monitor policy and geopolitical developments closely."
        else:
            recommendation = "✔️ Good to go! Minimal risk at present."

        # Output
        st.metric("Risk Score", risk_score)
        st.markdown(f"**Risk Level:** {risk_level}")
        st.info(recommendation)

# Footer
st.markdown("---")
st.markdown("🔐 Built with ❤️ for Indian SMEs | [GitHub](#) | [LinkedIn](#)")
