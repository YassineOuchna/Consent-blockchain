import blockchain, block, transaction
from flask import Flask, jsonify, request, render_template, redirect, url_for
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import check_password_hash, generate_password_hash




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/login/user', methods=['POST'])
def login():
    username = request.form['uname']
    password = request.form['psw']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.hashed_password, password):
        return redirect(url_for('success'))
    else:
        return "Invalid username or password"
    

@app.route('/success')
def success():
    return "Login successful!"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose another username."
        
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index')) 

    return render_template('register.html')

@app.route('/users')
def users_list():
    users = User.query.all()
    return render_template('users_list.html', users=users)



if __name__ == '__main__':
    app.run(debug = True)
    