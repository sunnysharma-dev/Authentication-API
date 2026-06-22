<<<<<<< HEAD
from fastapi import FastAPI
import bcrypt
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Authentication API"}

import sqlite3

conn = sqlite3.connect(
    "auth.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    password TEXT           
)
""")

conn.commit() 

@app.post("/users")
def user_register(username:str,email:str,password:str):
    password_bytes = password.encode()

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    cursor.execute(
        "INSERT INTO users (username,email,password) VALUES (?,?,?)",
        (username, email, hashed_password)
    )

    conn.commit()
    return {
        "message": "user registered",
        "username": username,
        "email": email,
    }

@app.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return rows

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()

    return {
        "message": "user deleted",
        "id": user_id
    }    

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    username: str,
    email: str
):
    cursor.execute(
        """
        UPDATE users
        SET username = ?, email = ?
        WHERE id = ?
        """,
        (username, email, user_id)
    )

    conn.commit()

    return {
        "message": "user updated",
        "id": user_id
    }

@app.post("/login")
def user_login(email: str, password: str):

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    if user:

        password_matches = bcrypt.checkpw(
            password.encode(),
            user[3]
        )

        if password_matches:
            return {"message": "Login successful"}

    return {"message": "Invalid email or password"}



    
    

=======
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Expense Tracker API"}

import sqlite3

conn = sqlite3.connect(
    "expense.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    title TEXT,
    amount REAL
)
""")

conn.commit()

@app.post("/expense")
def add_expense(title: str, amount: float):
    cursor.execute(
        "INSERT INTO expenses (title, amount) VALUES (?, ?)",
        (title, amount)
    )
    conn.commit()

    return {
        "message": "Expense added",
        "title": title,
        "amount": amount
    }

@app.get("/expenses")
def get_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    return rows

@app.delete("/expense/{expense_id}")
def delete_expense(expense_id: int):
    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    return {
        "message": "Expense deleted",
        "id": expense_id
    }    

@app.put("/expense/{expense_id}")
def update_expense(
    expense_id: int,
    title: str,
    amount: float
):
    cursor.execute(
        """
        UPDATE expenses
        SET title = ?, amount = ?
        WHERE id = ?
        """,
        (title, amount, expense_id)
    )

    conn.commit()

    return {
        "message": "Expense updated",
        "id": expense_id
    }
>>>>>>> 8cc67238680e08b52cbdb29985e1684af417c395
