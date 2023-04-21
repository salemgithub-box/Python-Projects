import socket
from threading import Thread


class TcpClientSocket:
    """Creates a tcp client socket

    Args:
        IP: IP address of the tcp server.
        PORT: Port address of the tcp server.

    Attributes:
        socket: Tcp socket.
    """

    def __init__(
        self, IP=socket.gethostbyname(socket.gethostname()), PORT=12345
    ) -> None:
        # create a tcp socket.
        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        self.socket.connect((IP, PORT))

        # Create threads to continuously send and recieve messages
        recieve_thread = Thread(target=self.receive_messages)
        send_thread = Thread(target=self.send_message)

        # Start the client
        recieve_thread.start()
        send_thread.start()

    def receive_messages(self, MSG_SIZE=1024):
        """Receive incoming messages from the tcp server"""
        while True:
            # Recieve an incoming message from the server.
            message = self.socket.recv(MSG_SIZE).decode()
            # Check for the name flag, else show the message
            if message == "NAME":
                name = input("What is your name: ")
                self.socket.send(name.encode())
            else:
                print(message)

    def send_message(self):
        """Send a message to the server"""
        while True:
            message = input("")
            self.socket.send(message.encode())


def main():
    tcp_socket = TcpClientSocket()


if __name__ == "__main__":
    main()
