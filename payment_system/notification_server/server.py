import socket
import threading
import grpc
from concurrent import futures

import notification_pb2
import notification_pb2_grpc

HOST = 'localhost'
PORT = 65432
clients = {}  

class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def SendNotification(self, request, context):
        order_id = request.order_id
        message = request.message
        print(f"gRPC: Recebida notificação para o pedido {order_id}: {message}")
        send_socket_message(order_id, message)
        return notification_pb2.NotificationResponse(success=True)

def send_socket_message(order_id, message):
    for client_address, client_socket in clients.items():
        try:
            client_socket.sendall(f"Pedido {order_id}: {message}".encode('utf-8'))
        except:
            print(f"Erro ao enviar para {client_address}")
            del clients[client_address]

def handle_client(conn, address):
    print(f"Conectado por {address}")
    clients[address] = conn

    try:
        while True:
            data = conn.recv(1024) 
            if not data:
                break
            print(f"Recebido de {address}: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Erro com cliente {address}: {e}")
    finally:
        print(f"Conexão com {address} fechada")
        del clients[address]
        conn.close()

def start_socket_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor Socket escutando em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port('[::]:50051') 
    server.start()
    print("Servidor gRPC rodando...")
    server.wait_for_termination()

if __name__ == "__main__":
    threading.Thread(target=start_socket_server, daemon=True).start()
    serve_grpc()