from .connection import Connection

class PlainConnection(Connection):
    def wrap_socket(self,client_socket):
        return client_socket


