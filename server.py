# server.py
import logging
import socket
import sys
from typing import Optional, Tuple


class EchoServer:
    def __init__(
        self, host: str = "127.0.0.1", port: int = 12345, max_connections: int = 5
    ):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.server_socket = None

        # Configure logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def setup_socket(self) -> None:
        """Initialize and configure the server socket."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Allow port reuse
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connections)
            self.logger.info(f"Server listening on {self.host}:{self.port}")
        except socket.error as e:
            self.logger.error(f"Socket setup failed: {e}")
            sys.exit(1)

    def accept_connection(self) -> Tuple[Optional[socket.socket], Optional[Tuple]]:
        """Accept incoming connection."""
        try:
            client_socket, client_address = self.server_socket.accept()
            self.logger.info(f"Connection established with {client_address}")
            return client_socket, client_address
        except socket.error as e:
            self.logger.error(f"Connection acceptance failed: {e}")
            return None, None

    def handle_client(self, client_socket: socket.socket) -> None:
        """Handle client communication."""
        try:
            while True:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break

                self.logger.info(f"Received: {data}")
                client_socket.send(data.encode("utf-8"))
        except socket.error as e:
            self.logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def run(self) -> None:
        """Run the server."""
        self.setup_socket()
        try:
            while True:
                client_socket, _ = self.accept_connection()
                if client_socket:
                    self.handle_client(client_socket)
        except KeyboardInterrupt:
            self.logger.info("Server shutting down...")
        finally:
            if self.server_socket:
                self.server_socket.close()


if __name__ == "__main__":
    server = EchoServer()
    server.run()
