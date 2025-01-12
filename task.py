import sqlite3
from getpass import getpass

# Database setup
conn = sqlite3.connect("finance_manager.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')
conn.commit()

# User registration
def register_user():
    print("\n=== Register ===")
    username = input("Enter a username: ").strip()
    password = getpass("Enter a password: ").strip()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Try again.")

# User login
def login_user():
    print("\n=== Login ===")
    username = input("Enter your username: ").strip()
    password = getpass("Enter your password: ").strip()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return user[0]
    else:
        print("Invalid username or password.")
        return None

# Add income or expense
def add_transaction(user_id):
    print("\n=== Add Transaction ===")
    t_type = input("Type (income/expense): ").strip().lower()
    if t_type not in ["income", "expense"]:
        print("Invalid type. Choose 'income' or 'expense'.")
        return
    category = input("Category (e.g., Food, Rent, Salary): ").strip()
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ").strip()
    cursor.execute('''
        INSERT INTO transactions (user_id, type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, t_type, category, amount, date))
    conn.commit()
    print(f"{t_type.capitalize()} added successfully!")

# View transactions
def view_transactions(user_id):
    print("\n=== Transactions ===")
    cursor.execute("SELECT type, category, amount, date FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cursor.fetchall()
    if transactions:
        for t in transactions:
            print(f"{t[3]} - {t[0].capitalize()} - {t[1]}: ${t[2]:.2f}")
    else:
        print("No transactions found.")

# Main menu
def main_menu(user_id):
    while True:
        print("\n=== Main Menu ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction(user_id)
        elif choice == "2":
            view_transactions(user_id)
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

# Main program
def main():
    while True:
        print("\n=== Personal Finance Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_user()
        elif choice == "2":
            user_id = login_user()
            if user_id:
                main_menu(user_id)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
