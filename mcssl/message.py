import json
from datetime import datetime, timezone

class Message(object):
    """
    Represents a message object that can be serialized to JSON and deserialized from JSON.
    Includes method name, arguments, options, and timestamp information.

    :param method: The method name this message is intended for (str)
    :param args: List of positional arguments for the method (list)
    :param options: Dictionary of keyword arguments for the method (dict)
    :param timestamp: ISO-formatted string timestamp of when the message was created (datetime str)
    """

    def __init__(self, method, args=None, options=None, timestamp=None):
        """
        Initialize a Message object.

        :param method: The method name this message is intended for
        :param args: List of positional arguments for the method
        :param options: Dictionary of keyword arguments for the method
        :param timestamp: ISO-formatted string timestamp of when the message was created (UTC)
        """
        self.method = method
        self.args = args if args is not None else []
        self.options = options if options is not None else {}
        # If no timestamp provided, use current time in UTC
        self.timestamp = timestamp if timestamp is not None else datetime.now(timezone.utc).isoformat()

    def to_json(self):
        """
        Convert the message object into a JSON string representation.

        :return: JSON string of the Message object
        """
        return json.dumps({
            'method': self.method,
            'args': self.args,
            'options': self.options,
            'timestamp': self.timestamp  # Include the timestamp
        })

    @staticmethod
    def from_json(json_str):
        """
        Create a Message instance from a JSON string.

        :param json_str: JSON string representing a message
        :return: Message object created from the JSON data
        """
        data = json.loads(json_str)
        method = data.get('method')
        args = data.get('args', [])
        options = data.get('options', {})
        timestamp = data.get('timestamp')  # Extract the timestamp
        return Message(method=method, args=args, options=options, timestamp=timestamp)

    def __repr__(self):
        """
        Provide a string representation of the Message object for debugging.

        :return: String representation of the Message instance
        """
        return f"Message(method={self.method}, args={self.args}, options={self.options}, timestamp={self.timestamp})"


