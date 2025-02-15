import requests

ORDER_SERVER_URL = 'http://localhost:8080/orders'  
def create_order(order_data):
    """Envia uma requisição POST para o Servidor de Pedidos para criar um novo pedido."""
    try:
        response = requests.post(ORDER_SERVER_URL, json=order_data)
        response.raise_for_status()  
        return response.text.split(': ')[1]  
    except requests.exceptions.RequestException as e:
        print(f"Erro ao comunicar com o Servidor de Pedidos: {e}")
        return None

def get_order_status(order_id):
    """Envia uma requisição GET para o Servidor de Pedidos para obter o status de um pedido."""
    try:
        response = requests.get(f'{ORDER_SERVER_URL}/{order_id}')
        response.raise_for_status()
        return response.text.split(': ')[1]  
    except requests.exceptions.RequestException as e:
        print(f"Erro ao comunicar com o Servidor de Pedidos: {e}")
        return None