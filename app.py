!pip install yfinance
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import yfinance as yf
import datetime

st.set_page_config(page_title="💰 Ultimate Financial Dashboard", layout="wide")

# HEADER & INTRO
st.image("https://cdn-icons-png.flaticon.com/512/2920/2920298.png", width=80)
st.title("💰 Ultimate Financial Dashboard")
st.write("""
Track your expenses, explore financial concepts, get real-time market, crypto, commodity, and economic data, and find top resources—all in one place.
""")

# SIDEBAR NAVIGATION
menu = st.sidebar.radio("📌 Navigation", [
    "Budget", "Markets", "Crypto", "Commodities", "Indices", "Economics", "Concepts", "Resources", "Money Flow", "Visualization"
])

# BUDGET TAB
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

# MARKETS TAB: STOCKS & CURRENCIES
elif menu == "Markets":
    st.header("📈 Stock Market & Currencies")
    symbol = st.text_input("Enter a stock symbol (e.g. AAPL, TSLA, MSFT):", "AAPL")
    if symbol:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1mo")
            price = ticker.info.get('regularMarketPrice', None)
            st.metric(f"{symbol} Current Price", f"${price:,.2f}" if price else "N/A")
            st.write(f"**{symbol} Last 1 Month Price Trend**")
            st.line_chart(hist['Close'])
            st.write("**Details:**")
            st.json({
                "Open": ticker.info.get('open'),
                "High": ticker.info.get('dayHigh'),
                "Low": ticker.info.get('dayLow'),
                "Previous Close": ticker.info.get('previousClose'),
                "Volume": ticker.info.get('volume'),
                "Market Cap": ticker.info.get('marketCap'),
            })
        except Exception as e:
            st.error(f"Could not fetch data for {symbol}: {e}")

    st.markdown("---")
    st.subheader("Major Currencies (USD Base)")
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        data = requests.get(url).json()
        st.metric("USD → EUR", f"{data['rates']['EUR']:.2f}")
        st.metric("USD → JPY", f"{data['rates']['JPY']:.2f}")
        st.metric("USD → GBP", f"{data['rates']['GBP']:.2f}")
        st.metric("USD → CAD", f"{data['rates']['CAD']:.2f}")
        st.metric("USD → AUD", f"{data['rates']['AUD']:.2f}")
    except Exception:
        st.warning("Could not fetch currency data.")

# CRYPTO TAB
elif menu == "Crypto":
    st.header("🪙 Cryptocurrency Prices")
    coins = ["bitcoin", "ethereum", "dogecoin", "solana", "cardano"]
    for coin in coins:
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            data = requests.get(url).json()
            price = data[coin]['usd']
            st.metric(f"{coin.capitalize()} (USD)", f"${price:,.2f}")
        except Exception:
            st.warning(f"Could not fetch {coin} price.")

# COMMODITIES TAB
elif menu == "Commodities":
    st.header("🛢️ Commodity Prices")
    commodities = {
        "Gold": "XAU",
        "Silver": "XAG",
        "Crude Oil": "WTI",
        "Platinum": "XPT",
        "Copper": "XCU"
    }
    # Metals-API or other commodity API needed for live prices (demo values shown)
    for name, code in commodities.items():
        st.metric(name, "Demo: $1800.00" if code == "XAU" else "Demo: $25.00")
    st.info("For live prices, sign up for a commodity API like Metals-API.")

# INDICES TAB
elif menu == "Indices":
    st.header("🌍 Major World Indices")
    indices = {
        "S&P 500": "^GSPC",
        "Dow Jones": "^DJI",
        "Nasdaq": "^IXIC",
        "FTSE 100": "^FTSE",
        "DAX": "^GDAXI",
        "Nikkei": "^N225"
    }
    for name, idx in indices.items():
        try:
            tick = yf.Ticker(idx)
            price = tick.info.get('regularMarketPrice', None)
            st.metric(f"{name}", f"{price:,.2f}" if price else "N/A")
        except Exception:
            st.warning(f"Could not fetch {name} data.")

# ECONOMIC INDICATORS TAB
elif menu == "Economics":
    st.header("📊 Economic Indicators")
    st.write("Live U.S. economic data (FRED API required for full access)")
    indicators = {
        "US Inflation Rate": "CPILFESL",
        "US Unemployment Rate": "UNRATE",
        "US GDP": "GDP"
    }
    fred_key = "YOUR_FRED_API_KEY"
    for name, series_id in indicators.items():
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={fred_key}&file_type=json"
            data = requests.get(url).json()
            latest = data["observations"][-1]
            st.metric(name, f"{latest['value']}")
        except Exception:
            st.info(f"Demo: Replace with your FRED API key for {name}.")

