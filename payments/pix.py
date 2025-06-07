from uuid import uuid4
import qrcode

class Pix:
    def __init__(self):
        pass

    def create_payment(self):
        # criar o pagamento na gateway de pagamento, 
        # como não temos, fazer mock dos dados
        bank_payment_id = str(uuid4()) #gera um uuid randomico

        '''
        #qr code no pix tem o copie e cola, e o de pagamento mesmo, que é basicamente o copie e col
        # mas no formato de imagem

        lib - https://github.com/lincolnloop/python-qrcode

        '''
        hash_payment =  f'hash_payment_{bank_payment_id}'
        img = qrcode.make(hash_payment) #gera um objeto com o hash payment
        img.save(f'static/img/qr_code_payment_{bank_payment_id}.png') 
        # indico o path que ele vai salvar a imagem e onde salvar a imagem como png


        return{
            "bank_payment_id": bank_payment_id,
            "qr_code_path": f'qr_code_payment_{bank_payment_id}'
        }