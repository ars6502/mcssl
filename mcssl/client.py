import socket
import io
from datetime import datetime, timezone
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


class Client:
    """
    Represents a client that connects to the server and sends/receives messages.

    :param host: Host address of the server (str)
    :param port: Port number of the server (int)
    :param encoder: Encoder instance for encoding/decoding messages
    """

    def __init__(self, host='localhost', port=10000, encoder=None):
        """
        Initialize a Client object.

        :param host: Host address of the server
        :param port: Port number of the server
        :param encoder: Encoder instance for encoding/decoding messages
        """
        self.host = host
        self.port = port
        self.client_socket = None
        self.response_handlers = {}
        self.encoder = encoder  # Encoder instance passed as an argument

    def connect(self):
        """
        Connect to the server at the specified address and port.
        """
        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)

        print(f'Connecting to {server_address[0]} port {server_address[1]}')

        try:
            self.client_socket.connect(server_address)
        except Exception as e:
            print(f"Failed to connect: {e}")
            raise

    def register_response_handler(self, method_name):
        """
        Register a handler function for a specific response message type.

        :param method_name: The name of the response method this handler is for (str)
        :return: Decorator function to register the handler
        """
        def decorator(func):
            self.response_handlers[method_name] = func
            return func
        return decorator

    def send_message(self, message: Message):
        """
        Send a message to the connected server.

        :param message: Message object to be sent
        """
        if not self.client_socket:
            print("Client is not connected.")
            return

        # Encode the message before sending it
        encoded_data = self.encoder.encode_message(message.to_json())
        try:
            self.client_socket.sendall(encoded_data)
        except Exception as e:
            print(f"Failed to send message: {e}")

    def receive_response(self) -> Message:
        """
        Receive a response from the server.

        :return: Message object created from the received data
        """
        if not self.client_socket:
            print("Client is not connected.")
            return None

        data = read_socket(self.client_socket)

        # Decode the received message after receiving it completely
        decoded_data = self.encoder.decode_message(data)
        return Message.from_json(decoded_data)

    def handle_response(self, response_message):
        """
        Handle a received response by invoking the registered handler.

        :param response_message: Message object received from server
        """
        handler = self.response_handlers.get(response_message.method)
        if handler:
            handler(response_message)
        else:
            print("No handler found for method:", response_message.method)

    def close(self):
        """
        Close the client socket connection.
        """
        if self.client_socket:
            print('Closing socket')
            try:
                self.client_socket.close()
            except Exception as e:
                print(f"Failed to close socket: {e}")
