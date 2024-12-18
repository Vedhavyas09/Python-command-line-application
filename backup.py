import shutil

def backup_database():
    try:
        shutil.copy("finance_manager.db", "finance_manager_backup.db")
        print("Backup created successfully!")
    except Exception as e:
        print("Error creating backup:", e)

def restore_database():
    try:
        shutil.copy("finance_manager_backup.db", "finance_manager.db")
        print("Database restored successfully!")
    except Exception as e:
        print("Error restoring database:", e)
