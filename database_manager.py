import sqlite3 as sq

conn = sq.connect('database.db')
cur = conn.cursor()


class contracts_database():
    def __init__(self):
        cur.execute(
            "CREATE TABLE IF NOT EXISTS contracts(contract_id TEXT NOT NULL, author, date date, signature, content)")
        conn.commit()

    def add_contract(self, contract):  # takes in a transaction object
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
