# Features
* the server accepts multiple client connections.
* the server broadcasts the received message to all client.
* all clients can send messages to the server.
* message are guaranteed to be sent 1024 bytes at a time.

----

# Usage
### start the server using the following command.
    python3 server.py
### start clients using the following command.
    python3 client.py
### at first you have to send the client's name to the server then you can send any message.