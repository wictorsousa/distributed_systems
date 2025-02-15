package com.example;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class PaymentServer extends UnicastRemoteObject implements PaymentService {

    public PaymentServer() throws RemoteException {
        super();
    }

    @Override
    public void processPayment(double amount, String orderId) throws RemoteException {
        System.out.println("Recebido pedido de pagamento para o pedido: " + orderId + ", valor: " + amount);

        boolean paymentSuccessful = true;
        if (paymentSuccessful) {
            System.out.println("Pagamento aprovado para o pedido: " + orderId);

        } else {
            System.out.println("Pagamento reprovado para o pedido: " + orderId);

        }
    }

    public static void main(String[] args) {
        try {
            PaymentServer server = new PaymentServer();
            Registry registry = LocateRegistry.createRegistry(1099); 
            registry.bind("PaymentService", server);
            System.out.println("Servidor de Pagamentos pronto!");
        } catch (Exception e) {
            System.err.println("Erro no Servidor de Pagamentos: " + e.getMessage());
            e.printStackTrace();
        }
    }
}