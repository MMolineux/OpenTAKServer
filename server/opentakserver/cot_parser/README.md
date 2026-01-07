# Component: CoT parser

Listens for new Cursor-on-Target messages emitted onto RabbitMQ exchanges by EUDs, parses the messages, then persists the parsed message in the database.

## Requirements

- RabbitMQ
- Database
