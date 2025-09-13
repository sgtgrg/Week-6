import sqlite3
import time
from datetime import datetime

class DatabaseConnection:
    def __init__(self, db_name="app.db"):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class UserService:
    def get_user(self, user_id):
        start_time = time.time()
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
        elapsed_time = time.time() - start_time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] UserService.get_user executed in {elapsed_time:.6f} seconds")
        return result


class OrderService:
    def get_order(self, order_id):
        start_time = time.time()
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            result = cursor.fetchone()
        elapsed_time = time.time() - start_time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] OrderService.get_order executed in {elapsed_time:.6f} seconds")
        return result


def initialize_db():
    with DatabaseConnection() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS orders")

        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, item TEXT)")

        cursor.execute("INSERT INTO users (name) VALUES ('Zoro')")
        cursor.execute("INSERT INTO orders (item) VALUES ('Monitor')")


def main():
    initialize_db()

    user_service = UserService()
    order_service = OrderService()

    user = user_service.get_user(1)
    order = order_service.get_order(1)

    print("User:", user)
    print("Order:", order)


if __name__ == "__main__":
    main()
