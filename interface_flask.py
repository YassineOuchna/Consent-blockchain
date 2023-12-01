import blockchain, block
from flask import Flask, jsonify, request, render_template, send_file, redirect, url_for
from uuid import uuid4
from ecdsa import SigningKey, NIST192p
from database_manager import contracts_database, blockchain_database
from PIL import Image, ImageDraw, ImageFont
import io
import datetime
import base64
from transaction import Transaction
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from reportlab.pdfgen import canvas

author=''

app = Flask(__name__)
cd = contracts_database()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    signing_key = db.Column(db.String(100), unique=True, nullable=False)


# Generate a globally unique address for this node
node_identifiere = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchaine = blockchain.Blockchain()

blockch = blockchain.Blockchain()
blockch_database = blockchain_database()




name = ""

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/login')
def connect():
    return render_template('login.html')



@app.route('/login/user', methods=['POST'])
def login():
    username = request.form['uname']
    password = request.form['psw']

    user = User.query.filter_by(username=username).first()
    global author 
    author = user.signing_key
    if user and check_password_hash(user.hashed_password, password):
        global name
        name = username
        return render_template('home.html' , username=username)
    else:
        return "Invalid username or password"
    
@app.route('/logout')
def logout():
    global name
    name = ""

    return render_template('logout.html')





@app.route('/success')
def success():
    return "Login successful!"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sk = SigningKey.generate()
        sk = sk.to_string()
        sk = sk.hex()  # Convert binary to hexadecimal text
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose another username."
        
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, hashed_password=hashed_password, signing_key=sk)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('connect')) 

    return render_template('register.html')






@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/Create_contract')
def create_contract():
    return render_template('create_contract.html')


@app.route('/create_contract', methods=['POST'])
def create():
    if request.method == 'POST':
        # Get form inputs
        service_description = request.form['service_description']


        # Here, you can create the contract using the inputs
        # For simplicity, let's just format the contract as a string
        contract = f"Description of Service : {service_description}"
        # You can then save this contract to a file or database, or perform any other actions needed
        # And now we'll add the transaction in our database
        sk = bytes.fromhex(author)
        sk = SigningKey.from_string(sk, curve=NIST192p)
        tr = Transaction(contract)
        tr.author = author
        cd.add_contract(tr)
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Create an image with PIL
        img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Set margins and starting positions for content
        margin = 50
        start_position = 100

        # Write content to the image in a contract-like format
        contract_content = [
            f"SERVICE DESCRIPTION: {service_description}",
            f"DATE: {current_date}"
        ]

        for content in contract_content:
            draw.text((margin, start_position), content, fill=(0, 0, 0), font=font)
            start_position += 50  # Adjust spacing between lines

        # Save the image to a byte buffer as PNG format
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        img_base64 = base64.b64encode(img_byte_array.read()).decode('utf-8')
        return redirect(url_for('contract_display', contract_image=img_base64))
    return "Something went wrong."

#display the contract image
@app.route('/contract_display')
def contract_display():
    contract_image = request.args.get('contract_image')
    return render_template('contract_display.html', contract_image=contract_image)


@app.route('/Contact')
def contact():
    return render_template('contact.html')



@app.route('/blockchain', methods=['GET'])
def full_chain():
    blocks = []
    full_blockchain = blockch_database.get_blockchain()
    for block in full_blockchain:
        # Convert rich table to a list of dictionaries
        block_ = {}
        block_['title'] = 'Block' + block[0]['index_block']
        data = []
        for transaction in block:
            del transaction['index_block']
            data.append(transaction)
        block_['data'] = data
        blocks.append(block_)

    return render_template('blockchain.html', blocks=blocks)


history = cd.get_history(author)

@app.route('/history')
def get_user_history(): 
    
    return render_template('history.html', history=history)


@app.route('/generate_pdf/<string:contract_id>')
def generate_pdf(contract_id):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    contract = cd.get_contract(contract_id)
    pdf.drawString(50, 820, f"Date :  {contract['date']}")
    pdf.drawString(50, 800, f"Contract Id : {contract['contract_id']}")
    pdf.drawString(50, 780, f"Author :  {contract['author']}")
    pdf.drawString(50, 700, f"{contract['content']}")
    pdf.drawString(50, 100, "Signature : ")
    pdf.drawString(50, 75, f"{contract['signature'][:64]}")
    pdf.drawString(50, 50, f"{contract['signature'][64:128]}")
    pdf.drawString(50, 25, f"{contract['signature'][128:]}")
    pdf.save()

    # Move the buffer's pointer to the beginning
    buffer.seek(0)

    # Return the generated PDF file to the user for download
    return send_file(buffer, as_attachment=True, download_name=f"contract_{contract['contract_id']}.pdf")





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    