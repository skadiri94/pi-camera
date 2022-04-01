from os.path import exists

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

private_key_pass = b"your-password"

def generate_key():
    file1_exists = exists("secrete-rsa.pem")
    file2_exists = exists("secrete-rsa.pub")
    
    if file1_exists and file2_exists:
        return None
    else:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        

        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                private_key_pass))
        
        p_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())

        pem_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)


        private_key_file = open("secrete-rsa.pem", "w")
        private_key_file.write(encrypted_pem_private_key.decode())
        private_key_file.close()

        public_key_file = open("secrete-rsa.pub", "w")
        public_key_file.write(pem_public_key.decode())
        public_key_file.close()
        
        return encrypted_pem_private_key.decode(), pem_public_key.decode()

def get_generated_key():
    file1_exists = exists("secrete-rsa.pem")
    file2_exists = exists("secrete-rsa.pub")
    
    if file1_exists and file2_exists:
        with open("secrete-rsa.pem", "rb") as key:
            
            priv_key= serialization.load_pem_private_key(
            key.read(),
            password=private_key_pass,
            backend=default_backend()
        )
        # f1  = open('secrete-rsa.pem', 'rb') 
        # # priv_key = f1.read()
        # priv_key = serialization.load_pem_private_key(f1.read(), password=private_key_pass, backend=default_backend())
      
#             p_key= serialization.load_pem_private_key(
#         key.read(),
#         password=os.environ['PRIVATE_KEY_PASSPHRASE'].encode(),
#         backend=default_backend()
#     )
 
        pkb = priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
 

        f2 = open('secrete-rsa.pub', 'r') 
        pub_key = f2.read()
        return pkb, pub_key

def get_keys(keys):
    
    secrete_keys = keys
    if secrete_keys != None:
        
        private_key = secrete_keys[0]
        public_key = secrete_keys[1]
        public_key= public_key.replace('-----BEGIN PUBLIC KEY-----\n', '')
        public_key = public_key.replace('\n-----END PUBLIC KEY-----\n', '')
        public_key = public_key.replace('\n', '')
        public_key = public_key.replace(' ', '')
        return public_key