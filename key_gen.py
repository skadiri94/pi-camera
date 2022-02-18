# import sys
# import paramiko

# key = paramiko.RSAKey.generate(4096)
# print(key.get_base64())  # print public key
# key.write_private_key(sys.stdout)  # print private key

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_key():

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_pass = b"your-password"

    encrypted_pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            private_key_pass))

    pem_public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # print(encrypted_pem_private_key)
    


    private_key_file = open("secrete-rsa.pem", "w")
    private_key_file.write(encrypted_pem_private_key.decode())
    private_key_file.close()

    public_key_file = open("secrete-rsa.pub", "w")
    public_key_file.write(pem_public_key.decode())
    public_key_file.close()
    
    return encrypted_pem_private_key.decode(), pem_public_key.decode()