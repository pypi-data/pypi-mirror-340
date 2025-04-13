import pika

class RabbitMQConnection:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)

    def connect(self):
        connection_params = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials
        )
        return pika.BlockingConnection(connection_params)