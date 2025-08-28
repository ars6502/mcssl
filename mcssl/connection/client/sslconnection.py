from mcssl.connection import Connection
import ssl

class SSLConnection(Connection):
    def __init__(self,cert,cert_hostname):
        self.cert = cert
        self.cert_hostname=cert_hostname

        self.context = None

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cadata=self.cert)

        self.context = context


    def wrap_socket(self,client_socket):
        return self.context.wrap_socket(client_socket,server_hostname=self.cert_hostname)



