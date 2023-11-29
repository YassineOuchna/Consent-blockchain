from utils import get_time, str_to_time
from datetime import datetime
import config
import random
from transaction import Transaction
from block import Block


class Blockchain():
    def __init__(self):
        self.chain = [Block()]
        self.mempool = []

    def __str__(self):
        return str([str(block) for block in self.chain])

    def __len__(self):
        return len(self.chain)

    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if transaction not in self.mempool and str_to_time(transaction.date) < str_to_time(get_time()) and transaction.signature and transaction.verify():
            self.mempool.append(transaction)
            return True
        return False

    def new_block(self, block=None):
        newblock = Block()
        if block is None:
            newblock.index = self.chain[-1].index + 1
            newblock.timestamp = get_time()
            newblock.proof = 0
            newblock.previous_hash = self.chain[-1].hash()
        else:
            newblock.index = block.index + 1
            newblock.timestamp = get_time()
            newblock.proof = 0
            newblock.previous_hash = block.hash()

        n = len(self.mempool)
        for k in range(min(config.blocksize, n)):
            i = random.randint(0, len(self.mempool)-1)
            newblock.transactions.append(self.mempool[i])
            self.mempool.pop(i)

        return newblock

    def extend_chain(self, block):

        if block.index == self.chain[-1].index + 1 and block.previous_hash == self.chain[-1].hash() and block.valid_proof():
            self.chain.append(block)

        else:
            raise TypeError("InvalidBlock")

    def validity(self):
        if self.chain[0] != Block():
            return False
        for block in self.chain:
            if not block.validity:
                return False
        for block in self.chain[1:]:
            current_index = block.index
            for sub_block in self.chain:
                if sub_block.index == current_index + 1:
                    if sub_block.previous_hash != block.hash:
                        return False
        transactions_union = self.mempool
        for block in self.chain:
            for transaction in block.transactions:
                transactions_union.append(transaction)

        if transactions_union != list(set(transactions_union)):
            return False

        return True

    def merge(self, other):
        if len(other.chain) > len(self.chain):
            j = 0
            for index in range(len(self.chain)):
                if self.chain[index].hash != other.chain[index].hash:
                    j = index
                    break
            L = other.mempool.copy()
            for k in range(j, len(self.chain)):
                for transaction in self.chain[k].transactions:
                    if not transaction in L:
                        L.append(transaction)
            for transaction in self.mempool:
                if not transaction in L:
                    L.append(transaction)
            self.chain = other.chain[:]
            self.mempool = L
        else:
            j = 0
            for index in range(len(other.chain)):
                if other.chain[index].hash != self.chain[index].hash:
                    j = index
                    break
            for k in range(j, len(other.chain)):
                for transaction in other.chain[k].transactions:
                    self.add_transaction(transaction)

    def log(self):
        print(self)
        Transaction.log(self.mempool)

        for b in self.chain:
            b.log()


def merge_test():
    from ecdsa import SigningKey
    blockchain = Blockchain()
    sk = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk)
        blockchain.add_transaction(t)

    blockchain2 = Blockchain()
    sk2 = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk2)
        blockchain2.add_transaction(t)

    for i in range(3):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    for i in range(2):
        b = blockchain2.new_block()
        b.mine()
        blockchain2.extend_chain(b)

    blockchain.merge(blockchain2)
    blockchain2.merge(blockchain)

    for i in range(2):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    for i in range(4):
        b = blockchain2.new_block()
        b.mine()
        blockchain2.extend_chain(b)

    blockchain.merge(blockchain2)
    blockchain2.merge(blockchain)

    blockchain.log()


def simple_test():
    from ecdsa import SigningKey
    blockchain = Blockchain()
    sk = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk)
        blockchain.add_transaction(t)

    print(blockchain)
    for i in range(3):
        b = blockchain.new_block()
        b.mine()
        print(b)
        print(blockchain.chain[0].hash())
        blockchain.extend_chain(b)

    print(blockchain)
    print(b.validity())
    print(len(blockchain))


if __name__ == '__main__':
    print("Blockchain test")
    simple_test()
    merge_test()