# CONCEPTS TAB
elif menu == "Concepts":
    st.header("📚 Financial Concepts & Calculators")
    concept = st.selectbox("Choose a concept:", [
        "Stocks", "Interest", "Compound Interest", "Inflation", "Budgeting", "Bond Yield", "Loan Payment"
    ])
    images = {
        "Stocks": "https://cdn-icons-png.flaticon.com/512/1424/1424453.png",
        "Interest": "https://cdn-icons-png.flaticon.com/512/2920/2920278.png",
        "Compound Interest": "https://cdn-icons-png.flaticon.com/512/2080/2080591.png",
        "Inflation": "https://cdn-icons-png.flaticon.com/512/1042/1042331.png",
        "Budgeting": "https://cdn-icons-png.flaticon.com/512/2920/2920298.png",
        "Bond Yield": "https://cdn-icons-png.flaticon.com/512/4139/4139981.png",
        "Loan Payment": "https://cdn-icons-png.flaticon.com/512/4139/4139989.png"
    }
    st.image(images[concept], width=60)
    explanations = {
        "Stocks": "**Stocks:** Shares in a company. Owners may benefit from growth or dividends.",
        "Interest": "**Interest:** The cost of borrowing money or the reward for saving.",
        "Compound Interest": "**Compound Interest:** Interest on your initial money *and* on the interest that accumulates.",
        "Inflation": "**Inflation:** The rate at which prices rise, reducing purchasing power.",
        "Budgeting": "**Budgeting:** Creating a plan for spending and saving money.",
        "Bond Yield": "**Bond Yield:** The return an investor gets on a bond, usually expressed as a percentage.",
        "Loan Payment": "**Loan Payment:** The regular payment required to pay off a loan over time."
    }
    st.write(explanations[concept])
    if concept == "Compound Interest":
        st.write("Try out the calculator:")
        principal = st.number_input("Principal ($)", 1000)
        rate = st.number_input("Annual Interest Rate (%)", 5.0) / 100
        years = st.number_input("Years", 10)
        freq = st.number_input("Times Compounded Per Year", 1)
        if st.button("Calculate"):
            amount = principal * (1 + rate / freq) ** (freq * years)
            st.success(f"Future Value: ${amount:,.2f}")
    elif concept == "Loan Payment":
        st.write("Try out the calculator:")
        loan = st.number_input("Loan Amount ($)", 10000)
        loan_rate = st.number_input("Annual Interest Rate (%)", 5.0) / 100
        months = st.number_input("Term (months)", 60)
        if st.button("Calculate Payment"):
            if loan_rate > 0:
                payment = loan * (loan_rate/12) / (1 - (1 + loan_rate/12) ** -months)
            else:
                payment = loan / months
            st.success(f"Monthly Payment: ${payment:,.2f}")

# RESOURCES TAB
elif menu == "Resources":
    st.header("🌐 Top Finance Websites & News")
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
            "name": "Bloomberg",
            "url": "https://www.bloomberg.com/",
            "logo": "https://assets.bwbx.io/business/public/images/favicon-32x32.png",
            "desc": "Latest news on markets, economies, and companies worldwide."
        },
        {
            "name": "Khan Academy Finance",
            "url": "https://www.khanacademy.org/economics-finance-domain/core-finance",
            "logo": "https://cdn.kastatic.org/images/favicon.ico",
            "desc": "Free, clear lessons on finance, economics, and investing."
        },
        {
            "name": "Federal Reserve Education",
            "url": "https://www.federalreserveeducation.org/",
            "logo": "https://www.federalreserveeducation.org/favicon.ico",
            "desc": "U.S. central bank education site on money, banking, and economics."
        },
        {
            "name": "World Bank",
            "url": "https://www.worldbank.org/",
            "logo": "https://www.worldbank.org/etc/designs/wb/images/favicon.ico",
            "desc": "Global economic data, research, and country profiles."
        },
    ]
    for site in resources:
        cols = st.columns([1, 5])
        with cols[0]:
            st.image(site["logo"], width=40)
        with cols[1]:
            st.markdown(f"**[{site['name']}]({site['url']})**")
            st.write(site["desc"])

# MONEY FLOW TAB
elif menu == "Money Flow":
    st.header("🔄 Money Flow Visualization")
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=60)
    st.write("See how your money moves from income to expenses, savings, and investments.")
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

# VISUALIZATION TAB
elif menu == "Visualization":
    st.header("📊 Financial Charts & Analysis")
    st.write("Visualize your spending, net worth, or investment growth.")
    # Example: Spending over time
    spending = st.file_uploader("Upload your spending CSV (Date,Amount,Category)", type=["csv"])
    if spending:
        df = pd.read_csv(spending, parse_dates=['Date'])
        st.line_chart(df.groupby('Date')['Amount'].sum())
        st.bar_chart(df.groupby('Category')['Amount'].sum())
