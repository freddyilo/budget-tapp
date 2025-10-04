import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="💰 Financial Explorer", layout="wide")

# -- HEADER & INTRODUCTION --
st.image("https://cdn-icons-png.flaticon.com/512/2920/2920298.png", width=80)
st.title("💰 Financial Explorer")
st.write("""
Welcome! Track your expenses, explore financial concepts, get real market data, and discover top financial resources—all in one place.
""")

# --- SIDEBAR NAVIGATION ---
menu = st.sidebar.radio("📌 Navigation", ["Budget", "Markets", "Concepts", "Resources", "Money Flow"])

# --- BUDGET TAB ---
if menu == "Budget":
    st.header("💵 Budget Planner")
    st.image("https://cdn-icons-png.flaticon.com/512/1042/1042331.png", width=60)
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Monthly income:", min_value=0.0, step=100.0)
    with col2:
        st.write("### Expenses")
        expense_categories = ["Rent", "Food", "Transport", "Entertainment", "Other"]
        expenses = {cat: st.number_input(f"{cat}:", min_value=0.0, step=50.0) for cat in expense_categories}
    df_expenses = pd.DataFrame({"Category": list(expenses.keys()), "Amount": list(expenses.values())})
    total_expenses = df_expenses["Amount"].sum()
    remaining_balance = income - total_expenses
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"${income:,.2f}")
    col2.metric("Expenses", f"${total_expenses:,.2f}")
    col3.metric("Remaining", f"${remaining_balance:,.2f}")
    if total_expenses > 0:
        fig = px.pie(df_expenses, names="Category", values="Amount", title="Expense Breakdown")
        st.plotly_chart(fig, use_container_width=True)

# --- MARKETS TAB: REAL FINANCIAL DATA ---
elif menu == "Markets":
    st.header("📈 Real Market Data")
    st.image("https://cdn-icons-png.flaticon.com/512/190/190411.png", width=60)
    tabs = st.tabs(["Stocks", "Currencies", "Interest Rates"])

if menu == "Markets":
    st.header("📈 Real Market Data")
    st.image("https://cdn-icons-png.flaticon.com/512/190/190411.png", width=60)
    st.subheader("Live Stock Quotes")
    st.write("Get real-time prices for any stock. Example: AAPL, TSLA, AMZN.")
    symbol = st.text_input("Stock Symbol:", "AAPL")
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # Replace with your actual key
    if symbol:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                price = float(data['Global Quote']['05. price'])
                st.metric(f"{symbol} Price", f"${price:,.2f}")
            else:
                st.warning(f"No data found for {symbol}. Try another symbol.")
        except Exception as e:
            st.error("Error fetching stock data. Please check your API key and symbol.")
   
    # -- Stocks --
    with tabs[0]:
        st.subheader("Stocks (Demo: Apple, Google)")
        api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
        symbols = {"Apple": "AAPL", "Google": "GOOGL"}
        for name, symbol in symbols.items():
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
            try:
                data = requests.get(url).json()
                price = float(data['Global Quote']['05. price'])
                st.metric(f"{name} ({symbol})", f"${price:.2f}")
            except Exception:
                st.warning(f"Could not fetch {name} stock data.")
    
    # -- Currencies --
    with tabs[1]:
        st.subheader("Currency Exchange Rates (USD base)")
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            data = requests.get(url).json()
            st.metric("USD → EUR", f"{data['rates']['EUR']:.2f}")
            st.metric("USD → JPY", f"{data['rates']['JPY']:.2f}")
        except Exception:
            st.warning("Could not fetch currency data.")

    # -- Interest Rates --
    with tabs[2]:
        st.subheader("Interest Rates (Demo: US Fed Funds Rate)")
        # FRED API example (replace with your API key)
        try:
            fred_key = "YOUR_FRED_API_KEY"
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key={fred_key}&file_type=json"
            data = requests.get(url).json()
            latest = data["observations"][-1]
            st.metric("US Fed Funds Rate", f"{latest['value']}%")
        except Exception:
            st.warning("Could not fetch interest rate data.")

# --- CONCEPTS TAB ---
elif menu == "Concepts":
    st.header("📚 Financial Concepts")
    concept = st.selectbox("Choose a concept:", [
        "Stocks", "Interest", "Compound Interest", "Inflation", "Budgeting"
    ])
    images = {
        "Stocks": "https://cdn-icons-png.flaticon.com/512/1424/1424453.png",
        "Interest": "https://cdn-icons-png.flaticon.com/512/2920/2920278.png",
        "Compound Interest": "https://cdn-icons-png.flaticon.com/512/2080/2080591.png",
        "Inflation": "https://cdn-icons-png.flaticon.com/512/1042/1042331.png",
        "Budgeting": "https://cdn-icons-png.flaticon.com/512/2920/2920298.png"
    }
    st.image(images[concept], width=60)
    explanations = {
        "Stocks": "**Stocks:** Shares in a company. Owners may benefit from growth or dividends.",
        "Interest": "**Interest:** The cost of borrowing money or the reward for saving.",
        "Compound Interest": "**Compound Interest:** Interest on your initial money *and* on the interest that accumulates.",
        "Inflation": "**Inflation:** The rate at which prices rise, reducing purchasing power.",
        "Budgeting": "**Budgeting:** Creating a plan for spending and saving money."
    }
    st.write(explanations[concept])

# --- RESOURCES TAB ---
elif menu == "Resources":
    st.header("🌐 Helpful Finance Websites")
    resources = [
        {
            "name": "Investopedia",
            "url": "https://www.investopedia.com/",
            "logo": "https://www.investopedia.com/favicon.ico",
            "desc": "Comprehensive guides and articles on investing, markets, and personal finance."
        },
        {
            "name": "NerdWallet",
            "url": "https://www.nerdwallet.com/",
            "logo": "https://www.nerdwallet.com/favicon.ico",
            "desc": "Compare financial products, credit cards, and get money advice."
        },
        {
            "name": "Yahoo Finance",
            "url": "https://finance.yahoo.com/",
            "logo": "https://s.yimg.com/cv/apiv2/favicon/favicon.ico",
            "desc": "Market news, stock quotes, and portfolio management."
        },
        {
            "name": "The Balance",
            "url": "https://www.thebalance.com/",
            "logo": "https://www.thebalance.com/favicon.ico",
            "desc": "Clear explanations of banking, investing, and economic concepts."
        }
    ]
    for site in resources:
        cols = st.columns([1, 5])
        with cols[0]:
            st.image(site["logo"], width=40)
        with cols[1]:
            st.markdown(f"**[{site['name']}]({site['url']})**")
            st.write(site["desc"])

# --- MONEY FLOW TAB ---
elif menu == "Money Flow":
    st.header("🔄 Money Flow Visualization")
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=60)
    st.write("See how your money moves from income to expenses, savings, and investments.")
    # Demo Sankey chart
    import plotly.graph_objects as go
    labels = ["Income", "Rent", "Food", "Transport", "Entertainment", "Savings"]
    source = [0, 0, 0, 0, 0]
    target = [1, 2, 3, 4, 5]
    values = [500, 300, 150, 100, 200]
    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels),
        link=dict(source=source, target=target, value=values)
    )])
    st.plotly_chart(fig, use_container_width=True)

