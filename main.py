from helpers import *
import get_users
import hashlib
from getpass import getpass
import datetime as dt
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

user_data = get_users.load_user_data()

# encrypt password
def hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# register
def register():
    username = format_string(input("Enter a username: "))

    # username invalid
    while len(username) == 0:
        username = format_string(input("Enter a username: "))

    # already existing username
    while username in user_data:
        print("Username taken, please try a different one")
        username = format_string(input("Enter a username: "))

    email_address = format_string(input("Enter an email address: "))
    # validate email address
    while not re.fullmatch(regex,email_address):
        print("Invalid email, please try a different one")
        email_address = format_string(input("Enter an email address: "))

    password = getpass("Enter a password: ")
    confirm_password = getpass("Confirm password: ")

    # password's match
    while password != confirm_password:
        print("Password's do not match")
        confirm_password = getpass("Confirm password: ")

    hashed_pass = hashed_password(password)

    # create transaction pin
    transaction_pin = int(getpass("Enter a 4 digit transaction pin: "))

    # validate pin
    while len(str(transaction_pin)) != 4:
        print("Pin is not a 4 digit number, Please enter a 4 digit number")
        transaction_pin = int(getpass("Enter a 4 digit transaction pin: "))

    confirm_transaction_pin = int(getpass("Confirm transaction pin: "))
    # validate pin and confirm pin
    while confirm_transaction_pin != transaction_pin:
        print("Pins do not match, Try again")
        confirm_transaction_pin = int(getpass("Confirm transaction pin: "))

    # generate new account number
    account_number = generate_random_account_number()
    current_date = dt.datetime.now().isoformat()

    # create user dictionary to store all their details
    user_data[username] = {
        "username":username,
        "email_address":email_address,
        "created_at":current_date,
        "password":hashed_pass,
        "account_number": account_number,
        "transaction_pin":transaction_pin,
        "account_balance":0,
        "transaction_history":[]
    }
    user_details = user_data[username]

    # save the user data to json file
    get_users.save_user_data(user_data)

    #registration successful
    print(f" -----------------------\n|REGISTRATION SUCCESSFUL|\n -----------------------\nUsername:{username}\nAccount Number: {user_data[username]["account_number"]}\nAccount Balance: {0}")

    # create a new BankApp object
    user = BankApp(username, user_details["account_number"])
    # user.display_account_details()
    user.bank_functions()


def login():
    username = format_string(input("-----------------------------------------\nEnter your username:  "))
    while len(username) == 0:
        username = format_string(input("Enter your username: "))
    # print("-----------------------------------------\n")
    password = getpass("-----------------------------------------\nEnter your password: ")
    while user_data[username]["password"] != hashed_password(password):
        forgot_password = format_string(input("Forgot password?(yes/no): "))
        if forgot_password == "yes":
            pass
        elif forgot_password == "no":
            pass
        password = getpass("-----------------------------------------\nEnter your password: ")

    print("-----------------------------------------\n")
    if username in user_data and user_data[username]["password"] == hashed_password(password):
        user_details = user_data[username]
        print("LOGIN SUCCESSFUL")
        print("\n")
        user = BankApp(username, user_details["account_number"])
        user.display_account_details()
        user.bank_functions()
    else:
        print("Incorrect username or password")

def change_password():
    updated_user_data = load_user_data()
    username = format_string(input("-----------------------------------------\nEnter your username: "))

    # username invalid
    while len(username) == 0:
        username = format_string(input("Enter your username: "))

    # username found
    if username in updated_user_data:
        print(f"welcome back {username}")
        old_password = getpass("-----------------------------------------\nEnter your old password: ")

        # forgot password or incorrect password
        while updated_user_data[username]["password"] != old_password:
            forgot_password = format_string(input("Forgot password?(yes/no): "))
            if forgot_password == "yes":
                pass
            elif forgot_password == "no":
                pass
            old_password = getpass("-----------------------------------------\nEnter your old password: ")

        # set new password
        if old_password == updated_user_data[username]["password"]:
            new_password = getpass("Enter your new password: ")
            updated_user_data[username]["password"] =hashed_password(new_password)
            new_user_data = updated_user_data

            # save updated personal details to json file
            get_users.save_user_data(new_user_data)
            print("Correct")
        else:
            print("Incorrect password, Try Again!")
    else:
        print("Username does not exist")



