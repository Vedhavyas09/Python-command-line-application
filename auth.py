# auth.py
import sqlite3

def register_user(username, password):
    try:
        connection = sqlite3.connect("finance_manager.db")
        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print("Error: Username already exists!")
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()

    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return None


def login_user(username, password):
    connection = sqlite3.connect("finance_manager.db")
    cursor = connection.cursor()

    # Check if the user exists
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    connection.close()
    if user:
        print("Login successful!")
        return user[0]  # Return the user ID
    else:
        print("Invalid username or password!")
        return None

