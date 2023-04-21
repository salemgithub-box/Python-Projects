import socket
from threading import Thread


class TcpSocketServer:
    """Creates a tcp server socket

    Args:
        IP: IP address of the tcp server.
        PORT: Port address of the tcp server.

    Attributes:
        socket: Tcp socket.
        client_data: holds client names and sockets.
    """

    def __init__(
        self, IP=socket.gethostbyname(socket.gethostname()), PORT=12345
    ) -> None:
        self.client_data = {}  # a dictionary of client data (name, socket)
        # create a tcp socket.
        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        # bind the socket to the given IP and PORT
        self.socket.bind((IP, PORT))
        # put the socket in listening mode
        self.socket.listen()
        # wait for connections
        self.client_connections()

    def client_connections(self, MSG_SIZE=1024):
        """Accepts client connections

        Args:
            MSG_SIZE = Size of the sent and received messages in bytes.
        """

        while True:
            client_socket, client_address = self.socket.accept()
            print("established connection with {}".format(client_socket))

            # ask the client for a name
            client_socket.send("NAME".encode())
            client_name = client_socket.recv(MSG_SIZE).decode()

            # add client name and socket to the dictionary
            self.client_data[client_socket] = client_name

            # send a confirmation message to the client
            client_socket.send(
                "{}, you have established a connection with the server!".format(
                    client_name
                ).encode()
            )

            # open a thread for each client connection
            receive_thread = Thread(
                target=self.receive_messages, args=(client_socket, MSG_SIZE)
            )
            receive_thread.start()

    def receive_messages(self, client_socket, MSG_SIZE=1024):
        """Receives messages from clients after establishing their connection

        Args:
            client_socket: the socket of the client that made a conncetion wit the server
            MSG_SIZE = Size of the sent and received messages in bytes.
        """
        client_name = self.client_data[client_socket]
        while True:
            try:
                # receive message from the client
                message = client_socket.recv(MSG_SIZE).decode()
                message = (
                    f"\033[1;92m\t{client_name}: {message}\033[0m".encode()
                )
                # broadcast message to all clients
                self.broadcast_message(message)
            except:
                # remove client socket from dict
                self.client_data.pop(client_socket)
                # close socket
                client_socket.close()
                # announce that the user has left the chatroom
                message = "has left the chat room!"
                message = (
                    f"\033[5;91m\t{client_name}: {message}\033[0m".encode()
                )
                self.broadcast_message(message)
                break

    def broadcast_message(self, msg):
        """Broadcasts received message to all client!

        Args:
            msg: message to be broadcasted to all clients!
        """
        for client_socket in self.client_data:
            client_socket.send(msg)


def main():
    tcp_socket = TcpSocketServer()


if __name__ == "__main__":
    main()
