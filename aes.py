from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Util.number import long_to_bytes
import secrets
import binascii
import base64

flag= open("README.md", "rb").read()
key= get_random_bytes(32)
HexMyKey= key.hex()

#with open("seed.key","rb") as f:
#    key=f.read()
cipher= AES.new(key, AES.MODE_EAX,nonce=get_random_bytes(16))
ciphertext, tag= cipher.encrypt_and_digest(flag)
enc= cipher.nonce + ciphertext + tag
HexEncryptedOriginalMessage= base64.b64encode(enc)
print(HexEncryptedOriginalMessage)
with open("cipher.asc","wb") as f:
     f.write(HexEncryptedOriginalMessage)
f.close()
HexMyKey= key.hex()
#with open("MyKey.hex","r") as f:
#    HexMyKey=f.read()
print(HexMyKey)
key=bytes.fromhex(HexMyKey)
#data = bytes.fromhex(HexEncryptedOriginalMessage)
with open("cipher.asc","rb") as f:
    data=base64.b64decode(f.read())
cipher = AES.new(key, AES.MODE_EAX, data[:16]) # nonce
try:
    dec = cipher.decrypt_and_verify(data[16:-16], data[-16:]).decode('utf-8') # ciphertext, tag
    print(dec) # b'my secret data'
except ValueError:
    print("Decryption failed")