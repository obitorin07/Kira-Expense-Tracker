import streamlit as st
import mysql.connector
import pandas as pd
import datetime
import os
from dotenv import dotenv_values

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

    if today_day == 17:  # Reset budget only on the given date
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
    return budget[0] if budget else 10000

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

# Fetch all expenses (for budget calculation)
def get_all_expenses():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM expenses ORDER BY date_time DESC", conn)
    conn.close()
    return df

# Fetch last 2 expenses (for display only)
def get_last_2_expenses():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM expenses ORDER BY date_time DESC LIMIT 2", conn)
    conn.close()
    return df

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

# Get all expenses (for budget calculation)
expenses = get_all_expenses()

# Calculate total spending and remaining budget from all transactions
total_spent = round(expenses["amount"].sum(), 2) if not expenses.empty else 0.00
remaining_budget = round(monthly_budget - total_spent, 2)

# Display budget summary with proper alignment
st.markdown("<h4 style='text-align: center;'>Budget Summary</h4>", unsafe_allow_html=True)
if remaining_budget >= 0:
    st.markdown(f"<h4 style='text-align: center;'>Total Spent: ₹{total_spent} &nbsp;&nbsp;&nbsp; Remaining: ₹{remaining_budget}</h4>", unsafe_allow_html=True)
else:
    st.markdown(f"<h4 style='text-align: center;'>Total Spent: ₹{total_spent} &nbsp;&nbsp;&nbsp; <span style='color: red;'>Remaining: ₹{remaining_budget}</span></h4>", unsafe_allow_html=True)

# Add new expense
st.subheader("➕ Add an Expense")
# Check if the time is already in session_state, otherwise set default to current time
if 'time_selected' not in st.session_state:
    st.session_state['time_selected'] = datetime.datetime.now().time()

# Time input (allow past time or manual entry)
time = st.time_input("Time:", value=st.session_state['time_selected'])

# Store the selected time in session_state so it doesn't reset
st.session_state['time_selected'] = time

date_time = st.date_input("Date:", current_date)
category = st.selectbox("Category:", ["Rent & PG", "Food & Groceries", "Transport", "Utilities & Bills", "Shopping", "Entertainment", "Health & Medical", "Education & Learning", "Miscellaneous", "Savings & Investments"])
amount = st.number_input("Amount:", min_value=0.01, format="%.2f")
description = st.text_area("Description:")
payment_method = st.selectbox("Payment Method:", ["UPI", "Cash", "Others"])

if st.button("Add Expense"):
    full_datetime = datetime.datetime.combine(date_time, time)
    add_expense(full_datetime, category, amount, description, payment_method)
    st.success(f"Expense of ₹{amount} added successfully!")
    st.rerun()

# Fetch last 2 expenses (for display only)
last_2_expenses = get_last_2_expenses()

# Display last 2 expenses
st.subheader("📜 Expense History (Last 2 Transactions)")
if not last_2_expenses.empty:
    for index, row in last_2_expenses.iterrows():
        col1, col2, col3 = st.columns([3, 3, 3])
        col1.write(row['date_time'])
        col2.write(row['category'])
        col3.write(f"₹{row['amount']}")
else:
    st.write("No expenses recorded yet!")
