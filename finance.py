import sqlite3
from datetime import datetime

def add_transaction(user_id, type, category, amount, description="", custom_date=None):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        # Use the custom date if provided, otherwise use the current date
        date = custom_date if custom_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert transaction
        cursor.execute("""
            INSERT INTO transactions (user_id, type, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, type, category, amount, date, description))
        
        connection.commit()
        print("Transaction added successfully!")

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()

def view_transactions(user_id, type=None):
    connection = sqlite3.connect("finance_manager.db")
    cursor = connection.cursor()

    if type:
        cursor.execute("SELECT * FROM transactions WHERE user_id = ? AND type = ?", (user_id, type))
    else:
        cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))

    transactions = cursor.fetchall()
    connection.close()
    return transactions if transactions else []  # Ensure it returns an empty list if no transactions

def update_transaction(transaction_id, category=None, amount=None, description=None):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        if category:
            cursor.execute("""
                UPDATE transactions SET category = ? WHERE id = ?
            """, (category, transaction_id))
        
        if amount:
            cursor.execute("""
                UPDATE transactions SET amount = ? WHERE id = ?
            """, (amount, transaction_id))
        
        if description:
            cursor.execute("""
                UPDATE transactions SET description = ? WHERE id = ?
            """, (description, transaction_id))
        
        connection.commit()
        print("Transaction updated successfully!")

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()

def delete_transaction(transaction_id):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        connection.commit()
        print("Transaction deleted successfully!")

    except Exception as e:
        print("Error:", e)
    
    finally:
        connection.close()
