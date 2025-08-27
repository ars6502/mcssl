class Encoder(object):
    """
    Provides methods to encode and decode message data.

    """

    def __init__(self):
        pass

    def encode_message(self, message):
        """
        Encode the provided message string based on the encoding type.

        :param message: The message data to be encoded (str)
        :return: Encoded message data
        """
        return message.encode()

    def decode_message(self, encoded_data):
        """
        Decode the provided encoded data based on the decoding method.

        :param encoded_data: The encoded message data to be decoded (bytes)
        :return: Decoded message string
        """
        return encoded_data.decode('UTF-8')
