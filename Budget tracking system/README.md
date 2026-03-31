# Budget Tracking System

A simple personal budget tracking website with a Python Flask backend, local SQLite database, and a responsive frontend that shows dashboard metrics and pie charts.

## Features
- User registration and login
- Monthly income and expense summary
- Expense category distribution chart
- Budget utilization chart
- Recent transaction list
- Transaction entry and history page
- Budget creation and overview page

## Files
- `app.py` — Flask backend application using local SQLite
- `budget_tracking.db` — SQLite database file created automatically on first run
- `templates/` — HTML templates for login, registration, and dashboard
- `static/css/style.css` — frontend styling
- `requirements.txt` — Python dependencies

## Setup
1. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. The application uses a local SQLite file database so no external database server is required.
3. Run the app:
   ```bash
   python app.py
   ```

## Run the app
Open `http://127.0.0.1:5000` in your browser.

Open `http://127.0.0.1:5000` in your browser.

## Notes
- If you want to use the sample user from `schema.sql`, replace the placeholder password hash with a valid hash or register a new user.
- The charts are rendered with Chart.js from CDN.
