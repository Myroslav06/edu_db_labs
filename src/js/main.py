from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "qwerty",
    "database": "mydb"
}

# --- Моделі ---

class UserBase(BaseModel):
    email: str
    last_name: str | None = None
    first_name: str | None = None
    role_id: int

class User(UserBase):
    id: int

class QuizBase(BaseModel):
    title: str
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    status: str | None = None
    category_id: int

class Quiz(QuizBase):
    id: int

# --- User endpoints ---

@app.get("/users", response_model=list[User])
def get_users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.post("/users", response_model=User)
def create_user(user: UserBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO User (email, last_name, first_name, role_id)
        VALUES (%s, %s, %s, %s)
    """, (user.email, user.last_name, user.first_name, user.role_id))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {**user.dict(), "id": user_id}

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE id = %s", (user_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="User not found")
    cursor.execute("""
        UPDATE User SET email=%s, last_name=%s, first_name=%s, role_id=%s WHERE id=%s
    """, (user.email, user.last_name, user.first_name, user.role_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE id = %s", (user_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="User not found")
    cursor.execute("DELETE FROM User WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User deleted successfully"}

# --- Quiz endpoints ---

@app.get("/quizzes", response_model=list[Quiz])
def get_quizzes():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Quiz")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.post("/quizzes", response_model=Quiz)
def create_quiz(quiz: QuizBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Quiz (title, description, start_date, end_date, status, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (quiz.title, quiz.description, quiz.start_date, quiz.end_date, quiz.status, quiz.category_id))
    conn.commit()
    quiz_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {**quiz.dict(), "id": quiz_id}

@app.put("/quizzes/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: int, quiz: QuizBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Quiz WHERE id = %s", (quiz_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    cursor.execute("""
        UPDATE Quiz SET title=%s, description=%s, start_date=%s, end_date=%s, status=%s, category_id=%s
        WHERE id=%s
    """, (quiz.title, quiz.description, quiz.start_date, quiz.end_date, quiz.status, quiz.category_id, quiz_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {**quiz.dict(), "id": quiz_id}

@app.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Quiz WHERE id = %s", (quiz_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    cursor.execute("DELETE FROM Quiz WHERE id = %s", (quiz_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Quiz deleted successfully"}
