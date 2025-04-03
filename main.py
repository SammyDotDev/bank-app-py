from helpers import *
import get_users
import hashlib
from getpass import getpass
import datetime as dt
import re
import time

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

user_data = get_users.load_user_data()

# encrypt password
def hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# register
def register():
    username = format_string(input("Enter a username: "))
    time.sleep(3)

    # username invalid
    while len(username) == 0:
        print("Username Invalid")
        username = format_string(input("Enter a username: "))
        time.sleep(3)

    # already existing username
    while username in user_data:
        print("Username taken, please try a different one")
        username = format_string(input("Enter a username: "))
        time.sleep(3)

    email_address = format_string(input("Enter an email address: "))
    # validate email address
    while not re.fullmatch(regex,email_address):
        print("Invalid email, please try a different one")
        email_address = format_string(input("Enter an email address: "))
        time.sleep(3)

    password = getpass("Enter a password: ")
    confirm_password = getpass("Confirm password: ")
    time.sleep(3)

    # password's match
    while password != confirm_password:
        print("Password's do not match")
        confirm_password = getpass("Confirm password: ")
        time.sleep(3)

    hashed_pass = hashed_password(password)
    time.sleep(1);print(".")
    time.sleep(1);print("..")
    time.sleep(1);print("...")
    print("loading...")
    time.sleep(5)

    # create transaction pin
    transaction_pin = int(getpass("Enter a 4 digit transaction pin: "))
    time.sleep(3)

    # validate pin
    while len(str(transaction_pin)) != 4:
        print("Pin is not a 4 digit number, Please enter a 4 digit number")
        transaction_pin = int(getpass("Enter a 4 digit transaction pin: "))

    confirm_transaction_pin = int(getpass("Confirm transaction pin: "))
    time.sleep(1);print(".")
    time.sleep(1);print("..")
    time.sleep(1);print("...")
    print("loading...")
    time.sleep(5)

    # validate pin and confirm pin
    while confirm_transaction_pin != transaction_pin:
        print("Pins do not match, Try again")
        confirm_transaction_pin = int(getpass("Confirm transaction pin: "))
        time.sleep(1);print(".")
        time.sleep(1);print("..")
        time.sleep(1);print("...")
        print("loading...")
        time.sleep(5)

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
        "transaction_limit":500000,
        "transaction_history":[],
    }
    user_details = user_data[username]

    # save the user data to json file
    get_users.save_user_data(user_data)
    time.sleep(1);print(".")
    time.sleep(1);print("..")
    time.sleep(1);print("...")
    print("loading...")
    time.sleep(5)

    #registration successful
    print(f" -----------------------\n|REGISTRATION SUCCESSFUL|\n -----------------------\nUsername:{username}\nAccount Number: {user_data[username]["account_number"]}\nAccount Balance: {0}")

    # create a new BankApp object
    user = BankApp(username, user_details["account_number"])
    # user.display_account_details()
    user.bank_functions()


