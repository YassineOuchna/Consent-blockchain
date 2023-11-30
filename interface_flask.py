from flask import Flask, render_template
from database_manager import contracts_database
app = Flask(__name__)

author = '1d48fc0e035779571b88a74695554540b1369561edf7dc20d7b68569ebf0db2a'


history = contracts_database().get_history(author)


@app.route('/')
def get_user_history():
    return render_template('history.html', history=history)


if __name__ == '__main__':
    app.run(debug=True)
