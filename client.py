# client.py
import logging
import socket
from typing import Optional


class EchoClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 12345):
        self.host = host
        self.port = port
        self.client_socket = None

        # Configure logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """Establish connection to the server."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.logger.info(f"Connected to server at {self.host}:{self.port}")
            return True
        except socket.error as e:
            self.logger.error(f"Connection failed: {e}")
            return False

    def send_message(self, message: str) -> Optional[str]:
        """Send message to server and receive response."""
        try:
            self.client_socket.send(message.encode("utf-8"))
            response = self.client_socket.recv(1024).decode("utf-8")
            self.logger.info(f"Received from server: {response}")
            return response
        except socket.error as e:
            self.logger.error(f"Communication error: {e}")
            return None

    def close(self) -> None:
        """Close the client socket."""
        if self.client_socket:
            self.client_socket.close()
            self.logger.info("Connection closed")

    def run(self, message: str = "Hello, server!") -> None:
        """Run the client with the specified message."""
        try:
            if self.connect():
                self.send_message(message)
        finally:
            self.close()


if __name__ == "__main__":
    client = EchoClient()
    client.run()
