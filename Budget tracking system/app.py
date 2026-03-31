import os
import calendar
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'replace-with-a-secret-key')

@app.context_processor
def inject_globals():
    return {
        'current_year': date.today().year
    }

DB_PATH = os.path.join(os.path.dirname(__file__), 'budget_tracking.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      password TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS categories (
      category_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      type TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS transactions (
      transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      category_id INTEGER NOT NULL,
      amount REAL NOT NULL,
      transaction_date TEXT NOT NULL,
      description TEXT,
      FOREIGN KEY (user_id) REFERENCES users(user_id),
      FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );

    CREATE TABLE IF NOT EXISTS budgets (
      budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      category_id INTEGER NOT NULL,
      limit_amount REAL NOT NULL,
      month TEXT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(user_id),
      FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    ''')

    cursor.execute('INSERT OR IGNORE INTO categories (category_id, name, type) VALUES (1, ?, ?)', ('Salary', 'Income'))
    cursor.execute('INSERT OR IGNORE INTO categories (category_id, name, type) VALUES (2, ?, ?)', ('Rent', 'Expense'))
    cursor.execute('INSERT OR IGNORE INTO categories (category_id, name, type) VALUES (3, ?, ?)', ('Food', 'Expense'))
    cursor.execute('INSERT OR IGNORE INTO categories (category_id, name, type) VALUES (4, ?, ?)', ('Utilities', 'Expense'))
    cursor.execute('INSERT OR IGNORE INTO categories (category_id, name, type) VALUES (5, ?, ?)', ('Investment', 'Income'))
    conn.commit()
    cursor.close()
    conn.close()

if not os.path.exists(DB_PATH):
    init_db()


def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY type DESC, name ASC')
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']

        if not name or not email or not password:
            flash('Please fill all fields.', 'danger')
            return render_template('register.html')

        if get_user_by_email(email):
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = get_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))

        flash('Invalid email or password.', 'danger')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    today = date.today()
    month_num = today.month
    month = f"{month_num:02d}"
    year = str(today.year)
    month_name = today.strftime('%B')
    first_day = date(int(year), month_num, 1)
    last_day = date(int(year), month_num, calendar.monthrange(int(year), month_num)[1])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT IFNULL(SUM(t.amount), 0) AS total_income "
        "FROM transactions t "
        "JOIN categories c ON t.category_id = c.category_id "
        "WHERE t.user_id = ? AND c.type = 'Income' "
        "AND strftime('%m', t.transaction_date) = ? "
        "AND strftime('%Y', t.transaction_date) = ?",
        (user_id, month, year),
    )
    monthly_income = cursor.fetchone()['total_income']

    cursor.execute(
        "SELECT IFNULL(SUM(t.amount), 0) AS total_expense "
        "FROM transactions t "
        "JOIN categories c ON t.category_id = c.category_id "
        "WHERE t.user_id = ? AND c.type = 'Expense' "
        "AND strftime('%m', t.transaction_date) = ? "
        "AND strftime('%Y', t.transaction_date) = ?",
        (user_id, month, year),
    )
    monthly_expense = cursor.fetchone()['total_expense']

    cursor.execute(
        "SELECT c.name AS category_name, IFNULL(SUM(t.amount), 0) AS amount "
        "FROM categories c "
        "LEFT JOIN transactions t ON c.category_id = t.category_id "
        "AND t.user_id = ? "
        "AND strftime('%m', t.transaction_date) = ? "
        "AND strftime('%Y', t.transaction_date) = ? "
        "WHERE c.type = 'Expense' "
        "GROUP BY c.category_id, c.name "
        "HAVING amount > 0 "
        "ORDER BY amount DESC",
        (user_id, month, year),
    )
    expense_categories = cursor.fetchall()

    cursor.execute(
        "SELECT b.budget_id, c.name AS category_name, b.limit_amount, "
        "IFNULL(SUM(t.amount), 0) AS spent "
        "FROM budgets b "
        "JOIN categories c ON b.category_id = c.category_id "
        "LEFT JOIN transactions t ON t.category_id = b.category_id "
        "AND t.user_id = b.user_id "
        "AND strftime('%m', t.transaction_date) = ? "
        "AND strftime('%Y', t.transaction_date) = ? "
        "WHERE b.user_id = ? "
        "GROUP BY b.budget_id, c.name, b.limit_amount "
        "ORDER BY b.limit_amount DESC",
        (month, year, user_id),
    )
    budget_utilization = cursor.fetchall()

    cursor.execute(
        "SELECT t.transaction_id, c.name AS category_name, c.type, t.amount, t.transaction_date, t.description "
        "FROM transactions t "
        "JOIN categories c ON t.category_id = c.category_id "
        "WHERE t.user_id = ? "
        "ORDER BY t.transaction_date DESC "
        "LIMIT 12",
        (user_id,),
    )
    recent_transactions = cursor.fetchall()

    cursor.execute(
        "SELECT IFNULL(SUM(t.amount), 0) AS actual_income "
        "FROM transactions t "
        "JOIN categories c ON t.category_id = c.category_id "
        "WHERE t.user_id = ? AND c.type = 'Income'",
        (user_id,),
    )
    total_income = cursor.fetchone()['actual_income']

    cursor.execute(
        "SELECT IFNULL(SUM(t.amount), 0) AS actual_expense "
        "FROM transactions t "
        "JOIN categories c ON t.category_id = c.category_id "
        "WHERE t.user_id = ? AND c.type = 'Expense'",
        (user_id,),
    )
    total_expense = cursor.fetchone()['actual_expense']

    available_balance = monthly_income - monthly_expense
    expense_ratio = 0
    budget_health = 0
    if monthly_income > 0:
        expense_ratio = round((monthly_expense / monthly_income) * 100, 2)
        budget_health = max(0, 100 - expense_ratio)

    cash_message = (
        f"Great job! You have ₹{available_balance:,.2f} excess money this month."
        if available_balance >= 0
        else f"Warning: You are overspending by ₹{abs(available_balance):,.2f} this month."
    )

    budget_alerts = [
        row for row in budget_utilization if row['spent'] > row['limit_amount']
    ]
    total_budget_amount = sum(row['limit_amount'] for row in budget_utilization)
    total_budget_left = sum(
        max(row['limit_amount'] - row['spent'], 0) for row in budget_utilization
    )
    top_expense_categories = expense_categories[:3]

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        user_name=session.get('user_name'),
        month_name=month_name,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        total_income=total_income,
        total_expense=total_expense,
        available_balance=available_balance,
        expense_ratio=expense_ratio,
        budget_health=budget_health,
        cash_message=cash_message,
        budget_alerts=budget_alerts,
        total_budget_amount=total_budget_amount,
        total_budget_left=total_budget_left,
        expense_categories=expense_categories,
        budget_utilization=budget_utilization,
        top_expense_categories=top_expense_categories,
        recent_transactions=recent_transactions,
    )


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    categories = get_categories()
    conn = get_db_connection()
    cursor = conn.cursor()

    current_date = date.today().isoformat()

    if request.method == 'POST':
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        transaction_date = request.form.get('transaction_date')
        description = request.form.get('description', '').strip()

        if not category_id or not amount or not transaction_date:
            cursor.close()
            conn.close()
            flash('Category, amount, and date are required.', 'danger')
            return redirect(url_for('transactions'))

        try:
            amount_value = float(amount)
        except ValueError:
            cursor.close()
            conn.close()
            flash('Enter a valid amount.', 'danger')
            return redirect(url_for('transactions'))

        cursor.execute(
            'INSERT INTO transactions (user_id, category_id, amount, transaction_date, description) VALUES (?, ?, ?, ?, ?)',
            (user_id, category_id, amount_value, transaction_date, description),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Transaction saved successfully.', 'success')
        return redirect(url_for('transactions'))

    cursor.execute(
        'SELECT t.transaction_id, t.transaction_date, c.name AS category_name, c.type, t.amount, t.description '
        'FROM transactions t '
        'JOIN categories c ON t.category_id = c.category_id '
        'WHERE t.user_id = ? '
        'ORDER BY t.transaction_date DESC, t.transaction_id DESC',
        (user_id,),
    )
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('transactions.html', categories=categories, transactions=transactions, current_date=current_date)


@app.route('/budgets', methods=['GET', 'POST'])
def budgets():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    categories = get_categories()
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        category_id = request.form.get('category_id')
        limit_amount = request.form.get('limit_amount')
        month = request.form.get('month', '').strip() or date.today().strftime('%B')

        if not category_id or not limit_amount or not month:
            flash('Category, limit amount, and month are required.', 'danger')
            return redirect(url_for('budgets'))

        try:
            limit_value = float(limit_amount)
        except ValueError:
            flash('Enter a valid budget amount.', 'danger')
            return redirect(url_for('budgets'))

        cursor.execute(
            'INSERT INTO budgets (user_id, category_id, limit_amount, month) VALUES (?, ?, ?, ?)',
            (user_id, category_id, limit_value, month),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Budget added successfully.', 'success')
        return redirect(url_for('budgets'))

    cursor.execute(
        'SELECT b.budget_id, b.month, c.name AS category_name, b.limit_amount '
        'FROM budgets b '
        'JOIN categories c ON b.category_id = c.category_id '
        'WHERE b.user_id = ? '
        'ORDER BY b.month ASC, c.name ASC',
        (user_id,),
    )
    budgets = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('budgets.html', categories=categories, budgets=budgets)


if __name__ == '__main__':
    app.run(debug=True)
