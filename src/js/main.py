from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Конфігурація підключення до MySQL
db_config = {
    "host": "localhost",
    "user": "api_user",
    "password": "secure_pass123",
    "database": "mydb",
    "charset": "utf8mb4"
}

# Функція, що створює з'єднання через PyMySQL
def get_connection():
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        charset=db_config["charset"],
        cursorclass=pymysql.cursors.DictCursor  # щоб fetchall() повертав список словників
    )

# --- Pydantic-моделі ---

class UserBase(BaseModel):
    id: int
    email: str
    last_name: str | None = None
    first_name: str | None = None
    role_id: int

class User(UserBase):
    pass

class QuizBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    start_date: str | None = None    # формат "YYYY-MM-DD"
    end_date: str | None = None      # формат "YYYY-MM-DD"
    status: str | None = None
    category_id: int

class Quiz(QuizBase):
    pass

# --- User endpoints ---

@app.get("/users", response_model=list[User])
def get_users():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            rows = cursor.fetchall()  # список dict-об’єктів
        return rows
    finally:
        conn.close()

@app.post("/users", response_model=User)
def create_user(user: UserBase):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Перевіряємо, чи такий ID вже є
            cursor.execute("SELECT id FROM User WHERE id = %s", (user.id,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="User with this ID already exists")
            # Якщо немає, вставляємо
            cursor.execute(
                "INSERT INTO User (id, email, last_name, first_name, role_id) VALUES (%s, %s, %s, %s, %s)",
                (user.id, user.email, user.last_name, user.first_name, user.role_id)
            )
            conn.commit()
        return user.dict()
    except HTTPException:
        # Якщо ми свідомо кинули HTTPException (наприклад, дублікат ID) – прокинемо далі
        raise
    except Exception as e:
        # Інші помилки (наприклад, некоректні колонки, відсутність таблиці тощо)
        # Повертаємо чистий текст помилки з кодом 500
        return HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserBase):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE id = %s", (user_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="User not found")
            cursor.execute(
                "UPDATE User SET email=%s, last_name=%s, first_name=%s, role_id=%s WHERE id=%s",
                (user.email, user.last_name, user.first_name, user.role_id, user_id)
            )
            conn.commit()
        return {**user.dict(), "id": user_id}
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE id = %s", (user_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="User not found")
            cursor.execute("DELETE FROM User WHERE id = %s", (user_id,))
            conn.commit()
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# --- Quiz endpoints ---

@app.get("/quizzes", response_model=list[Quiz])
def get_quizzes():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Quiz")
            rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

@app.post("/quizzes", response_model=Quiz)
def create_quiz(quiz: QuizBase):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Перевіряємо, чи такий ID вже є
            cursor.execute("SELECT id FROM Quiz WHERE id = %s", (quiz.id,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Quiz with this ID already exists")
            # Якщо немає, вставляємо
            cursor.execute(
                "INSERT INTO Quiz (id, title, description, start_date, end_date, status, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (quiz.id, quiz.title, quiz.description, quiz.start_date, quiz.end_date, quiz.status, quiz.category_id)
            )
            conn.commit()
        return quiz.dict()
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/quizzes/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: int, quiz: QuizBase):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Quiz WHERE id = %s", (quiz_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Quiz not found")
            cursor.execute(
                "UPDATE Quiz SET title=%s, description=%s, start_date=%s, end_date=%s, status=%s, category_id=%s WHERE id=%s",
                (quiz.title, quiz.description, quiz.start_date, quiz.end_date, quiz.status, quiz.category_id, quiz_id)
            )
            conn.commit()
        return {**quiz.dict(), "id": quiz_id}
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Quiz WHERE id = %s", (quiz_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Quiz not found")
            cursor.execute("DELETE FROM Quiz WHERE id = %s", (quiz_id,))
            conn.commit()
        return {"message": "Quiz deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