def login():
    updated_user_data = load_user_data()
    username = format_string(input("-----------------------------------------\nEnter your username:  "))
    time.sleep(3)

    # check if account exists
    while username not in updated_user_data:
        print(f"Account with username '{username}' does not exist")
        username = format_string(input("-----------------------------------------\nEnter your username:  "))
        time.sleep(3)


    while len(username) == 0:
        print("Invalid Username")
        username = format_string(input("Enter your username: "))
        time.sleep(3)

    email_address = format_string(input("Enter your email address: "))
    time.sleep(3)

    while not re.fullmatch(regex, email_address):
        print("Invalid email address format")
        email_address = format_string(input("Enter your email address: "))
        time.sleep(3)

    while email_address != updated_user_data[username]["email_address"]:
        print("Invalid email address")
        email_address = format_string(input("Enter your email address"))
        time.sleep(3)



    # print("-----------------------------------------\n")
    password = getpass("-----------------------------------------\nEnter your password: ")
    time.sleep(1);print(".")
    time.sleep(1);print("..")
    time.sleep(1);print("...")
    print("loading...")
    time.sleep(5)
    while updated_user_data[username]["password"] != hashed_password(password):
        forgot_password = format_string(input("Forgot password?(yes/no): "))
        if forgot_password == "yes":
            pass
        elif forgot_password == "no":
            pass
        password = getpass("-----------------------------------------\nEnter your password: ")

    print("-----------------------------------------\n")
    if username in updated_user_data and updated_user_data[username]["password"] == hashed_password(password):
        user_details = updated_user_data[username]
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
    time.sleep(3)

    # username invalid
    while len(username) == 0 or username not in updated_user_data:
        print("Invalid username")
        username = format_string(input("Enter your username: "))
        time.sleep(3)

    # username found
    if username in updated_user_data:
        print(f"welcome back {username}")
        old_password = hashed_password(getpass("-----------------------------------------\nEnter your old password: "))
        time.sleep(3)

        # forgot password or incorrect password
        while updated_user_data[username]["password"] != old_password:
            forgot_password = format_string(input("Forgot password?(yes/no): "))
            if forgot_password == "yes":
                pass
            elif forgot_password == "no":
                pass
            old_password = hashed_password(getpass("-----------------------------------------\nEnter your old password: "))
            time.sleep(1);print(".")
            time.sleep(1);print("..")
            time.sleep(1);print("...")
            print("loading...")
            time.sleep(5)

        # set new password
        if old_password == updated_user_data[username]["password"]:
            new_password = getpass("Enter your new password: ")
            confirm_new_password = getpass("Confirm new password: ")
            time.sleep(3)
            while confirm_new_password != new_password:
                print("Passwords don't match")
                confirm_new_password = getpass("Confirm new password: ")
                time.sleep(3)

            updated_user_data[username]["password"] =hashed_password(new_password)
            new_user_data = updated_user_data

            # save updated personal details to json file
            get_users.save_user_data(new_user_data)
            time.sleep(1);print(".")
            time.sleep(1);print("..")
            time.sleep(1);print("...")
            print("loading...")
            time.sleep(5)
            print("Password Updated")
        else:
            print("Incorrect password, Try Again!")
    else:
        print("Username does not exist")

# change username
def change_username():
    while True:
        try:
            updated_user_data = load_user_data()
            username = format_string(input("-----------------------------------------\nEnter your current username: "))
            time.sleep(3)

            # username invalid
            while len(username) == 0 or username not in updated_user_data:
                print("Invalid username")
                username = format_string(input("Enter your current username: "))
                time.sleep(3)

            new_username = format_string(input("-----------------------------------------\nEnter your new username: "))
            time.sleep(3)
            while len(new_username) == 0 or username not in updated_user_data:
                print("Invalid username")
                username = format_string(input("Enter your new username: "))
                time.sleep(3)

            while new_username in updated_user_data:
                print("Username exists")
                new_username = format_string(input("-----------------------------------------\nEnter your new username: "))
                time.sleep(3)

            print(f"Username '{new_username}' is available")

            # copy old user data
            new_user_data = updated_user_data[username]

            # assign old userdata to new username
            updated_user_data[new_username] = new_user_data
            updated_user_data[new_username]["username"] = new_username
            get_users.save_user_data(updated_user_data)
            # updated_user_data.pop(username)
            updated_user_data.pop(username)
            get_users.save_user_data(updated_user_data)
            time.sleep(1);print(".")
            time.sleep(1);print("..")
            time.sleep(1);print("...")
            print("loading...")
            time.sleep(5)
            print("Username changed successfully!")
            break
        except:
            print("Please Try Again. An error occurred")

