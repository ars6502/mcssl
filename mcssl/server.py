import socket
import threading
import sys
import ssl
from datetime import datetime, timezone, timedelta
from .common  import read_socket
from .message import Message
from .encoder import Encoder
from .connection.server import *


class Server(object):
    """
    Represents a server that handles incoming client connections and processes messages.

    :param host: Host address to bind the server (str)
    :param port: Port number to listen on (int)
    :param encoder: Encoder instance for encoding/decoding messages
    """

    def __init__(self, host='localhost', port=10000, encoder=None,connection_type=PlainConnection()):
        """
        Initialize a Server object.

        :param host: Host address to bind the server
        :param port: Port number to listen on
        :param encoder: Encoder instance for encoding/decoding messages
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.stop_main_thread = False
        self.method_handlers = {}
        self.encoder = encoder  # Encoder instance passed as an argument
        self.connection_type = connection_type

    def start_server(self):
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
        try:
            while not self.stop_main_thread:
                try:
                    client_connection, client_address = self.server_socket.accept()
                    wrapped_connection = self.connection_type.wrap_socket(client_connection)
                    threading.Thread(target=self.handle_client, 
                                 args=(wrapped_connection,client_address)).start()
                except ssl.SSLError as ex:
                    print("SSL Error")
        except Exception as e:
            print(e)

    def register_method(self):
        """
        Register a handler function for a specific message method.

        :return: Decorator function to register the handler
        """
        def decorator(func):
            self.method_handlers[func.__name__] = func
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

    def stop_server(self):
        self.stop_main_thread = True

        # makes a dummy connection just to unlock accept method
        # and trigger the graceful stop
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host,self.port))


    def run(self):
        """
        Run the server loop, accepting and handling client connections.
        """


        try:
            self.main_thread = threading.Thread(target=self.start_server,args=())
            self.main_thread.start()

        except KeyboardInterrupt as e:
            print('Shutting down server...')
            self.stop_server()
            self.main_thread.join()
            self.server_socket.close()

