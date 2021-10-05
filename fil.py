# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
key_size = 32
iv = '1234567890123456'.encode('utf-8')

def create_key(p_key):
    """
    キーデータ(bytes)を作成する。
    長さが32でない場合は、0埋め、もしくはtrimする。
    :param p_key:
    :return:
    """
    key_size_fill = p_key.zfill(key_size)
    key = key_size_fill[:key_size].encode('utf-8')
    return key


def encrypt(data, p_key, output_file=None):
    """
    暗号化
    :param data: 暗号化対象データ
    :param p_key: 暗号キー
    :param output_file: 暗号化結果の出力先ファイル
    :return:
    """
    key = create_key(p_key)
    obj = AES.new(key, AES.MODE_CFB, iv)

    ret_bytes = obj.encrypt(data)

    if output_file is not None:
        with open(output_file, "wb") as fout:
            fout.write(ret_bytes)

    return ret_bytes


def decrypt(data, p_key):
    """
    復号化
    :param data:復号化データ
    :param p_key:暗号キー
    :return:
    """
    key = create_key(p_key)
    obj = AES.new(key, AES.MODE_CFB, iv)
    return obj.decrypt(data)


def encrypt_from_file(input_data_file_name, output_data_file_name, key_file_path):
    """
    データを暗号化しファイルに出力する。
    :param input_data_file_name: 暗号化したい文字列を含むファイル(パスを含む)
    :param output_data_file_name: 暗号化ファイル(パスを含む)
    :param key_file_path: 暗号キーファイル(パスを含む)
    :return:
    """
    with open(input_data_file_name, "r", encoding="utf-8") as df:
        str_file_data = df.read()

    with open(key_file_path, "r") as kf:
        key = kf.read()

    return encrypt(str_file_data, key, output_file=output_data_file_name)


def decrypt_from_file(data_file_path, key_file_path):
    """
    暗号化されたファイルを復号化する。
    :param data_file_path: 暗号化されたファイル(パスを含む)
    :param key_file_path: 暗号キーファイル(パスを含む)
    :return:
    """
    with open(data_file_path, "rb") as df:
        byte = df.read()

    with open(key_file_path, "r") as kf:
        key = kf.read()

    return decrypt(byte, key).decode('utf-8')