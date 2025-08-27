from mcssl.client  import Client    # Import the Client class
from mcssl.encoder import Encoder   # Import the Encoder class
from mcssl.message import Message   # Import the Message class

client = Client(encoder=Encoder())

@client.register_request()
def add(a,b):
    """ If it returns true then:
            Calls the Message(method="add", args=[a,b], options={}) 
            and handles the response. 
        Exception otherwise
    """
    return True

@client.register_request()
def subtract(a,b):
    return True

@client.register_request()
def multiply(a,b):
    return True

@client.register_response_handler()
def result(message):
    """
    Handle result response messages by extracting and printing results.

    :param message: Message object with method 'result'
    """
    result = message.args[0]
    print("Handling result with args:", result)

try:
    client.connect()
    # Example messages for addition, subtraction, and multiplication

    add(10,5)
    subtract(10,5)
    multiply(10,5)

except Exception as e:
    print(f"Client failed: {e}")
finally:
    client.close()



