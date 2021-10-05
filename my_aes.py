from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from base64 import b64encode
from base64 import b64decode

def create_aes(password, iv):
	sha = SHA256.new()
	sha.update(password.encode())
	key = sha.digest()
	return AES.new(key, AES.MODE_CFB, iv)

def encrypt(decrypted_data, password):
	iv = Random.new().read(AES.block_size)
	return iv + create_aes(password, iv).encrypt(decrypted_data)

def decrypt(encrypted_data, password):
	iv, cipher = encrypted_data[:AES.block_size], encrypted_data[AES.block_size:]
	return create_aes(password, iv).decrypt(cipher)

if __name__ == '__main__':

	password = "tommy1"
	s_strings = "secret tommy's sentence."

	enc = encrypt(s_strings, password)
	print(enc)

	dec = decrypt(enc, password)
	print(dec)
