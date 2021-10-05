# これが暗号化/復号化処理関数のファイルです。
import crypto_util

input_file_name = "README.md"
output_data_file_name = "output_data_file"
key_file_name = "test.aes"

# 暗号化
crypto_util.encrypt_from_file(input_file_name, output_data_file_name, key_file_name)

# 復号化
decrypto_data = crypto_util.decrypt_from_file(output_data_file_name, key_file_name)

print(decrypto_data)