from mcssl.client  import Client    # Import the Client class
from mcssl.encoder import Encoder   # Import the Encoder class
from mcssl.message import Message   # Import the Message class

client = Client(encoder=Encoder())

@client.register_response_handler('result')
def handle_result(message):
    """
    Handle result response messages by extracting and printing results.

    :param message: Message object with method 'result'
    """
    result = message.args[0]
    print("Handling result with args:", result)

try:
    client.connect()
    # Example messages for addition, subtraction, and multiplication
    client.send_message(Message(method='add', args=['10', '5'], options={}))
    response_message = client.receive_response()
    if response_message:
        client.handle_response(response_message)

    client.send_message(Message(method='subtract', args=['10', '5'], options={}))
    response_message = client.receive_response()
    if response_message:
        client.handle_response(response_message)

    client.send_message(Message(method='multiply', args=['10', '5'], options={}))
    response_message = client.receive_response()
    if response_message:
        client.handle_response(response_message)
except Exception as e:
    print(f"Client failed: {e}")
finally:
    client.close()



