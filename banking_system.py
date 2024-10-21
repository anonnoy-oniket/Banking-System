import datetime

class Bank:
    def __init__(self, initial_balance) -> None:
        self.acc_list = {}
        self.total_available_balance = initial_balance
        self.total_loan = 0
        self.loan_activated = True

class Admin:
    def create_account(name, email, address, acc_type, bank):
        user = User(name, email, address, acc_type)
        bank.acc_list[user.account_no] = user
        print("User Account Added Successfully")

    def delete_user(acc_no, bank):
        if acc_no not in bank.acc_list.keys():
            print("USER DOSEN'T EXIST")
            return
        del bank.acc_list[acc_no]
        print("User removed successfully")

    def see_all_users(bank):
        print("USERS LIST: ")
        for key, val in bank.acc_list.items():
            print(val)

    def check_total_balance(bank):
        print(f"Total balance: {bank.total_available_balance}")

    def check_loan_amount(bank):
        print(f"Total loan amount: {bank.total_loan}")

    def toggle_loan_option(bank):
        if bank.loan_activated is True:
            bank.loan_activated = False
            print("Loan feature is turned off")
        else:
            bank.loan_activated = True
            print("Loan feature is turned on")

class User:
    users_list = []

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        User.users_list.append(self)
        self.account_no = len(User.users_list)+100000
        self.loan_taken = 0
        self.loan_limit = 2
        self.transaction_history = []

    def deposit(self, amount, bank):
        self.balance += amount
        current_datetime = datetime.datetime.now()
        self.transaction_history.append(f"{current_datetime} {amount}$ deposit")
        bank.total_available_balance += amount

    def withdraw(self, amount, bank):
        if self.balance < amount:
            print("Withdrawal amount exceeded")
        elif bank.total_available_balance < amount:
            print("Bank is Bankrupt")
        else:
            self.balance -= amount
            current_datetime = datetime.datetime.now()
            self.transaction_history.append(f"{current_datetime} {amount}$ withdraw")
            bank.total_available_balance -= amount

    def check_balance(self):
        print(f"Available Balance: {self.balance}")

    def check_transaction_history(self):
        print("Transaction History:")
        for s in self.transaction_history:
            print(s)
    
    def take_loan(self, amount, bank):
        print(f"Loan given of amount: {amount}")
        bank.total_loan += amount
        bank.total_available_balance -= amount
            
    def transfer_money(self, amount, acc_no, bank):
        if acc_no not in bank.acc_list.keys():
            print("Account dosen't exist")
        elif self.balance < amount:
            print("Not enough money")
        else:
            self.balance -= amount
            bank.acc_list[acc_no].balance += amount
            current_datetime = datetime.datetime.now()
            self.transaction_history.append(f"{current_datetime} {amount}$ transferred to acc_no {acc_no}")

    def __repr__(self) -> str:
        return f"Name: {self.name}; account number: {self.account_no}; email: {self.email}; acc_type: {self.account_type}"
    
bank = Bank(500000)

def main_menu():
    while True:
        s = """Log in as:
        1. Admin
        2. User
        3. Exit
        """
        print(s)
        res = int(input("Enter your choice: "))
        if res == 1:
            admin_menu()
        elif res == 2:
            user_menu()
        elif res == 3:
            break
        else:
            print("Invalid Command")

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Create User Account")
        print("2. Delete User Account")
        print("3. View All User Accounts")
        print("4. Check Total Balance of the Bank")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. Back to Main Menu")

        c = int(input("Enter your choice: "))

        if c == 1:
            name = input("Enter name: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            acc_type = input("Enter accoutn type: ")
            Admin.create_account(name, email, address, acc_type, bank)
        elif c == 2:
            acc_no = int(input("Enter account no: "))
            Admin.delete_user(acc_no, bank)
        elif c == 3:
            Admin.see_all_users(bank)
        elif c == 4:
            Admin.check_total_balance(bank)
        elif c == 5:
            Admin.check_loan_amount(bank)
        elif c == 6:
            Admin.toggle_loan_option(bank)
        elif c == 7:
            break
        else:
            print("Invalid Input")
        
def user_menu():
    acc_no = int(input("Enter account number: "))
    if acc_no not in bank.acc_list.keys():
        print("Account dosen't exist")
        return
    
    user = bank.acc_list[acc_no]

    while True:
        print(f"\nUser Menu for {user.name}:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. View Transaction History")
        print("5. Take Loan")
        print("6. Transfer Money")
        print("7. Back to Main Menu")

        c = int(input("Enter your choice: "))

        if c == 1:
            amount = int(input("Enter the amount to deposit: "))
            user.deposit(amount, bank)
        elif c == 2:
            amount = int(input("Enter the amount to withdraw: "))
            user.withdraw(amount, bank)
        elif c == 3:
            user.check_balance()
        elif c == 4:
            user.check_transaction_history()
        elif c == 5:
            if bank.loan_activated is not True:
                print("Bank is not currently giving any loans :\"(")
            elif user.loan_taken < 2:
                user.loan_taken += 1
                amount = int(input("Enter the amount of loan: "))
                user.take_loan(amount, bank)
            else:
                print("Loan taking limit exceeded")

        elif c == 6:
            acc_no = int(input("Enter the reciever account no: "))
            amount = int(input("Enter the amount: "))
            user.transfer_money(amount, acc_no, bank)
        elif c == 7:
            break
        else:
            print("Invalid Input")

main_menu()
