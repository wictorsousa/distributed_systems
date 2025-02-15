package com.example.config;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class GrpcConfig {
    private static ManagedChannel channel;

    public static ManagedChannel getChannel() {
        if (channel == null) {
            channel = ManagedChannelBuilder.forAddress("localhost", 50051) // Endereço do Servidor de Notificações
                    .usePlaintext() // Usar apenas em desenvolvimento
                    .build();
        }
        return channel;
    }
}