import sqlite3

def set_budget(user_id, category, amount, month):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        # Check if a budget already exists for this category and month
        cursor.execute("""
            SELECT * FROM budgets WHERE user_id = ? AND category = ? AND month = ?
        """, (user_id, category, month))
        existing_budget = cursor.fetchone()

        if existing_budget:
            # Update existing budget
            cursor.execute("""
                UPDATE budgets SET amount = ? WHERE user_id = ? AND category = ? AND month = ?
            """, (amount, user_id, category, month))
            print("Budget updated successfully!")
        else:
            # Insert new budget
            cursor.execute("""
                INSERT INTO budgets (user_id, category, amount, month)
                VALUES (?, ?, ?, ?)
            """, (user_id, category, amount, month))
            print("Budget set successfully!")

        connection.commit()

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()


def check_budget(user_id, month):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        # Retrieve budgets for the month
        cursor.execute("""
            SELECT category, amount FROM budgets
            WHERE user_id = ? AND month = ?
        """, (user_id, month))
        budgets = cursor.fetchall()

        # Calculate spending per category
        cursor.execute("""
            SELECT category, SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'expense' AND strftime('%Y-%m', date) = ?
            GROUP BY category
        """, (user_id, month))
        spending = cursor.fetchall()

        # Convert spending to a dictionary for easier comparison
        spending_dict = {category: total for category, total in spending}

        print("\nBudget Report for", month)
        for category, budget in budgets:
            spent = spending_dict.get(category, 0.0)
            print(f"Category: {category}")
            print(f"  Budget: {budget:.2f}")
            print(f"  Spent: {spent:.2f}")
            if spent > budget:
                print(f"  ⚠️ Over budget by {spent - budget:.2f}!")
            else:
                print(f"  ✅ Under budget by {budget - spent:.2f}")

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()
