import sys
sys.path.append("./")
# dessa forma eu estou acessando uma pasta para trás
# fazendo com que o test consiga identificar as demasi pastas 


import pytest
import os
from payments.pix import Pix

def test_pix_create_payment():
    pix = Pix()

    #create a payment
    payment_info = pix.create_payment()

    #verify infos
    print(payment_info)

    assert "bank_payment_id" in payment_info
    assert "qr_code_path" in payment_info

    qr_code_path = payment_info["qr_code_path"]
    assert os.path.isfile(f"./static/img/{qr_code_path}.png")