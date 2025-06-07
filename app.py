from flask import Flask, jsonify, request
from repository.database import db
from model.payment import Payment
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)

@app.route("/payments/pix", methods=['POST'])
def create_payment_pix():
    data = request.get_json()
    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now()+ timedelta(minutes=30)

    new_payment = Payment(value = data['value'], 
                          expiration_date = expiration_date)
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message":"The payment has been created",
                    "payment": new_payment.to_dict()}), 200

@app.route("/payments/pix/confirmation", methods=['POST'])
def pix_confirmation(): # webhook pois sera requisitado pra informar 
    return jsonify({"message":"The payment has been confirmed"}), 200

@app.route("/payments/pix/<int:payment_id>", methods=['GET'])
def payment_pix_page(payment_id):
    return 'Pagammento pix'

if __name__ == "__main__":
    app.run(debug=True)