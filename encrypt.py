import sys
import getpass
import my_aes

password = getpass.getpass('password> ')
password2 = getpass.getpass('confirm> ')
if password != password2:
    print('Passwords do not match.')
    sys.exit(0)
enc = my_aes.encrypt(sys.stdin.buffer.read(), password)
sys.stdout.buffer.write(enc)