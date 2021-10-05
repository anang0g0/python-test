from base64 import b64encode
from base64 import b64decode
from Cryptodome.Cipher import AES
from hashlib import sha256
import random
""" AES.CTR_MODE による暗号化/復号 """
def generate_random_secret_key(algorithm_func=sha256):
    return algorithm_func(str(random.random).encode('utf-8')).digest()
def encrypt(secret_key, raw_data):
    crypto = AES.new(secret_key, AES.MODE_CTR)
    return dict(content=b64encode(crypto.encrypt(raw_data)).decode('utf-8'),
                nonce=b64encode(crypto.nonce).decode('utf-8'))
def decrypt(secret_key, encrypted_data):
    """ encrypted_data = dict(content, nonce) """
    crypto = AES.new(secret_key, AES.MODE_CTR, nonce=b64decode(encrypted_data['nonce']))
    return crypto.decrypt(b64decode(encrypted_data['content']))
if __name__ == "__main__":
    # 簡易テスト
    key = generate_random_secret_key()
    raw_data = 'raw_test_data'
    print("raw_data = {}".format(raw_data))
    encrypted_data = encrypt(key, raw_data.encode())
    print("encrypted_data.content = {} nonce = {}".format(encrypted_data['content'], encrypted_data['nonce']))
    decrypted_data = decrypt(key, encrypted_data)
    print("decrypted_data = {}".format(decrypted_data))