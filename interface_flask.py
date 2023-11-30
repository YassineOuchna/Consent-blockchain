import blockchain, block, transaction
from flask import Flask, jsonify, request, render_template
from uuid import uuid4


app = Flask(__name__)


# Generate a globally unique address for this node
node_identifiere = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchaine = blockchain.Blockchain()

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

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
        'chain': [block.block_data for block in blockchaine.chain],
        'length': len(blockchaine.chain),
    }
    return jsonify(response), 200




@app.route('/create_contract')
def contract():
    return render_template('create_contract.html')

# Route to handle form submission and create the contract
@app.route('/create_contract', methods=['POST'])
def create_contract():
    # Get form inputs
    client_name = request.form['client_name']
    service_description = request.form['service_description']
    payment_amount = request.form['payment_amount']
    
    # Here, you can create the contract using the inputs
    # For simplicity, let's just format the contract as a string
    contract = f"Contract\nClient: {client_name}\nDescription of Service: {service_description}\nPayment: ${payment_amount}"
    
    # You can then save this contract to a file or database, or perform any other actions needed
    
    return contract









if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    