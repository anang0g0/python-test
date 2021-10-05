import socketserver
from base64 import b64encode, b64decode
import socket
import threading
import json
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from pkcs12 import PKCS12
from aes import generate_random_secret_key
from rsa import RSACipher
from aes import encrypt, decrypt, generate_random_secret_key
BUFFER=2048
class CipherRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # クライアントへ 受信したデータを返却する
        enc_data = self.request.recv(BUFFER)
        print("enc_data at server: {}".format(enc_data))
        dec_data = dec_process(enc_data)
        print("enc_data decrypting at server: {}".format(dec_data))
        self.request.send(dec_data)
def get_b64_to_json_load(b64_json_encrypted_data):
    return json.loads(b64decode(b64_json_encrypted_data).decode('utf-8'))
def dec_process(b64_json_enc_data):
    # dict(secret_key, enc_message)
    enc_data = get_b64_to_json_load(b64_json_enc_data)
    rsa = RSACipher()
    with open(PKCS12.PRIVATE_KEY_FILENAME) as f:
        rsa.import_privkey(f.read())
    enc_secret_key = b64decode(enc_data['secret_key'])
    # 秘密鍵で復号
    dec_key = rsa.decrypt(enc_secret_key)
    print("decrypted key: {}".format(dec_key))
    dec_data = decrypt(dec_key, enc_data['enc_message'])
    print("dec_data = {}".format(dec_data))
    return dec_data
def enc_process(raw_message):
    # 公開鍵を読み込み
    rsa = RSACipher()
    with open(PKCS12.PUBLIC_KEY_FILENAME) as f:
        rsa.import_pubkey(f.read())
    # 公開鍵で秘密鍵(secret_key)を暗号化
    secret_key = generate_random_secret_key()
    print("encrypted secret key: {}".format(secret_key))
    enc_secret_key = rsa.encrypt(secret_key)
    enc_message = encrypt(secret_key, raw_message.encode())
    enc_struct = dict(secret_key=b64encode(enc_secret_key).decode('utf-8'), enc_message=enc_message)
    print("enc_struct {}".format(enc_struct))
    enc_data = b64encode(json.dumps(enc_struct).encode('utf-8'))
    print(enc_data)
    return enc_data
def tcp_process():
    # サーバ側
    address = ('localhost', 19012)
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(address, CipherRequestHandler)
    ip, port = server.server_address # 与えられたポート番号を調べる
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # 終了時にハングアップしない
    t.start()
    # クライアント側
    # サーバへ接続する
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    # データを送る
    message = 'Hello, world'
    print('Message : "{}"'.format(message))
    enc_data = enc_process(message)
    print('Sending Encrypt Data : "{}"'.format(enc_data))
    len_sent = s.send(enc_data)
    # レスポンスを受けとる
    response = s.recv(len_sent)
    print('Received: "{}"'.format(response))
    # クリーンアップ
    s.close()
    server.socket.close()
def main():
    tcp_process()
    # message = 'Hello, world'
    # enc_data = enc_process(message)
    # dec_data = dec_process(enc_data)
if __name__ == '__main__':
    main()