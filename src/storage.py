import json
import os


FILE = "expenses.json"


def load_expenses():

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as file:
        return json.load(file)


def save_expenses(expenses):

    with open(FILE, "w") as file:

        json.dump(
            expenses,
            file,
            indent=4,
            default=str
        )
