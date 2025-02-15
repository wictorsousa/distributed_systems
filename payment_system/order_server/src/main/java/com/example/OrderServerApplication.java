package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import java.rmi.Naming;
import java.util.HashMap;
import java.util.Map;

@SpringBootApplication
@RestController
public class OrderServerApplication {

    private final Map<String, String> orderStatuses = new HashMap<>(); 
    private PaymentService paymentService;

    private NotificationServiceGrpc.NotificationServiceBlockingStub notificationStub;


    public static void main(String[] args) {
        SpringApplication.run(OrderServerApplication.class, args);
    }

    @PostConstruct
    public void init() {
        try {
            paymentService = (PaymentService) Naming.lookup("//localhost/PaymentService");
            System.out.println("Conectado ao Servidor de Pagamentos!");
        } catch (Exception e) {
            System.err.println("Erro ao conectar com o Servidor de Pagamentos: " + e.getMessage());
            e.printStackTrace();
        }

        this.notificationStub = NotificationServiceGrpc.newBlockingStub(GrpcConfig.getChannel());

    }

    @PostMapping("/orders")
    public String createOrder(@RequestBody Order order) {
        String orderId = generateOrderId(); 
        orderStatuses.put(orderId, "Criado");
        System.out.println("Pedido criado: " + order);

        try {
            paymentService.processPayment(order.getValue(), orderId); 
            updateOrderStatus(orderId, "Pago");

        } catch (Exception e) {
            System.err.println("Erro ao processar pagamento: " + e.getMessage());
            updateOrderStatus(orderId, "Erro no pagamento");
        }

        return "Pedido criado com ID: " + orderId;
    }

    @GetMapping("/orders/{orderId}")
    public String getOrderStatus(@PathVariable String orderId) {
        return "Status do pedido " + orderId + ": " + orderStatuses.getOrDefault(orderId, "Pedido não encontrado");
    }

    public void updateOrderStatus(String orderId, String status) {
        orderStatuses.put(orderId, status);
        System.out.println("Status do pedido " + orderId + " atualizado para: " + status);

        try {
            Notification.NotificationRequest request = Notification.NotificationRequest.newBuilder()
                    .setOrderId(orderId)
                    .setMessage("O status do seu pedido foi atualizado para: " + status)
                    .build();
            Notification.NotificationResponse response = notificationStub.sendNotification(request);
            System.out.println("Notificação enviada via gRPC. Sucesso: " + response.getSuccess());
        } catch (Exception e) {
            System.err.println("Erro ao enviar notificação via gRPC: " + e.getMessage());
        }
    }

    private String generateOrderId() {
        return java.util.UUID.randomUUID().toString();
    }
}