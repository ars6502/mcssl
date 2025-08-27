import socket
import io
from datetime import datetime, timezone, timedelta
from .message import Message
from .encoder import Encoder

def read_socket(in_socket,size=1024):
    buf = io.BytesIO()
    done = False

    while not done:
        data = in_socket.recv(size)
        if len(data) < size:
            done=True
        buf.write(data)

    return buf.getvalue()

class Server:
    """
    Represents a server that handles incoming client connections and processes messages.

    :param host: Host address to bind the server (str)
    :param port: Port number to listen on (int)
    :param encoder: Encoder instance for encoding/decoding messages
    """

    def __init__(self, host='localhost', port=10000, encoder=None):
        """
        Initialize a Server object.

        :param host: Host address to bind the server
        :param port: Port number to listen on
        :param encoder: Encoder instance for encoding/decoding messages
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.method_handlers = {}
        self.encoder = encoder  # Encoder instance passed as an argument

    def start(self):
        """
        Start the server by binding to the address and listening for connections.
        """
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)

        print(f'Starting up on {server_address[0]} port {server_address[1]}')

        try:
            self.server_socket.bind(server_address)
            self.server_socket.listen(5)  # Listen for incoming connections
        except Exception as e:
            print(f"Failed to start server: {e}")
            raise

    def register_method(self, method_name):
        """
        Register a handler function for a specific message method.

        :param method_name: The name of the method this handler is for (str)
        :return: Decorator function to register the handler
        """
        def decorator(func):
            self.method_handlers[method_name] = func
            return func
        return decorator

    def handle_client(self, client_connection, client_address):
        """
        Handle communication with a connected client.

        :param client_connection: The socket connection object for the client (socket)
        :param client_address: The address of the connected client (tuple)
        """
        print(f"Connection from {client_address}")

        try:
            while True:
                data = read_socket(client_connection)
                if len(data) == 0:
                    client_connection.close()
                    return

                # Decode the received message after receiving it completely
                decoded_data = self.encoder.decode_message(data)
                message = Message.from_json(decoded_data)

                # Handle incoming message by invoking registered handlers or error handling
                handler = self.method_handlers.get(message.method)
                if handler:
                    response_message = handler(message)
                else:
                    response_message = Message(
                        method='error',
                        args=['Unknown method'],
                        options={}
                    )

                # Encode the response before sending it
                encoded_response = self.encoder.encode_message(response_message.to_json())
                client_connection.sendall(encoded_response)

        finally:
            # Clean up the connection
            print(f"Closing connection to {client_address}")
            client_connection.close()

    def run(self):
        """
        Run the server loop, accepting and handling client connections.
        """
        try:
            while True:
                client_connection, client_address = self.server_socket.accept()
                self.handle_client(client_connection, client_address)
        except KeyboardInterrupt:
            print('Shutting down server...')
        finally:
            if self.server_socket:
                self.server_socket.close()
