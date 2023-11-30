from flask import Flask, render_template, send_file
from database_manager import contracts_database
from reportlab.pdfgen import canvas
import io
import json
app = Flask(__name__)

author = '1d48fc0e035779571b88a74695554540b1369561edf7dc20d7b68569ebf0db2a'

cont_database = contracts_database()
history = cont_database.get_history(author)


@app.route('/')
def get_user_history():
    return render_template('history.html', history=history)


@app.route('/generate_pdf/<string:contract_id>')
def generate_pdf(contract_id):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    contract = cont_database.get_contract(contract_id)
    pdf.drawString(50, 820, f"Date :  {contract['date']}")
    pdf.drawString(50, 800, f"Contract Id : {contract['contract_id']}")
    pdf.drawString(50, 780, f"Author :  {contract['author']}")
    pdf.drawString(50, 700, f"{contract['content']}")
    pdf.drawString(50, 450, "Signature : ")
    pdf.drawString(50, 400, f"{contract['signature'][:64]}")
    pdf.drawString(50, 375, f"{contract['signature'][64:128]}")
    pdf.drawString(50, 350, f"{contract['signature'][128:]}")
    pdf.save()

    # Move the buffer's pointer to the beginning
    buffer.seek(0)

    # Return the generated PDF file to the user for download
    return send_file(buffer, as_attachment=True, download_name=f"contract_{contract['contract_id']}.pdf")


if __name__ == '__main__':
    app.run(debug=True)
