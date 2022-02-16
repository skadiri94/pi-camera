import sys
import paramiko

key = paramiko.RSAKey.generate(4096)
print(key.get_base64())  # print public key
key.write_private_key(sys.stdout)  # print private key