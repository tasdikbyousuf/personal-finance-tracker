import pandas as pd

def add_transaction(filename, transaction):
    try:
        df = pd.read_excel(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Description', 'Expense', 'Income'])

    # Classify transaction type (Expense or Income)
    if transaction['Amount'] < 0:
        df = df._append({'Description': transaction['Description'], 'Expense': -transaction['Amount'], 'Income': 0}, ignore_index=True)
    else:
        df = df._append({'Description': transaction['Description'], 'Expense': 0, 'Income': transaction['Amount']}, ignore_index=True)

    # Calculate and add net balance
    df['Net Balance'] = df['Income'].cumsum() - df['Expense'].cumsum()

    df.to_excel(filename, index=False)
    print("Transaction added successfully.")

def display_transactions(filename):
    try:
        df = pd.read_excel(filename)
    except FileNotFoundError:
        print("No transactions found.")
        return 0.0

    print(df.to_string(index=False))

    # Separate expenses and incomes
    expenses = df[df['Expense'] > 0]
    incomes = df[df['Income'] > 0]

    # Display expenses
    if not expenses.empty:
        print("\nExpenses:")
        print(expenses[['Description', 'Expense', 'Net Balance']].to_string(index=False))

    # Display incomes
    if not incomes.empty:
        print("\nIncomes:")
        print(incomes[['Description', 'Income', 'Net Balance']].to_string(index=False))

    # Calculate and display net balance
    net_balance = df['Net Balance'].iloc[-1]
    #print(f'\nNet Balance: {net_balance}')

    return net_balance

def main():
    filename = 'transactions_with_separate_columns.xlsx'

    while True:
        print("1. Add Expense/Income")
        print("2. View Transactions")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter Description: ")
            amount = float(input("Enter Amount: "))
            transaction = {'Description': description, 'Amount': amount}
            add_transaction(filename, transaction)
        elif choice == '2':
            net_balance = display_transactions(filename)
            print(f'Net Balance: {net_balance}')
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
