import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="💰 All-in-One Budgeting App", layout="wide")

st.title("💰 All-in-One Budgeting Dashboard")
st.write("Track your income, expenses, and stay updated with financial insights.")

# Sidebar navigation
menu = st.sidebar.radio("📌 Navigation", ["Budget", "Savings Goal", "Insights", "Summary"])

# --- INCOME & EXPENSES ---
if menu == "Budget":
    st.header("💵 Budget Planner")

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input("Enter your monthly income:", min_value=0.0, step=100.0)

    with col2:
        st.write("### Expenses")
        expense_categories = ["Rent", "Food", "Transport", "Entertainment", "Other"]
        expenses = {}
        for category in expense_categories:
            expenses[category] = st.number_input(f"{category}:", min_value=0.0, step=50.0)

    # DataFrame of expenses
    df_expenses = pd.DataFrame({
        "Category": list(expenses.keys()),
        "Amount": list(expenses.values())
    })

    total_expenses = df_expenses["Amount"].sum()
    remaining_balance = income - total_expenses

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"${income:,.2f}")
    col2.metric("Expenses", f"${total_expenses:,.2f}")
    col3.metric("Remaining", f"${remaining_balance:,.2f}")

    # Chart
    if total_expenses > 0:
        fig = px.pie(df_expenses, names="Category", values="Amount", title="Expense Breakdown")
        st.plotly_chart(fig, use_container_width=True)

# --- SAVINGS GOAL ---
elif menu == "Savings Goal":
    st.header("🎯 Savings Goal Tracker")

    goal = st.number_input("Enter your savings goal:", min_value=0.0, step=100.0)

    if goal > 0:
        progress = max(0, min(1, remaining_balance / goal))
        st.progress(progress)
        st.write(f"Remaining balance: **${remaining_balance:,.2f}**")
        st.write(f"Goal progress: **{progress*100:.1f}%**")
    else:
        st.write("Set a goal to start tracking progress!")

# --- FINANCIAL INSIGHTS ---
elif menu == "Insights":
    st.header("🌍 Global Financial Insights")

    # Example: Exchange rate (USD to EUR)
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()
        usd_to_eur = data["rates"]["EUR"]
        usd_to_jpy = data["rates"]["JPY"]

        st.subheader("💱 Currency Exchange Rates (Base: USD)")
        col1, col2 = st.columns(2)
        col1.metric("USD → EUR", f"{usd_to_eur:.2f}")
        col2.metric("USD → JPY", f"{usd_to_jpy:.2f}")

    except:
        st.error("⚠️ Could not fetch live exchange rates.")

    # Add space for global inflation or stock index
    st.subheader("📈 Stock Market Snapshot (Example)")
    st.write("Future expansion: add stock index or inflation API here.")

# --- SUMMARY ---
elif menu == "Summary":
    st.header("📊 Full Summary")
    st.write("This section will give an overview once more history tracking is added.")
