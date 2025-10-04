# app.py
import streamlit as st

st.title("💰 My Budgeting App")
st.write("Welcome! This is a simple Streamlit budgeting app.")

# Example input
income = st.number_input("Enter your income", min_value=0.0, step=100.0)
expense = st.number_input("Enter your expenses", min_value=0.0, step=100.0)

# Calculation
balance = income - expense
st.metric("Remaining Balance", f"${balance:,.2f}")
