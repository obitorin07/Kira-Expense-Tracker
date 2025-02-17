# Kira Expense Tracker

Kira Expense Tracker is a personal finance tracking app designed to help you log and analyze your monthly expenses. It allows you to categorize spending, set budgets, and track trends over time.

## Technologies Used
- **Streamlit** – for the interactive web interface  
- **MySQL** – as the database backend  
- **mysql-connector-python** – to connect Python with MySQL  
- **python-dotenv** – to manage environment variables  

## Features
✅ **Log Expenses** – Store date, time, category, amount, and description  
✅ **Categorize Spending** – Track expenses under predefined or custom categories  
✅ **Monthly Budgeting** – Set a budget and see overspending in red  
✅ **Data Storage** – Uses MySQL to securely store all transactions  

## Setup

1. **Database Setup:**  
   Run the provided `database.sql` to create the `expense_tracker` database and necessary tables.

2. **Environment Variables:**  
   Create a file named `credentials.env` in the project root with the following dummy information (replace with actual details):
   ```env
   host='localhost'
   database='expense_tracker'
   user='your_username'
   password='your_password'

3. **Install dependencies:**
``` pip install streamlit mysql-connector-python python-dotenv ```


4. **How to run? :**
``` Open Terminal and just type :- streamlit run app.py ```

![Screenshot]()

**Thank you :)**