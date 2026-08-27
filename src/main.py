from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.models import Expense
from src.storage import load_expenses, save_expenses


app = FastAPI(
    title="Smart Expense Tracker API",
    version="1.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Add Expense
# --------------------------------------------------

@app.post("/expenses")
def add_expense(expense: Expense):

    expenses = load_expenses()

    # Prevent duplicate IDs
    for existing_expense in expenses:

        if existing_expense["id"] == expense.id:

            raise HTTPException(
                status_code=400,
                detail="Expense ID already exists"
            )

    expenses.append(
        expense.model_dump(mode="json")
    )

    save_expenses(expenses)

    return expense


# --------------------------------------------------
# Get All Expenses
# --------------------------------------------------

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


# --------------------------------------------------
# Get Single Expense
# --------------------------------------------------

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):

    expenses = load_expenses()

    for expense in expenses:

        if expense["id"] == expense_id:

            return expense

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


# --------------------------------------------------
# Update Expense
# --------------------------------------------------

@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    updated_expense: Expense
):

    expenses = load_expenses()

    for index, expense in enumerate(expenses):

        if expense["id"] == expense_id:

            updated_data = (
                updated_expense.model_dump(
                    mode="json"
                )
            )

            updated_data["id"] = expense_id

            expenses[index] = updated_data

            save_expenses(expenses)

            return updated_data

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


# --------------------------------------------------
# Delete Expense
# --------------------------------------------------

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    expenses = load_expenses()

    remaining = [
        expense
        for expense in expenses
        if expense["id"] != expense_id
    ]

    if len(remaining) == len(expenses):

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    save_expenses(remaining)

    return {
        "message": "Expense deleted successfully"
    }


# --------------------------------------------------
# Expense Summary
# --------------------------------------------------

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
            categories.get(category, 0)
            + expense["amount"]
        )

    return {
        "total": total,
        "by_category": categories
    }
