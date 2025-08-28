from mcssl.connection import Connection
import ssl

class SSLConnection(Connection):
    def __init__(self,cert,key):
        self.cert = cert
        self.key = key
        self.context = None

        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.cert,self.key)
        except ssl.SSLError as e:
            sys.exit('Error in SSL certificate/password')

        self.context = context


    def wrap_socket(self,client_socket):
        return self.context.wrap_socket(client_socket, server_side=True)