def change_email_address(username):
    while True:
        try:
            updated_user_data = load_user_data()
            email_address = format_string(input("-----------------------------------------\nEnter your current email address: "))
            time.sleep(3)

            #invalid email address format
            while not re.fullmatch(regex, email_address):
                print("Invalid email address format")
                email_address = format_string(
                    input("-----------------------------------------\nEnter your current email address: "))
                time.sleep(3)

            # if entered email address is not equal to current address
            while email_address != updated_user_data[username]["email_address"]:
                print("Email address does not match your current email address")
                email_address = format_string(
                    input("-----------------------------------------\nEnter your current email address: "))
                time.sleep(3)
            new_email_address = format_string(input("-----------------------------------------\nEnter your new email address: "))
            time.sleep(3)

            # invalid email address format
            while not re.fullmatch(regex, new_email_address):
                print("Invalid email address format")
                new_email_address = format_string(
                    input("-----------------------------------------\nEnter your new email address: "))
                time.sleep(3)

            while new_email_address in updated_user_data:
                print("This email address already exists\nTry Again!")
                new_email_address = format_string(
                    input("-----------------------------------------\nEnter your new email address: "))
                time.sleep(3)

            print(f"Email address '{new_email_address}'")
            updated_user_data[username]["email_address"] = new_email_address
            get_users.save_user_data(updated_user_data)
            time.sleep(1);print(".")
            time.sleep(1);print("..")
            time.sleep(1);print("...")
            print("loading...")
            time.sleep(5)
            print("Email address updated successfully!")

            break

        except:
            print("Try again, An error occurred")

def update_transaction_limit(username):
    updated_user_data = load_user_data()
    max_limit = 5000000
    min_limit = 5000

    print(f"Maximum Transaction Limit: {max_limit}\nMinimum Transaction Limit: {min_limit}")
    print("-----------------------------------------\n")
    while True:
        try:
            new_transaction_limit = int(format_string(input("Enter new transaction limit: ")))
            time.sleep(3)

            while new_transaction_limit > max_limit or new_transaction_limit < min_limit:
                print(f"Transaction limit must be between {min_limit} and {max_limit}")
                new_transaction_limit = int(format_string(input("Enter new transaction limit: ")))
                time.sleep(3)

            updated_user_data[username]["transaction_limit"] = new_transaction_limit
            get_users.save_user_data(updated_user_data)
            time.sleep(1);print(".")
            time.sleep(1);print("..")
            time.sleep(1);print("...")
            print("loading...")
            time.sleep(5)
            print("Transaction limit upgraded successfully")
            break
        except ValueError:
            print("Invalid Transaction Amount.")










