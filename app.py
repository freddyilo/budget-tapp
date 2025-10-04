import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="💰 Budgeting App", layout="wide")

st.title("💰 All-in-One Budgeting App")
st.write("Track your income, expenses, and savings goals in one place.")

# --- INCOME ---
st.header("1️⃣ Income")
income = st.number_input("Enter your monthly income:", min_value=0.0, step=100.0)

# --- EXPENSES ---
st.header("2️⃣ Expenses")
st.write("Add your main expenses below:")

expense_categories = ["Rent", "Food", "Transport", "Entertainment", "Other"]
expenses = {}
for category in expense_categories:
    expenses[category] = st.number_input(f"{category}:", min_value=0.0, step=50.0)

# Convert to DataFrame
df_expenses = pd.DataFrame({
    "Category": list(expenses.keys()),
    "Amount": list(expenses.values())
})

total_expenses = df_expenses["Amount"].sum()
remaining_balance = income - total_expenses

# --- SAVINGS GOAL ---
st.header("3️⃣ Savings Goal")
goal = st.number_input("Enter your savings goal:", min_value=0.0, step=100.0)

if goal > 0:
    progress = max(0, min(1, remaining_balance / goal))
    st.progress(progress)
    st.write(f"Remaining balance: **${remaining_balance:,.2f}**")
    st.write(f"Goal progress: **{progress*100:.1f}%**")
else:
    st.write(f"Remaining balance: **${remaining_balance:,.2f}**")

# --- CHART ---
st.header("📊 Expense Breakdown")
if total_expenses > 0:
    fig = px.pie(df_expenses, names="Category", values="Amount", title="Expenses by Category")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No expenses added yet.")

# --- SUMMARY ---
st.header("📌 Summary")
st.metric("Total Income", f"${income:,.2f}")
st.metric("Total Expenses", f"${total_expenses:,.2f}")
st.metric("Remaining Balance", f"${remaining_balance:,.2f}")
