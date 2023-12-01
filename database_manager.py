import sqlite3 as sq

conn = sq.connect('database.db', check_same_thread=False)
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


class blockchain_database():
    def __init__(self):
        cur.execute(
            "CREATE TABLE IF NOT EXISTS blockchain(index_block, proof, date date, transaction_id TEXT NOT NULL, previous_hash)")
        conn.commit()

    def add_block(self, block):  # takes in a transaction object
        data = block.block_data
        for contract in data['transactions']:
            cur.execute(
                f"INSERT INTO blockchain VALUES ('{data['index']}', '{data['proof']}', '{data['timestamp']}','{contract.hash()}', '{data['previous_hash']}')")
            conn.commit()

    def get_block(self, index_block):
        b = cur.execute(
            f"SELECT index_block, proof, date, transaction_id, previous_hash FROM blockchain WHERE index_block='{index_block}'").fetchall()
        data = []
        for r in b:
            data.append({
                "index_block": r[0],
                "proof": r[1],
                "date": r[2],
                "transaction_id": r[3],
                "previous_hash": r[4]
            })
        conn.commit()
        return data  # returns list of contracts in a single block of index_block index

    def get_blockchain(self):
        r = cur.execute(
            f"SELECT index_block, proof, date, transaction_id, previous_hash FROM blockchain").fetchall()
        num_blocks = cur.execute(
            f'SELECT COUNT(DISTINCT index_block) as num_orders FROM blockchain').fetchone()[0]
        history = [self.get_block(index_block)
                   for index_block in range(1, num_blocks+1)]
        return history