class BankApp:
    def __init__(self, username, account_number):
        self.username = username
        self.account_number = account_number
        self.is_logged_in = False
        self.withdrawal_limit = 300000


    def bank_functions(self):
        updated_user_data = load_user_data()
        actionInput = ["1","2","3","4","5","6","7","0"]
        actions = format_string(input("-----------------------------------------\nWhat actions do you want to perform?\nTransfer --> PRESS 1 \nDeposit --> PRESS 2 \nWithdraw --> PRESS 3 \nDelete Account -->PRESS 4 \nDisplay account details --> PRESS 5 \nView transaction history --> PRESS 6\nUpdate personal information --> PRESS 7\nLog out -->PRESS 0\n-----------------------------------------\n"))
        while actions not in actionInput:
            print("Invalid action")
            self.bank_functions()
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
            # delete account
            self.remove_account()
        elif actions == "5":
            # display account information
            self.display_account_details()
        elif actions == "6":
            # view transaction history
            self.view_transaction_history()
        elif actions == "7":
            # update personal information
            self.update_personal_details()
        elif actions == "0":
            # logout
            self.logout()
        else:
            print("Invalid action")


    def update_personal_details(self):
        updated_user_data = load_user_data()
        print("-----------------------------------------\nUPDATE PERSONAL INFORMATION\n-----------------------------------------\n")
        print(f"-----------------------------------------\nHere are your account details\nUsername:{self.username}\nEmail Address:{updated_user_data[self.username]["email_address"]}\n-----------------------------------------\n")

        while True:
            try:
                details_to_update = format_string(input("To update username PRESS 1\nTo update email address PRESS 2\nTo update password PRESS 3\nTo increase transaction limit PRESS 4\nTo go back PRESS 0\n: "))
                if details_to_update == "1":
                    change_username()
                    break
                elif details_to_update == "2":
                    change_email_address(self.username)
                    break
                elif details_to_update == "3":
                    change_password()
                    break
                elif details_to_update == "4":
                    update_transaction_limit(self.username)
                    break
                elif details_to_update == "0":
                    break
                else:
                    print("Invalid input, Try again")
            except ValueError:
                print("Invalid field.")
        if details_to_update == "0":
            self.bank_functions()

        timer_countdown = 5

        while timer_countdown != 0:
            print(f"You will be logged out in {timer_countdown} seconds")
            timer_countdown -=1
            time.sleep(1)
        self.logout()




    # logout
    def logout(self):
        self.is_logged_in = False
        exit()

    # display account details
    def display_account_details(self):
        updated_user_data = load_user_data()
        print(f"-----------------------------------------\nHere are your account details\nUsername:{self.username}\nAccount Number: {self.account_number}\nAccount Balance: {updated_user_data[self.username]["account_balance"]}\n-----------------------------------------\n")
        self.bank_functions()

    # transfer money to another user
    def transfer(self):
        updated_user_data = load_user_data()
        username_to_transfer = format_string(input("-----------------------------------------\nEnter the username you want to transfer to: "))
        time.sleep(3)
        # username does not exist
        while username_to_transfer not in updated_user_data:
            print("Username does not exist, try again")
            username_to_transfer = format_string(
                input("-----------------------------------------\nEnter the username you want to transfer to: "))
            time.sleep(3)

        account_number_to_transfer = format_string(input("-----------------------------------------\nEnter the recipient's account number: "))
        time.sleep(3)

        # Account number invalid
        while account_number_to_transfer != updated_user_data[username_to_transfer]["account_number"]:
            print("Account number invalid")
            account_number_to_transfer = format_string(
                input("-----------------------------------------\nEnter the recipient's account number: "))
            time.sleep(3)


        # Account number found
        if username_to_transfer in updated_user_data and account_number_to_transfer == updated_user_data[username_to_transfer]["account_number"]:
            print(f"Account Found\n{updated_user_data[username_to_transfer]["username"].upper()}")

            while True:
                try:
                    amount = int(input("-----------------------------------------\nEnter amount to transfer: "))
                    time.sleep(3)

                    transaction_limit = updated_user_data[self.username]["transaction_limit"]

                    while amount > transaction_limit:
                        print("Amount is greater than transaction limit. Try again")
                        amount = int(input("-----------------------------------------\nEnter amount to transfer: "))
                        time.sleep(3)


                    transaction_pin = int(getpass("Enter transaction pin: "))
                    time.sleep(1);print(".")
                    time.sleep(1);print("..")
                    time.sleep(1);print("...")
                    print("loading...")
                    time.sleep(5)
                    while len(str(transaction_pin)) != 4 | transaction_pin != updated_user_data[self.username][
                        "transaction_pin"]:
                        print("Invalid pin, Try again")
                        transaction_pin = int(getpass("Enter transaction pin: "))
                        time.sleep(1);print(".")
                        time.sleep(1);print("..")
                        time.sleep(1);print("...")
                        print("loading...")
                        time.sleep(5)

                    # if balance is sufficient
                    if updated_user_data[self.username]["account_balance"] > amount:
                        updated_user_data[username_to_transfer]["account_balance"] += amount
                        updated_user_data[self.username]["account_balance"] -= amount
                        get_users.save_user_data(updated_user_data)
                        current_date = dt.datetime.now().isoformat()

                        # save transaction to transaction history
                        save_transaction(self.username, username_to_transfer, amount, current_date, "transfer")
                        time.sleep(1);print(".")
                        time.sleep(1);print("..")
                        time.sleep(1);print("...")
                        print("loading...")
                        time.sleep(5)
                        print(
                            f"You have successfully transferred {amount} to {username_to_transfer}\nYour current balance is: {updated_user_data[self.username]["account_balance"]}")
                        break
                    else:
                        print("Insufficient Funds")
                except ValueError:
                    print("Incorrect format for amount. Try again")
        else:
            print("username or account number incorrect")


    # view transaction history
    def view_transaction_history(self):
        updated_user_data = load_user_data()
        time.sleep(1);print(".")
        time.sleep(1);print("..")
        time.sleep(1);print("...")
        print("loading...")
        time.sleep(5)
        transaction_history = updated_user_data[self.username]["transaction_history"]
        for item in transaction_history:
            # print(item["user"])
            print("---------------------------------")
            if item["transaction_method"] == "transfer":
                if item["type"] == "debit":
                    print(f"Recipient: {item["user"]}")
                if item["type"] == "credit":
                    print(f"Sender: {item["user"]}")
            elif item["transaction_method"] == "deposit":
                print(f"Deposit: {item["user"]}")

            elif item["transaction_method"] == "withdrawal":
                print(f"Withdrawal: {item["user"]}")
            print(f"Amount: {item["amount"]}")
            # print(f"Date: {dt.datetime.strptime(item["date"],'%c').date()}")
            print("---------------------------------")
        self.bank_functions()


    # delete account
    def remove_account(self):
        account_remove_warning = format_string(input("WARNING! THIS ACTION IS IRREVERSIBLE, Do you still want to continue? (yes/no): "))
        time.sleep(1);print(".")
        time.sleep(1);print("..")
        time.sleep(1);print("...")
        print("please wait...")
        time.sleep(9)
        if account_remove_warning == "yes":
            user_data.pop(self.username)
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
        global deposit
        updated_user_data = load_user_data()

        while True:
            while True:
                try:
                    deposit = int(
                        input(
                            "-----------------------------------------\nPlease enter the amount you want to deposit: "))
                    time.sleep(1);print(".")
                    time.sleep(1);print("..")
                    time.sleep(1);print("...")
                    print("loading...")
                    time.sleep(5)
                    break

                except ValueError:
                    print("Please enter a valid numeric amount.\n")
                    print("")


            # if the deposit amount is greater than 0
            if deposit > 0:
                updated_user_data[self.username]["account_balance"] += deposit
                # user_data[self.username]["account_balance"] = self.balance
                new_user_data = updated_user_data

                # save the updated balance to the users details in the json file
                get_users.save_user_data(new_user_data)
                current_date = dt.datetime.now().isoformat()
                save_transaction(self.username, recipient="", amount=deposit, current_date=current_date,
                                 transaction_method="deposit")
                time.sleep(1);print(".")
                time.sleep(1);print("..")
                time.sleep(1);print("...")
                print("loading...")
                time.sleep(5)
                msg = f"-----------------------------------------\nDeposit of {deposit} successful!\nYour Balance is now {user_data[self.username]["account_balance"]}\n-----------------------------------------\n"
                print(msg)

                while True:
                    is_continue = input("Do you still want to deposit? ")
                    if format_string(is_continue) == "yes":

                        # deposit = int(input("Please enter the amount you want to deposit: "))
                        while True:
                            try:
                                deposit = int(
                                    input(
                                        "-----------------------------------------\nPlease enter the amount you want to deposit: "))
                                break

                            except ValueError:
                                print("Please enter a valid numeric amount.\n")
                                print("")

                        # self.balance += deposit
                        user_data[self.username]["account_balance"] += deposit
                        new_user_data = user_data
                        get_users.save_user_data(new_user_data)
                        current_date = dt.datetime.now().isoformat()
                        save_transaction(self.username, recipient=None, amount=deposit, current_date=current_date,
                                         transaction_method="deposit")
                        msg = f"Deposit of {deposit} successful!\nYour current balance is now {user_data[self.username]["account_balance"]}"
                        print("-----------------------------------------")
                        print(msg)
                        print("-----------------------------------------\n")
                    elif format_string(is_continue) == "no":
                        break
            break

        # go back to the bank menu
        self.bank_functions()

    # withdraw money
    def withdraw(self):
        updated_user_data = load_user_data()
        while True:
            try:
                withdrawal_amount = int(format_string(input("-----------------------------------------\nEnter the amount you want to withdraw: ")))

                # withdrawal limit enforced
                while withdrawal_amount > self.withdrawal_limit:
                    print("Withdrawal Failed!. Amount is greater than the withdrawal limit. Increase limit to continue")
                    withdrawal_amount = int(format_string(input("-----------------------------------------\nEnter the amount you want to withdraw: ")))

                # insufficient funds
                if withdrawal_amount > updated_user_data[self.username]["account_balance"]:
                    print("Insufficient funds")
                    withdrawal_amount = int(format_string(
                        input("-----------------------------------------\nEnter the amount you want to withdraw: ")))
                else:
                    # proceed
                    break
            except ValueError:
                print("Please enter a valid numeric amount.")

        # if updated_user_data[self.username]["account_balance"] < withdrawal_amount:
        #     print("Insufficient funds")
        # else:
            # self.balance -= withdrawal_amount
        while True:
            transaction_pin = int(getpass("Enter transaction pin: "))
            try:
                if transaction_pin != updated_user_data[self.username]["transaction_pin"]:
                    print("Invalid transaction pin")
                else:
                    break
            except ValueError:
                print("Please enter a valid numeric amount.")

        updated_user_data[self.username]["account_balance"] -=withdrawal_amount
        current_date = dt.datetime.now().isoformat()
        get_users.save_user_data(updated_user_data)
        save_transaction(self.username, recipient=None, amount=withdrawal_amount, current_date=current_date,
                         transaction_method="withdrawal")
        msg = f"-----------------------------------------\nWithdrawal successful!\nCurrent balance is: {user_data[self.username]["account_balance"]}\n-----------------------------------------"
        print(msg)
        while True:
            still_withdrawing = input("-----------------------------------------\nDo you still want to withdraw? (yes/no)")
            answer = format_string(still_withdrawing)
            if answer == "yes":
                while True:
                    try:
                        withdrawal_amount = int(
                            input("-----------------------------------------\nEnter the amount you want to withdraw: "))
                        if withdrawal_amount > updated_user_data[self.username]["account_balance"]:
                            print("Insufficient funds")
                            withdrawal_amount = int(format_string(
                                input(
                                    "-----------------------------------------\nEnter the amount you want to withdraw: ")))
                        else:
                            # proceed
                            break
                    except ValueError:
                        print(print("Please enter a valid numeric amount."))

                # transaction pin
                while True:
                    try:
                        transaction_pin = int(getpass("Enter transaction pin: "))
                        if transaction_pin != updated_user_data[self.username]["transaction_pin"]:
                            print("Invalid transaction pin")
                        else:
                            # proceed
                            break
                    except ValueError:
                        print(print("Please enter a valid numeric amount."))
                updated_user_data[self.username]["account_balance"]-=withdrawal_amount
                get_users.save_user_data(updated_user_data)
                current_date = dt.datetime.now().isoformat()
                save_transaction(self.username, recipient=None, amount=withdrawal_amount, current_date=current_date,
                                 transaction_method="withdrawal")
                msg = f"-----------------------------------------\nWithdrawal successful!\nCurrent balance is: {user_data[self.username]["account_balance"]} |\n-----------------------------------------"
                print(msg)
            elif answer == "no":
                break
            else:
                print("Input Invalid. Try again")
        # go to bank menu
        self.bank_functions()

    # check balance
    def check_balance(self):
        updated_user_data = load_user_data()
        print(f"-----------------------------------------\nYour current balance is {updated_user_data[self.username]["account_balance"]} |\n-----------------------------------------")
        self.bank_functions()


try:
    print("Welcome to the Bank App")
    is_new_user = format_string(input("Are you a new user? (yes/no): "))
    lss = ["yes","no"]
    while is_new_user not in lss:
        is_new_user = format_string(input("Are you a new user? (yes/no): "))

    if is_new_user == "yes":
        print("--------------------------\nREGISTER|\n--------------------------\n")
        register()
    elif is_new_user == "no":
        print("--------------------------\nLOGIN|\n--------------------------\n")
        login()
except KeyboardInterrupt:
    print("\nApp terminated by user")
