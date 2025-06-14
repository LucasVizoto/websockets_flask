from model.payment import Payment
from repository.database import db
from payments.pix import Pix

from flask import Flask, jsonify, request, send_file, render_template
from flask_socketio import SocketIO
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'
socketio = SocketIO(app)
db.init_app(app)


'''
--------------------------------------------------------------------
        GERANDO UM NOVO PAGAMENTO TRANSAÇÃO
---------------------------------------------------------------------
'''
@app.route("/payments/pix", methods=['POST'])
def create_payment_pix():
    data = request.get_json()
    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now()+ timedelta(minutes=30)

    new_payment = Payment(value = data['value'], 
                          expiration_date = expiration_date)
    pix = Pix()
    data_payment_pix = pix.create_payment()
    
    new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
    new_payment.qr_code = data_payment_pix['qr_code_path']


    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message":"The payment has been created",
                    "payment": new_payment.to_dict()}), 200

'''
---------------------------------------------------------------------
        RECUPERANDO O QR CODE NA REQUISIÇÃO
---------------------------------------------------------------------
'''
@app.route("/payments/pix/qr_code/<file_name>", methods=['GET'])
def get_image(file_name):
    return send_file(f'static/img/{file_name}.png', mimetype='image/png')


'''
---------------------------------------------------------------------
        ROTA DE CONFIRMAÇÃO DO PIX
---------------------------------------------------------------------
'''
@app.route("/payments/pix/confirmation", methods=['POST'])
def pix_confirmation(): # webhook pois sera requisitado pra informar
    data = request.get_json()
    
    if "bank_payment_id" not in data:
        return jsonify({"message":"Invalid payment data"}), 400
    
    #qual o payment que eu quero recuperar
    payment = Payment.query.filter_by(bank_payment_id = data.get("bank_payment_id")).first() 
    #Usar o identificado da transação bancária, pois a outr API nn sabe sobre minha indexação
    #e com o first pego só o primeiro

    if not payment or payment.paid:
        return jsonify({"message": "Payment not found"}), 404

    if data.get("value") != payment.value:
        return jsonify({"message": "Invalid data"}), 400

    payment.paid = True
    db.session.commit()
    #esse emit lança uma notificação para todos os usários, mas apenas aquele interessado
    # em lê-la que pode ver
    socketio.emit(f'payment-confirmed-{payment.id}')
    return jsonify({"message":"The payment has been confirmed"}), 200


'''
---------------------------------------------------------------------
        RENDERIZANDO UMA PÁGINA HTML
---------------------------------------------------------------------
'''
@app.route("/payments/pix/<int:payment_id>", methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)

    if payment.paid: #ou seja, se já foi pago
        return render_template('confirmed_payment.html', 
                               #importante passar aqui todos as variáveis utilizadas no html
                               payment_id = payment.id,
                               value = payment.value,
                               qr_code = payment.qr_code) 
    #renderizo o pagamento confirmado
    return render_template('payment.html',
                           payment_id = payment.id, 
                           value=payment.value,
                           host="http://127.0.0.1:5000", 
                           qr_code=payment.qr_code)

'''
---------------------------------------------------------------------
                            WEBSOCKET
---------------------------------------------------------------------
'''
#usando o método on, eu estou dizendo que estou esperando um evento, e o connet, 
#que seria justamente quando conectar na aplicação 
@socketio.on('connect')
def handle_connet():
    print("client connected to the server")


if __name__ == "__main__":
    socketio.run(app, debug=True)