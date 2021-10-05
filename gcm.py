from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import secrets
import binascii


key = get_random_bytes(32)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(b'Target data')
print(ciphertext)
cipher_dec = AES.new(key, AES.MODE_EAX, cipher.nonce)
data = cipher_dec.decrypt_and_verify(ciphertext, tag)
print(data)

