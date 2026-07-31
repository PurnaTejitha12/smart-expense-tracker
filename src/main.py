from fastapi import FastAPI, HTTPException, Query
from src.models import Expense
from src.storage import load_expenses, save_expenses


app = FastAPI(
    title="Smart Expense Tracker API",
    version="1.0"
)



@app.post("/expenses")
def add_expense(expense: Expense):

    expenses = load_expenses()

    expenses.append(
        expense.model_dump()
    )

    save_expenses(expenses)

    return expense



@app.get("/expenses")
def get_expenses(
    category: str | None = Query(None)
):

    expenses = load_expenses()

    if category:

        expenses = [
            expense
            for expense in expenses
            if expense["category"].lower()
            == category.lower()
        ]

    return expenses



@app.get("/expenses/summary")
def summary():

    expenses = load_expenses()

    total = sum(
        expense["amount"]
        for expense in expenses
    )

    categories = {}

    for expense in expenses:

        category = expense["category"]

        categories[category] = (
            categories.get(category,0)
            +
            expense["amount"]
        )


    return {
        "total": total,
        "by_category": categories
    }




@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id:int):

    expenses = load_expenses()


    remaining = [
        expense
        for expense in expenses
        if expense["id"] != expense_id
    ]


    if len(remaining)==len(expenses):

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )


    save_expenses(remaining)


    return {
        "message":"Expense deleted"
    }