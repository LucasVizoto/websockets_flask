
# 🌏 WebSocket em Python

Este projeto demonstra a implementação de WebSockets em Python utilizando Flask-SocketIO para comunicação em tempo real. Ele ilustra como o servidor pode enviar mensagens aos clientes de forma assíncrona, impulsionado por eventos específicos ou "gatilhos" que ocorrem no backend.


Flask-SocketIO é uma extensão para o framework web Flask que facilita a integração de WebSockets em suas aplicações. Ele permite uma comunicação bidirecional e de baixa latência entre o servidor e os clientes, superando as limitações do modelo tradicional de requisição-resposta HTTP. Com Flask-SocketIO, você pode facilmente implementar funcionalidades como chats em tempo real, notificações instantâneas, dashboards interativos e muito mais, onde o servidor pode "empurrar" dados para o cliente sem que este precise solicitar.

### Cenário do Projeto:

Para exemplificar o uso de WebSockets, este projeto simula um fluxo de pagamento via QR Code. A aplicação gera dinamicamente um QR Code para cada transação e o disponibiliza através de uma rota específica da API.

Além da funcionalidade de WebSocket, o projeto também aprimora a integração com uma interface front-end. O Flask permite a renderização de páginas HTML diretamente do servidor usando a função ```render_template()```, o que facilita a construção de uma experiência de usuário coesa e interativa.
Funcionalidades Principais

✅ Criação de Pagamento: Uma rota da API permite a criação de um novo pedido de pagamento.

🔗 Autenticação e Redirecionamento: Após a autenticação de um pagamento via outra rota, a página do usuário é automaticamente redirecionada para uma página de "pagamento aprovado", demonstrando a capacidade de comunicação em tempo real via WebSocket.

⚠️ Tratamento de Erros: O projeto inclui uma página de erro 404 personalizada para IDs de pagamento inexistentes, garantindo uma experiência de usuário robusta. Além disso, foram implementados testes unitários para verificar se as função ```create_payment()``` possui o comportamento adequado.


## ⚙️ Rodando localmente

#### 1. Clone o projeto


```bash
  git clone https://github.com/LucasVizoto/websockets_flask
```
#### 2. Crie e ative um ambiente virtual


```bash
python -m venv venv

source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows

```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```


#### 4. Inicie o Servidor

```
  python app.py
```


## 📖 Documentação da API

- Criar um novo Pagamento

```http
  POST /payments/pix
```

#### Body da Requisição:
| Campo   | Tipo | Descrição|Exemplo|
| :---------- | :--------- | :---------- |:---------------------------------- |
| `value` | `integer` | **Obrigatório**. Valor do pagamento que será criado.| 1500 |


#### Resposta esperada: 
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "message": "The payment has been created",
    "payment": {
        "bank_payment_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "expiration_date": "Sun, 15 Jun 2025 16:00:03 GMT",
        "id": 123,
        "paid": false,
        "qr_code": "qr_code_payment_a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "value": 1500
    }
}

```
---
####

- Acesso à página HTML com o pagamento recém criado

```http
  {host}/payments/pix/id
```
#### Resposta esperada: 

![Print Página](https://raw.githubusercontent.com/LucasVizoto/websockets_flask/refs/heads/main/templates/screenshots/screenshot_1.png)

---
#### 
- Confirmação de Pagamento

```http
  POST /payments/pix/confirmation
```

#### Body da Requisição:
| Campo   | Tipo | Descrição|Exemplo|
| :---------- | :--------- | :---------- |:---------------------------------- |
| `value` | `integer` | **Obrigatório**. Valor do pagamento que foi criado.| 1500 |
| `bank_payment_id` | `string` | **Obrigatório**. Uuid retornado na resposta da criação do pagamento.| 1500 |


#### Resposta esperada: 
```http
{
    "message": "The payment has been confirmed"
}
```
* Verificar se a página de exibição do pagamento foi atualizada para a de Pagamento Confirmado.

![Print Página de Pagamento Confirmado](https://raw.githubusercontent.com/LucasVizoto/websockets_flask/refs/heads/main/templates/screenshots/screenshot_2.png)

---
#### 
- Retorno do QR Code gerado

```http
  GET /payments/pix/qr_code/qr_code_payment_ + uuid
```

#### Resposta esperada:

![Print Página de Pagamento Confirmado](https://raw.githubusercontent.com/LucasVizoto/websockets_flask/refs/heads/main/static/img/qr_code_payment_5e53bbf4-cdf1-4a2f-b137-551c4b462ef1.png)
## 🔗Links

 - [Link para o curso](https://app.rocketseat.com.br/classroom/comunicacao-em-tempo-real-com-flask)
 - [Certificado](https://app.rocketseat.com.br/certificates/032560aa-4254-4b01-8e6e-e1b4623e10bd)


## 🔎 Onde me encontrar

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lucasvizoto/)

[![e-mail](https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white)](mailto:lucavizoto364@gmail.com)
