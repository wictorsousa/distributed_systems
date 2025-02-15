from flask import Flask, request, jsonify
import socket
import threading
import json
import requests
from client.utils import create_order, get_order_status

app = Flask(__name__)
NOTIFICATION_SERVER_HOST = 'localhost'  
NOTIFICATION_SERVER_PORT = 65432
ORDER_SERVER_URL = 'http://localhost:8080/orders'  

client_socket = None
order_id_to_track = None  

def start_socket_listener():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((NOTIFICATION_SERVER_HOST, NOTIFICATION_SERVER_PORT))
        print("Conectado ao servidor de notificações.")
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor de notificações. Verifique se ele está rodando.")
        return

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Notificação recebida: {message}")  
                else:
                    break  
            except ConnectionResetError:
                print("Conexão com o servidor de notificações perdida.")
                break

    threading.Thread(target=receive_messages, daemon=True).start()

@app.route('/order', methods=['POST'])
def create_order_route():
    order_data = request.json
    try:
        order_id = create_order(order_data)  
        if order_id:
            global order_id_to_track
            order_id_to_track = order_id 
            return jsonify({'message': 'Pedido criado com sucesso!', 'order_id': order_id}), 201
        else:
            return jsonify({'message': 'Erro ao criar o pedido.'}), 500
    except Exception as e:
        print(f"Erro ao criar o pedido: {e}")
        return jsonify({'message': 'Erro ao criar o pedido.'}), 500

@app.route('/order/<order_id>', methods=['GET'])
def get_order_status_route(order_id):
    try:
        status = get_order_status(order_id)  
        if status:
            return jsonify({'order_id': order_id, 'status': status})
        else:
            return jsonify({'message': 'Pedido não encontrado.'}), 404
    except Exception as e:
        print(f"Erro ao obter o status do pedido: {e}")
        return jsonify({'message': 'Erro ao obter o status do pedido.'}), 500

if __name__ == '__main__':
    start_socket_listener()  
    app.run(debug=True, port=5000)