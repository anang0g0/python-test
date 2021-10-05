import pickle
import base64

# padding by pkcs7
_pad = lambda s: s + (32 - len(s) % 32) * chr(32 - len(s) % 32)

# save data to file
def _save_file(file_path, data):
    target = file_path
    if file_path == "":
        target = "_{}.pkl".format("key" if type(data) == type("") else "pass")

    with open(target, 'wb') as f:
        pickle.dump({"data": data}, f)

# load data from file
def _load_file(file_path, iskey=False):
    target = file_path
    if file_path == "":
        target = "_{}.pkl".format("key" if iskey else "pass")

    if target.endswith("psk"):
        with open(target, 'r', encoding='utf-8-sig') as f:
            return f.read().replace("\r", "").replace("\n", "")
    else:
        with open(target, 'rb') as f:
            return pickle.load(f)["data"]

class KeyUtil:
    # utility class for managing key
    def __init__(self, key=""):
        if key != "":
            # set secret key with modifying
            self.__key = key[:32] if len(key) >= 32 else _pad(key)
        else:
            # generate new key
            import random
            import string
            self.__key = ''.join(random.choices(
                string.ascii_letters + string.digits, k=32))

    def get(self):
        return self.__key

    def save(self, file_path=""):
        _save_file(file_path, self.__key)

    def load(self, file_path=""):
        self.__key = _load_file(file_path, iskey=True)
        return self.__key

class AesCipher:
    def __init__(self, secret_key):
        if len(secret_key) != 32:
            raise Exception("unexpected secret key length")
        self.__key = secret_key
        # use bytes in case of PyCryptodome
        self.__key = sectet_key.encode("utf-8")
        # ---
        self.__encrypted = None

    def encrypt_phrase(self, phrase):
        from Crypto import Random
        from Crypto.Cipher import AES
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.__key, AES.MODE_CBC, iv).encrypt(_pad(phrase))
        # store encrypted phrase
        self.__encrypted = base64.b64encode(iv + cipher)

    def get(self):
        return self.__encrypted

    def save(self, file_path=""):
        _save_file(file_path, self.__encrypted)

    def load(self, file_path=""):
        self.__encrypted = _load_file(file_path)

    def decrypt_phrase(self, encrypted_phrase=""):
        # use loaded one if argument is not specified
        data_bytes = encrypted_phrase
        if encrypted_phrase == "":
            data_bytes = self.__encrypted

        from Crypto.Cipher import AES
        enc = base64.b64decode(data_bytes)
        cipher = AES.new(self.__key, AES.MODE_CBC, enc[:AES.block_size])
        dec = cipher.decrypt(enc[AES.block_size:])
        # decode as unpad string
        return dec[:-ord(dec[len(dec) - 1:])].decode()