class BankApp:
    def __init__(self, username, account_number):
        self.username = username
        self.account_number = account_number
        self.is_logged_in = False


    def bank_functions(self):
        updated_user_data = load_user_data()
        actions = format_string(input("-----------------------------------------\nWhat actions do you want to perform?\nTransfer --> press 1 \nDeposit --> press 2 \nWithdraw --> press 3 \nChange password --> press 4 \nDelete Account -->press 5 \nDisplay account details --> press 6 \nView transaction history --> press 7\nLog out -->press 0\n-----------------------------------------\n"))
        if actions == "1":
            # transfer
            self.transfer()
        elif actions == "2":
            # deposit
            self.deposit()
        elif actions == "3":
            # withdraw
            self.withdraw()
        elif actions == "4":
            # change password
            change_password()
        elif actions == "5":
            # delete account
            self.remove_account()
        elif actions == "6":
            # display account information
            self.display_account_details()
        elif actions == "7":
            # view transaction history
            self.view_transaction_history()
        elif actions == "0":
            # logout
            self.logout()
        else:
            print("Invalid action")


    # logout
    def logout(self):
        self.is_logged_in = False
        exit()

    # display account details
    def display_account_details(self):
        print(f"-----------------------------------------\nHere are your account details\nUsername:{self.username}\nAccount Number: {self.account_number}\nAccount Balance: {user_data[self.username]["account_balance"]}\n-----------------------------------------\n")
        self.bank_functions()

    # transfer money to another user
    def transfer(self):
        updated_user_data = load_user_data()
        username_to_transfer = format_string(input("-----------------------------------------\nEnter the username you want to transfer to: "))
        # username does not exist
        while username_to_transfer not in updated_user_data:
            print("Username does not exist, try again")
            username_to_transfer = format_string(
                input("-----------------------------------------\nEnter the username you want to transfer to: "))

        account_number_to_transfer = format_string(input("-----------------------------------------\nEnter the recipient's account number: "))

        # Account number invalid
        while account_number_to_transfer != updated_user_data[username_to_transfer]["account_number"]:
            print("Account number invalid")
            account_number_to_transfer = format_string(
                input("-----------------------------------------\nEnter the recipient's account number: "))


        # Account number found
        if username_to_transfer in updated_user_data and account_number_to_transfer == updated_user_data[username_to_transfer]["account_number"]:
            print(f"Account Found\n{updated_user_data[username_to_transfer]["username"].upper()}")
            amount = int(input("-----------------------------------------\nEnter amount to transfer: "))

            transaction_pin = int(getpass("Enter transaction pin: "))
            while len(str(transaction_pin)) != 4 | transaction_pin != updated_user_data[self.username]["transaction_pin"]:
                print("Invalid pin, Try again")
                transaction_pin = int(getpass("Enter transaction pin: "))

            # if balance is sufficient
            if  updated_user_data[username_to_transfer]["account_balance"] > amount:
                updated_user_data[username_to_transfer]["account_balance"] += amount
                updated_user_data[self.username]["account_balance"] -= amount
                get_users.save_user_data(updated_user_data)
                # print(user_data,"TEST DATA")
                current_date = dt.datetime.now().isoformat()

                # save transaction to transaction history
                save_transaction(self.username,username_to_transfer, amount, current_date)
                # save_transaction(username_to_transfer, amount, current_date)
                # user_data[self.username]["transaction_history"].append(sender_transaction_item)
                # user_data[username_to_transfer]["transaction_history"].append(recipient_transaction_item)
                # get_users.save_user_data(user_data)
                print(
                    f"You have successfully transferred {amount} to {username_to_transfer}\nYour current balance is: {updated_user_data[self.username]["account_balance"]}")
            else:
                print("Insufficient Funds")
        else:
            print("username or account number incorrect")


    # view transaction history
    def view_transaction_history(self):
        updated_user_data = load_user_data()
        transaction_history = updated_user_data[self.username]["transaction_history"]
        for item in transaction_history:
            # print(item["user"])
            print("---------------------------------")
            if item["type"] == "out":
                # pass
                print(f"Recipient: {item["user"]}")
            if item["type"] == "in":
                print(f"Sender: {item["user"]}")
            print(f"Amount: {item["amount"]}")
            # print(f"Date: {dt.datetime.strptime(item["date"],'%c').date()}")
            print("---------------------------------")
        self.bank_functions()

    def remove_account(self):
        account_remove_warning = format_string(input("WARNING! THIS ACTION IS IRREVERSIBLE, Do you still want to continue? (yes/no): "))

        if account_remove_warning == "yes":
            user_data.pop(self.username)
            # print(user_data)
            new_user_data = user_data
            get_users.save_user_data(new_user_data)
            print("-----------------------------------------\nACCOUNT SUCCESSFULLY REMOVED\n-----------------------------------------")
            exit()
        elif account_remove_warning == "no":
            pass
        else:
            print("Invalid input")


    # deposit money into the account
    def deposit(self):
        updated_user_data = load_user_data()
        deposit = int(input("-----------------------------------------\nPlease enter the amount you want to deposit: "))

        # if the deposit amount is greater than 0
        if deposit > 0:
            updated_user_data[self.username]["account_balance"]+=deposit
            # user_data[self.username]["account_balance"] = self.balance
            new_user_data = updated_user_data

            # save the updated balance to the users details in the json file
            get_users.save_user_data(new_user_data)
            msg = f"-----------------------------------------\nDeposit of {deposit} successful!\nYour Balance is now {user_data[self.username]["account_balance"]}\n-----------------------------------------\n"
            print(msg)

            while True:
                is_continue = input("Do you still want to deposit? ")
                if format_string(is_continue) == "yes":
                   deposit = int(input("Please enter the amount you want to deposit: "))
                   # self.balance += deposit
                   user_data[self.username]["account_balance"] += deposit
                   new_user_data = user_data
                   get_users.save_user_data(new_user_data)
                   msg = f"Deposit of {deposit} successful!\nYour current balance is now {user_data[self.username]["account_balance"]}"
                   print("-----------------------------------------")
                   print(msg)
                   print("-----------------------------------------\n")
                elif format_string(is_continue) == "no":
                   break

        # go back to the bank menu
        self.bank_functions()

    # withdraw money
    def withdraw(self):
        updated_user_data = load_user_data()
        withdrawal_amount = int(input("-----------------------------------------\nEnter the amount you want to withdraw: "))
        if updated_user_data[self.username]["account_balance"] < withdrawal_amount:
            print("Insufficient funds")
        else:
            # self.balance -= withdrawal_amount
            updated_user_data[self.username]["account_balance"] -=withdrawal_amount
            get_users.save_user_data(updated_user_data)
            msg = f"-----------------------------------------\nWithdrawal successful!\nCurrent balance is: {user_data[self.username]["account_balance"]}\n-----------------------------------------"
            print(msg)
            while True:
                still_withdrawing = input("-----------------------------------------\nDo you still want to withdraw? ")
                if format_string(still_withdrawing) == "yes":
                    withdrawal_amount = int(input("-----------------------------------------\nEnter the amount you want to withdraw: "))
                    updated_user_data[self.username]["account_balance"]-=withdrawal_amount
                    get_users.save_user_data(updated_user_data)
                    msg = f"-----------------------------------------\nWithdrawal successful!\nCurrent balance is: {user_data[self.username]["account_balance"]} |\n-----------------------------------------"
                    print(msg)
                else:
                    break
        # go to bank menu
        self.bank_functions()

    # check balance
    def check_balance(self):
        updated_user_data = load_user_data()
        print(f"-----------------------------------------\nYour current balance is {updated_user_data[self.username]["account_balance"]} |\n-----------------------------------------")
        self.bank_functions()


print("Welcome to the Bank App")
is_new_user = format_string(input("Are you a new user? (yes/no): "))
if is_new_user == "yes":
    print("--------------------------\nREGISTER|\n--------------------------\n")
    register()
elif is_new_user == "no":
    print("--------------------------\nLOGIN|\n--------------------------\n")
    login()
