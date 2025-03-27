import json
import os
USER_DATA_FILE = "user_data.json"
# dictionary = {}
# dictionary["sammy"] = {"password":12345}
# # dictionary["password"] = "12345678"
#
# print(dictionary)

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_user_data(user_data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_data, file)

