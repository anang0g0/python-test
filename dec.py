import sys
import getpass
import my_aes

password = getpass.getpass('password> ')
dec = my_aes.decrypt(sys.stdin.buffer.read(), password)
sys.stdout.buffer.write(dec)