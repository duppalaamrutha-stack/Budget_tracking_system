💰 Budget Tracking System (Flask + SQL)

A web-based Budget Tracking System built using Flask and SQLAlchemy, designed to help users manage income, expenses, and budgets efficiently.

🚀 Features
🔐 User Registration & Login
💵 Add Income & Expense Transactions
📊 Dashboard with financial summary
📅 Monthly budget tracking
⚠️ Overspending alerts
📈 Reports (Top categories & monthly trends)
🗂 Category-based transaction management
🛠 Tech Stack
Backend: Flask (Python)
Database: SQLite (Flask app) / MySQL (SQL script)
ORM: SQLAlchemy
Frontend: HTML (Jinja templates)
📂 Project Structure
├── app.py                     # Main Flask application
├── requirements.txt          # Python dependencies
├── budget_tracking_system.sql # MySQL database script
├── templates/                # HTML templates
└── README.md                 # Project documentation
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/budget-tracker.git
cd budget-tracker
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the Application
python app.py
🌐 Usage

Open browser and go to:

http://127.0.0.1:5000/
Register a new account or use sample data
Start adding transactions and budgets
🧪 Sample Data

The app automatically creates:

Default user:

Email: ravi@example.com  
Password: password
Sample categories and transactions
🗄 Database (MySQL Version)

You can also use the provided SQL file for advanced database features.

Run SQL Script:
mysql -u root -p < budget_tracking_system.sql
Includes:
Tables: users, categories, transactions, budgets
Stored Procedures
Triggers
Views for reporting
📊 Reports Available
Top 3 expense categories
Monthly income vs expense
Budget vs actual spending
Category-wise transaction history
🔒 Future Improvements
Password hashing (security enhancement)
API integration
Charts & data visualization
Mobile responsiveness
🤝 Contributing

Feel free to fork this repository and submit pull requests.

📜 License

This project is open-source and available under the MIT License.

👩‍💻 Author
Your Name

If you want, I can also:
✅ Customize it with your GitHub username
✅ Add screenshots section
✅ Make it more attractive with badges (⭐, forks, etc.)

Give me complete info in one shoot to copy and paste

Here is your complete README.md (ready to copy & paste in one shot) 👇

# 💰 Budget Tracking System (Flask + SQL)

A web-based **Budget Tracking System** built using **Flask** and **SQLAlchemy** that helps users manage their income, expenses, and budgets effectively.

---

## 🚀 Features

- 🔐 User Registration & Login system
- 💵 Add and manage income & expense transactions
- 📊 Dashboard showing total income, expenses, and balance
- 📅 Monthly budget setting for categories
- ⚠️ Overspending alerts when budget exceeds
- 📈 Reports (Top categories & monthly summary)
- 🗂 Category-based financial tracking

---

## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (default) / MySQL (optional)
- **ORM:** SQLAlchemy
- **Frontend:** HTML, Jinja Templates

---

## 📂 Project Structure

```
├── app.py                      # Main Flask application
├── requirements.txt           # Dependencies
├── budget_tracking_system.sql # MySQL database script
├── templates/                 # HTML templates (UI)
└── README.md                  # Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/budget-tracker.git
cd budget-tracker
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment
```bash
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Mac/Linux
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application
```bash
python app.py
```

---

## 🌐 Usage

- Open your browser and go to:
  ```
  http://127.0.0.1:5000/
  ```
- Register a new account or login with sample credentials
- Add transactions and budgets
- View reports and dashboard

---

## 🧪 Sample Login

The app automatically creates sample data:

```
Email: ravi@example.com
Password: password
```

---

## 🗄 Database Support

### 🔹 SQLite (Default)
- Automatically created when you run the app

### 🔹 MySQL (Optional)

Run the SQL script:

```bash
mysql -u root -p < budget_tracking_system.sql
```

---

## 📊 Database Features (MySQL)

- Tables:
  - users
  - categories
  - transactions
  - budgets
  - monthly_summary

- Stored Procedure:
  - monthly_spending_per_category

- Function:
  - is_budget_exceeded

- Trigger:
  - trg_after_transaction_insert

- Views:
  - monthly_income_expense_summary
  - budget_vs_actual
  - category_transaction_history

---

## 📈 Reports Included

- Top 3 expense categories
- Monthly income vs expense
- Budget vs actual comparison
- Transaction history by category

---

## 🔒 Future Improvements

- Password encryption (hashing)
- Graphs & charts (visual dashboard)
- REST API integration
- Mobile-friendly UI
- Export reports (PDF/Excel)

---

## 🤝 Contributing

1. Fork the repository  
2. Create your feature branch  
3. Commit your changes  
4. Push to the branch  
5. Open a Pull Request  

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👩‍💻 Author

D.AMRUTHA
⭐ If you like this project, don't forget to star the repository!
