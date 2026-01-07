# Component: EUD Handler

End-user device handler is what enables TAK clients and devices to connect with OpenTakServer.

It listens on a TCP or SSL socket awaiting end-user TAK clients to connect. Once an EUD connects, a new thread is spawned to handle authentication, and proxying CoT messages to other EUDs via RabbitMQ exchanges.

## Requirements

- Host listen privileges
- RabbitMQ
- Database
