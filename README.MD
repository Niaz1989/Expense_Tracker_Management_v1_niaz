💰 Expense Tracking System
A simple web app for recording daily expenses and viewing spending breakdowns by category. Built with FastAPI, Jinja2 templates, and MySQL. The UI uses plain HTML and CSS only (no external CDN or JavaScript libraries), so it works fully offline.
Features
Add / Update Expenses – pick a date, view that day's expenses, edit them, and add new rows.
Analytics – choose a date range to see total spending, a per-category percentage bar chart, and a detailed breakdown table.
Categories – Food, Entertainment, Utilities, Rent, Transport, Other.
Tech Stack
Layer	Technology
Backend	FastAPI, Uvicorn
Templates	Jinja2
Database	MySQL (`mysql-connector-python`)
Frontend	HTML + inline CSS
Project Structure
```
project-root/
├── backend/
│   ├── main.py            # FastAPI app and routes
│   └── db_connector.py    # MySQL helper functions
├── frontend/
│   └── templates/
│       ├── base.html      # Shared layout and navigation
│       ├── add_update.html
│       └── analytics.html
├── requirements.txt
└── README.md
```
> Adjust the file names above if yours differ (for example, if the FastAPI file is not called `main.py`).
Prerequisites
Python 3.9+
MySQL Server running locally
Setup
1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Create the database and table
Log in to MySQL and run:
```sql
CREATE DATABASE expense_manager;
USE expense_manager;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    notes VARCHAR(255)
);
```
3. Configure the database connection
Connection settings live in `backend/db_connector.py`:
```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="expense_manager"
)
```
Update the `user` and `password` to match your MySQL setup.
4. Run the app
From the `backend` folder:
```bash
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000 in your browser.
Routes
Method	Path	Description
GET	`/`	Redirects to the Add / Update page
GET	`/ui/add-update`	Show and edit expenses for a given date
POST	`/ui/save-expenses`	Save the submitted expenses for a date
GET	`/ui/analytics`	Show category totals for a date range
Query parameters
`/ui/add-update?expense_date=YYYY-MM-DD&rows=N` – `rows` adds N extra blank rows.
`/ui/analytics?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
How Saving Works
When you click Save changes to Database, the app deletes all existing expenses for the selected date and re-inserts every row from the form. Rows with an empty amount or category are skipped.
Notes
Default dates in `main.py` (`2026-08-14` for the add/update page and `2026-07-18` to `2026-08-18` for analytics) are hardcoded. Change them to suit your data.
Database credentials are hardcoded for local development. For anything beyond that, move them to environment variables.
License
Free to use and modify for personal or educational projects.