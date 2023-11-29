"""
This module contains the class Block. A block is a list of transactions. The first block is called the genesis block.
"""

import hashlib
import json
import config
import utils
from rich.console import Console
from rich.table import Table


class InvalidBlock(Exception):
    pass


class Block(object):
    def __init__(self, data=None):
        """
        If data is None, create a new genesis block. Otherwise, create a block from data (a dictionary).
        Raise InvalidBlock if the data are invalid.
        """
        if data:
            try:
                self.index = data['index']
                self.timestamp = data['timestamp']
                self.transactions = data['transactions']
                self.proof = data['proof']
                self.previous_hash = data['previous_hash']
            except Exception as e:
                raise InvalidBlock(e)
        else:
            self.index = 0
            self.timestamp = utils.get_time()
            self.transactions = []
            self.proof = 0
            self.previous_hash = "0"*64

    @property
    def block_data(self):
        block = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }
        return block

    def next(self, transactions):
        """
        Create a block following the current block
        :param transactions: a list of transactions, i.e. a list of messages and their signatures
        :return: a new block
        """
        block = Block()
        block.index = self.index+1
        block.timestamp = utils.get_time()
        block.transactions = transactions
        block.proof = self.mine()
        block.previous_hash = self.hash()
        return block

    def hash(self):
        """
        Hash the current block (SHA256). The dictionary representing the block is sorted to ensure the same hash for
        two identical block. The transactions are part of the block and are not sorted.
        :return: a string representing the hash of the block
        """
        block_string = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True).encode()
        hashe = hashlib.sha256(block_string).hexdigest()
        return hashe

    def __str__(self):
        """
        String representation of the block
        :return: str
        """
        index = self.index
        hash = self.previous_hash
        start_hash = hash[:len(hash)//6]
        finish_hash = hash[-len(hash)//6:]
        date = self.timestamp
        number_transactions = len(self.transactions)
        return str('index='+str(index)+"\n"+"hash:"+str(start_hash)+'...'+str(finish_hash)+"\n"+"time="+str(date)
                   + "\n"+"number of transactions="+str(number_transactions))

    def valid_proof(self):
        """
        Check if the proof of work is valid. The proof of work is valid if the hash of the block starts with a number
        of 0 equal to difficulty.

        If index is 0, the proof of work is valid.
        :param difficulty: the number of 0 the hash must start with
        :return: True or False
        """
        hash = self.hash()
        return (hash[:config.default_difficulty] == "0"*config.default_difficulty) or self.index == 0

    def mine(self):
        """
        Mine the current block. The block is valid if the hash of the block starts with a number of 0 equal to
        config.default_difficulty.
        :return: the proof of work
        """
        proof = 0
        self.proof = proof
        while self.valid_proof() is False:
            proof += 1
            self.proof = proof
        return proof

    def validity(self):
        """
        Check if the block is valid. A block is valid if it is a genesis block or if:
        - the proof of work is valid
        - the transactions are valid
        - the number of transactions is in [0, config.blocksize]
        :return: True or False
        """
        # res= (self.inex==0) or (self.valid_proof() and res_trans and (len(self.transactions)<=config.blocksize) )
        # res_trans
        # for transaction in self.transactions:
        #     if not transaction.verify():
        #         res_trans=False
        #         break
        if self.transactions == []:
            return True
        else:
            if not self.valid_proof():
                return False
            elif len(self.transactions) not in range(0, config.blocksize + 1):
                return False
            else:
                for transaction in self.transactions:
                    if not transaction.verify():
                        return False
            return True

    def log(self):
        """
        A nice log of the block
        :return: None
        """
        table = Table(
            title=f"Block #{self.index} -- {self.hash()[:7]}...{self.hash()[-7:]} -> {self.previous_hash[:7]}...{self.previous_hash[-7:]}")
        table.add_column("Author", justify="right", style="cyan")
        table.add_column("Message", style="magenta", min_width=30)
        table.add_column("Date", justify="center", style="green")

        for t in self.transactions:
            table.add_row(t.author[:7] + "..." +
                          t.author[-7:], t.message, t.date[:-7])

        console = Console()
        console.print(table)


def test():
    from ecdsa import SigningKey
    from transaction import Transaction
    sk = SigningKey.generate()
    transactions = [Transaction(f"Message {i}") for i in range(10)]
    for t in transactions:
        t.sign(sk)

    Transaction.log(transactions)

    blocks = [Block()]
    for i in range(5):
        blocks.append(blocks[-1].next(transactions[i * 2:(i + 1) * 2]))
        blocks[-1].mine()

    for b in blocks:
        b.log()


if __name__ == '__main__':
    print("Test Block")
    test()
