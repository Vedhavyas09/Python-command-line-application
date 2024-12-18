import sqlite3
from export import export_to_csv

def generate_monthly_report(user_id, year, month, export=False):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        # Get total income
        cursor.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'income'
            AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
        """, (user_id, str(year), f"{int(month):02d}"))
        total_income = cursor.fetchone()[0] or 0.0

        # Get total expenses
        cursor.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'expense'
            AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
        """, (user_id, str(year), f"{int(month):02d}"))
        total_expenses = cursor.fetchone()[0] or 0.0

        # Calculate savings
        savings = total_income - total_expenses

        print("\nMonthly Report:")
        print(f"Year: {year}, Month: {month}")
        print(f"Total Income: {total_income:.2f}")
        print(f"Total Expenses: {total_expenses:.2f}")
        print(f"Savings: {savings:.2f}")

        # Get category-wise expenses
        cursor.execute("""
            SELECT category, SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'expense'
            AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
            GROUP BY category
        """, (user_id, str(year), f"{int(month):02d}"))
        categories = cursor.fetchall()

        # Prepare data for export
        if export:
            data = {
                "headers": ["Category", "Amount"],
                "rows": [(category, total) for category, total in categories]
            }
            filename = f"monthly_report_{year}_{month}.csv"
            export_to_csv(data, filename)

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()

def generate_yearly_report(user_id, year):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        # Get total income
        cursor.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'income'
            AND strftime('%Y', date) = ?
        """, (user_id, str(year)))
        total_income = cursor.fetchone()[0] or 0.0

        # Get total expenses
        cursor.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'expense'
            AND strftime('%Y', date) = ?
        """, (user_id, str(year)))
        total_expenses = cursor.fetchone()[0] or 0.0

        # Calculate savings
        savings = total_income - total_expenses

        print("\nYearly Report:")
        print(f"Year: {year}")
        print(f"Total Income: {total_income:.2f}")
        print(f"Total Expenses: {total_expenses:.2f}")
        print(f"Savings: {savings:.2f}")

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()

def view_transactions_by_category(user_id, type):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        # Group transactions by category
        cursor.execute("""
            SELECT category, SUM(amount) FROM transactions
            WHERE user_id = ? AND type = ?
            GROUP BY category
        """, (user_id, type))
        categories = cursor.fetchall()

        print(f"\n{type.capitalize()} by Category:")
        for category, total in categories:
            print(f"{category}: {total:.2f}")

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()
