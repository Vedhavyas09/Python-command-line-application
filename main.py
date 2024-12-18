from datetime import datetime
from auth import register_user, login_user
from finance import add_transaction, view_transactions, update_transaction, delete_transaction
from db import initialize_db
from reports import generate_monthly_report, generate_yearly_report, view_transactions_by_category
from budget import set_budget, check_budget
from backup import backup_database, restore_database
import logging

def main():
    # Initialize the database
    initialize_db()

    print("Welcome to Personal Finance Manager")
    user_id = None

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = login_user(username, password)
            if user_id:
                print(f"Welcome back, {username}!")
                break
        
        elif choice == "3":
            confirm = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirm == "yes":
                print("Exiting application. Goodbye!")
                return
        
        else:
            print("Invalid choice. Please try again.")

    while True:
        print("\n1. Add Transaction\n2. View Transactions\n3. Update Transaction\n4. Delete Transaction\n"
              "5. Logout\n6. Generate Report\n7. Manage Budget\n8. Backup & Restore")
        choice = input("Choose an option: ")

        if choice == "1":
            type = input("Enter type (income/expense): ").lower()
            category = input("Enter category: ")
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
                continue
            description = input("Enter description (optional): ")
            custom_date = input("Enter date (YYYY-MM-DD) or press Enter to use the current date: ")

            if custom_date:
                try:
                    datetime.strptime(custom_date, "%Y-%m-%d")  # Validate date format
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                    continue
            else:
                custom_date = datetime.now().strftime("%Y-%m-%d")  # Use current date if none is provided

            add_transaction(user_id, type, category, amount, description, custom_date)
        
        elif choice == "2":
            type = input("Filter by type (income/expense) or press Enter to view all: ")
            view_transactions(user_id, type)

        elif choice == "3":
            try:
                transaction_id = int(input("Enter transaction ID to update: "))
            except ValueError:
                print("Invalid transaction ID. Please enter a valid number.")
                continue
            category = input("Enter new category (or press Enter to skip): ")
            amount = input("Enter new amount (or press Enter to skip): ")
            description = input("Enter new description (or press Enter to skip): ")
            update_transaction(transaction_id, category, float(amount) if amount else None, description)

        elif choice == "4":
            try:
                transaction_id = int(input("Enter transaction ID to delete: "))
            except ValueError:
                print("Invalid transaction ID. Please enter a valid number.")
                continue
            delete_transaction(transaction_id)

        elif choice == "5":
            print("Logging out. Goodbye!")
            break

        elif choice == "6":
            print("\n1. Monthly Report\n2. Yearly Report\n3. Transactions by Category")
            report_choice = input("Choose an option: ")

            if report_choice == "1":
                year = input("Enter year (YYYY): ")
                month = input("Enter month (MM): ")
                export = input("Export to CSV? (yes/no): ").lower() == "yes"
                generate_monthly_report(user_id, year, month, export)

            elif report_choice == "2":
                year = input("Enter year (YYYY): ")
                generate_yearly_report(user_id, year)

            elif report_choice == "3":
                type = input("Enter type (income/expense): ")
                view_transactions_by_category(user_id, type)

            else:
                print("Invalid choice. Returning to main menu.")

        elif choice == "7":
            print("\n1. Set Budget\n2. Check Budget\n3. Return to Main Menu")
            budget_choice = input("Choose an option: ")

            if budget_choice == "1":
                category = input("Enter category: ")
                try:
                    amount = float(input("Enter budget amount: "))
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
                    continue
                month = input("Enter month (YYYY-MM): ")
                set_budget(user_id, category, amount, month)

            elif budget_choice == "2":
                month = input("Enter month (YYYY-MM): ")
                check_budget(user_id, month)

            elif budget_choice == "3":
                continue  # Go back to the main menu

            else:
                print("Invalid choice. Returning to main menu.")

        elif choice == "8":
            print("\n1. Backup Data\n2. Restore Data")
            backup_choice = input("Choose an option: ")

            if backup_choice == "1":
                backup_database()
            elif backup_choice == "2":
                restore_database()
            else:
                print("Invalid choice. Returning to main menu.")

        else:
            print("Invalid choice. Please try again.")

    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info(f"User {user_id} added a transaction.")

if __name__ == "__main__":
    main()
