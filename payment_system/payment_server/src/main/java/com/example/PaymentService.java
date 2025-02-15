package com.example;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface PaymentService extends Remote {
    void processPayment(double amount, String orderId) throws RemoteException;
}