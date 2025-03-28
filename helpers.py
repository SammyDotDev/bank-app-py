import random
from get_users import load_user_data, save_user_data
from typing import List, Dict, Any
import datetime

# user_data = load_user_data()
# user_details = Dict[str, str | int | datetime | List[Dict[str, str | int]]]
user_data: Dict[str, Dict[str, Any]] = load_user_data()


def format_string(text: str):
    return text.strip().lower()

def generate_random_account_number():
    account_number = ""
    for i in range(10):
        account_number+= str(random.randint(0,9))
    return account_number

def save_transaction(sender, recipient, amount:int, current_date:str):
    user_datar: Dict[str, Dict[str, Any]] = load_user_data()
    user_datar[recipient]["transaction_history"] = []
    print(user_datar,"USER DATAR")

    sender_transaction_item = {
        "user": recipient,
        "amount": amount,
        "date": current_date,
        "type":"out"
    }
    recipient_transaction_item = {
        "user": sender,
        "amount": amount,
        "date": current_date,
        "type":"in"
    }
    # user_data.setdefault(recipient, {}).setdefault("transaction_history", [])
    user_datar[recipient]["transaction_history"].append(recipient_transaction_item)
    save_user_data(user_datar)
    user_datar[sender]["transaction_history"].append(sender_transaction_item)
    save_user_data(user_datar)