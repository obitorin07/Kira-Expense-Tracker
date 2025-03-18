import streamlit as st
import mysql.connector
import pandas as pd
import datetime
import os
from dotenv import dotenv_values
from decimal import Decimal

# Load environment variables
cre = dotenv_values(r"credentials.env")

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host=cre['host'],
        database=cre['database'],
        user=cre['user'],
        password=cre['password']
    )

# Reset budget on the given date every month
def reset_budget():
    conn = get_db_connection()
    cursor = conn.cursor()
    current_month = datetime.date.today().strftime("%Y-%m")
    today_day = datetime.date.today().day

    if today_day == 16:  # Reset budget only on the given date
        cursor.execute(
            "INSERT INTO budget (month_year, total_budget) VALUES (%s, %s) ON DUPLICATE KEY UPDATE total_budget = 10000",
            (current_month, 10000)
        )
        conn.commit()
    
    conn.close()

# Get current month's budget
def get_budget():
    conn = get_db_connection()
    cursor = conn.cursor()
    current_month = datetime.date.today().strftime("%Y-%m")
    cursor.execute("SELECT total_budget FROM budget WHERE month_year = %s", (current_month,))
    budget = cursor.fetchone()
    conn.close()
    return Decimal(budget[0]) if budget else Decimal(10000)

# Add expense to the database
def add_expense(date_time, category, amount, description, payment_method):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (date_time, category, amount, description, payment_method) VALUES (%s, %s, %s, %s, %s)",
        (date_time, category, amount, description, payment_method)
    )
    conn.commit()
    conn.close()

# Fetch last 2 expenses
def get_expenses():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM expenses ORDER BY date_time DESC LIMIT 2", conn)
    conn.close()
    return df

# Function to update the budget
def update_budget(new_budget):
    conn = get_db_connection()
    cursor = conn.cursor()
    current_month = datetime.date.today().strftime("%Y-%m")
    cursor.execute(
        "INSERT INTO budget (month_year, total_budget) VALUES (%s, %s) ON DUPLICATE KEY UPDATE total_budget = %s",
        (current_month, new_budget, new_budget)
    )
    conn.commit()
    conn.close()

# Main Streamlit UI
st.set_page_config(page_title="Expense Tracker", page_icon="kira_logo.png")
st.image("lone_warrior.jpg", use_container_width=True)
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Expense Tracker</h2>", unsafe_allow_html=True)

reset_budget()  # Automatically reset budget given date of the month

# Display current date and budget in a single line
current_date = datetime.date.today()
current_day = current_date.strftime("%A")
monthly_budget = get_budget()

st.markdown(f"<h4 style='text-align: center;'>📅 {current_day}, {current_date} &nbsp;&nbsp;&nbsp; Budget: ₹{monthly_budget}</h4>", unsafe_allow_html=True)

# Calculate spending
expenses = get_expenses()
total_spent = round(expenses["amount"].sum(), 2) if not expenses.empty else 0.00
remaining_budget = round(float(monthly_budget) - total_spent, 2)  # Ensure both are float for subtraction

# Display budget summary with proper alignment
st.markdown("<h4 style='text-align: center;'>Budget Summary</h4>", unsafe_allow_html=True)
if remaining_budget >= 0:
    st.markdown(f"<h4 style='text-align: center;'>Total Spent: ₹{total_spent} &nbsp;&nbsp;&nbsp; Remaining: ₹{remaining_budget}</h4>", unsafe_allow_html=True)
else:
    st.markdown(f"<h4 style='text-align: center;'>Total Spent: ₹{total_spent} &nbsp;&nbsp;&nbsp; <span style='color: red;'>Remaining: ₹{remaining_budget}</span></h4>", unsafe_allow_html=True)

# Add new expense
st.subheader("➕ Add an Expense")
date_time = st.date_input("Date:", current_date)

# ✅ FIX: Default to current time but allow selecting past time without resetting
if "selected_time" not in st.session_state:
    st.session_state["selected_time"] = datetime.datetime.now().time()  # Default to current time

selected_time = st.time_input("Time:", st.session_state["selected_time"])
st.session_state["selected_time"] = selected_time  # Store selected time

category = st.selectbox("Category:", ["Rent & PG", "Food & Groceries", "Transport", "Utilities & Bills", "Shopping", "Entertainment", "Health & Medical", "Education & Learning", "Miscellaneous", "Savings & Investments"])
amount = st.number_input("Amount:", min_value=0.01, format="%.2f")
description = st.text_area("Description:")
payment_method = st.selectbox("Payment Method:", ["UPI", "Cash", "Others"])

if st.button("Add Expense"):
    full_datetime = datetime.datetime.combine(date_time, selected_time)
    add_expense(full_datetime, category, amount, description, payment_method)
    st.success(f"Expense of ₹{amount} added successfully!")
    st.rerun()

# Display last 2 expenses
st.subheader("📜 Expense History (Last 2 Transactions)")
if not expenses.empty:
    for index, row in expenses.iterrows():
        col1, col2, col3 = st.columns([3, 3, 3])
        col1.write(row['date_time'])
        col2.write(row['category'])
        col3.write(f"₹{row['amount']}")
else:
    st.write("No expenses recorded yet!")

# Update budget section
st.subheader("💰 Update Budget")
new_budget = st.number_input("Enter New Budget Amount:", min_value=0.01, format="%.2f")

if st.button("Update Budget"):
    if new_budget > 0:
        update_budget(new_budget)
        st.success(f"Budget updated to ₹{new_budget}")
    else:
        st.error("Please enter a valid budget amount.")
