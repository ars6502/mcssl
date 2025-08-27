from mcssl.server  import Server    # Import the Server class
from mcssl.encoder import Encoder   # Import the Encoder class
from mcssl.message import Message   # Import the Message class

server = Server(encoder=Encoder())

@server.register_method()
def add(message: Message):
    """
    Handle addition request by adding provided numbers.

    :param message: Message containing method and arguments
    :return: Response message with result of the addition
    """
    a, b = message.args
    result = float(a) + float(b)
    print(f"Adding {a} and {b}")
    return Message(
        method='result',
        args=[str(result)],
        options={}
    )

@server.register_method()
def subtract(message: Message):
    """
    Handle subtraction request by subtracting provided numbers.

    :param message: Message containing method and arguments
    :return: Response message with result of the subtraction
    """
    a, b = message.args
    result = float(a) - float(b)
    print(f"Subtracting {a} and {b}")
    return Message(
        method='result',
        args=[str(result)],
        options={}
    )

@server.register_method()
def multiply(message: Message):
    """
    Handle multiplication request by multiplying provided numbers.

    :param message: Message containing method and arguments
    :return: Response message with result of the multiplication
    """
    a, b = message.args
    result = float(a) * float(b)
    print(f"Multiplying {a} and {b}")
    return Message(
        method='result',
        args=[str(result)],
        options={}
    )

server.start()
server.run()

