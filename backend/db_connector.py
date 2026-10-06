import  mysql.connector
from contextlib import contextmanager
from datetime import date
@contextmanager
def get_db_connection(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)

    if connection.is_connected():
        print("Connected to MySQL database")
    else:
        print("Failed to connect to MySQL database")

    yield cursor

    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def get_fetch_all_data():
    with get_db_connection() as cursor:
        cursor.execute("SELECT * FROM expenses")
        return cursor.fetchall()

def fetch_data_by_date(expense_date):
    with get_db_connection() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date=%s", (expense_date,))
        expenses=cursor.fetchall()
        return expenses
def insert_expense(expense_date,amount, category, notes):
    with get_db_connection(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses(expense_date, amount, category, notes) VALUES (%s,%s,%s,%s)", (expense_date,amount,category,notes))

def delete_expense(expense_date):
    with get_db_connection(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date=%s", (expense_date,))


def get_summary_by_date(start_date:date, end_date:date):
    with get_db_connection() as cursor:
        cursor.execute('''SELECT category, sum(amount) as total  FROM expenses WHERE expense_date between %s and %s group by category''', (start_date,end_date))
        expenses=cursor.fetchall()
        return expenses
if __name__ == '__main__':
    print(fetch_data_by_date("2024-08-15"))
    # data=get_summary_by_date("2024-08-02","2024-09-05")
    # for row in data:
    #     print(row)
    # delete_expense("2024-08-15")
    # insert_expense("2024-08-15", 250, "Food","buying dosa")