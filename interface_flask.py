import blockchain, block, transaction
from flask import Flask, jsonify, request
from uuid import uuid4


app = Flask(__name__)


# Generate a globally unique address for this node
node_identifiere = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchaine = blockchain.Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [block.serialize() for block in blockchaine.chain],
        'length': len(blockchaine.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug = True)
    