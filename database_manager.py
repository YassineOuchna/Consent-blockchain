import sqlite3 as sq
from transaction import Transaction

conn = sq.connect('database.db', check_same_thread=False)
cur = conn.cursor()


class contracts_database():
    def __init__(self):
        cur.execute(
            "CREATE TABLE IF NOT EXISTS contracts(contract_id TEXT NOT NULL, author, date date, signature, content)")
        conn.commit()

    def add_contract(self, contract : Transaction):  # takes in a transaction object
        data = contract.data
        contract_id = contract.hash()
        cur.execute(
            f"INSERT INTO contracts VALUES ('{contract_id}', '{data['author']}', '{data['date']}','{contract.signature}', '{data['message']}')")
        conn.commit()

    def get_contract(self, id):
        r = cur.execute(
            f"SELECT contract_id, author, date, signature, content FROM contracts WHERE contract_id='{id}'").fetchone()
        data = {
            "contract_id": r[0],
            "author": r[1],
            "date": r[2],
            "signature": r[3],
            "content": r[4]
        }
        conn.commit()
        return data

    def get_history(self, author):
        r = cur.execute(
            f"SELECT contract_id, author, date, signature, content FROM contracts WHERE author='{author}'").fetchall()
        history = [self.get_contract(contract[0]) for contract in r]
        return history


class users():
    def __init__(self):
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users(id, hashed_password)")
        conn.commit()

    def add_user(self, id, hashed_p):
        cur.execute(
            f"INSERT INTO contracts VALUES ('{id}', '{hashed_p}')")
        conn.commit()

    def get_user(self, id):
        try:
            r = cur.execute(
                f"SELECT id, hashed_password FROM users WHERE id='{id}'").fetchall()
            conn.commit()
            if r is None:
                raise Exception("User not found")
        except Exception as e:
            print("An error occurred:", e)
        return r
