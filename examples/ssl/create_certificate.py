from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime

CERT_FILE = "certificate.crt"
KEY_FILE = "private_key.key"


# Create a self signed certificate
def create_certificate():
         
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # create a self-signed cert
    cert = crypto.X509()
    # country name alias
    cert.get_subject().C    = "IN"     
    # state or province alias
    cert.get_subject().ST   = "Mumbai"
    # locality alias
    cert.get_subject().L    = "Mumbai"
    # organization alias
    cert.get_subject().O    = "Example Organization"
    # organizational unit alias
    cert.get_subject().OU   = "Example Organization"
    # common name alias
    cert.get_subject().CN   = gethostname()
    # set serial number
    cert.set_serial_number(1)

    # timestamp on which the certificate starts being valid
    cert.gmtime_adj_notBefore(0)

    # timestamp on which the certificate stops being valid
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(CERT_FILE, "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    open(KEY_FILE, "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

create_certificate()
