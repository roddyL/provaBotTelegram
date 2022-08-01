import hashlib
import os
# h = hashlib.new('sha256')#sha256 can be replaced with diffrent algorithms
# h.update('Hello World'.encode()) #give a encoded string. Makes the String to the Hash 
# print(h.hexdigest())#Prints the Hash


pr=hashlib.new('sha256')
prova="fromfarmtofork"
pr.update(f"{prova}".encode())
print(pr.hexdigest())

# salt=os.urandom(32)
salt=b'ciaosonoloris'
print(salt)
plain_text="fromfarmtofork".encode()
digest=hashlib.pbkdf2_hmac("sha256",plain_text, salt, 103471)
print(digest.hex())

# sr=hashlib.new('sha256')
# sr.update("fromfarmtofork".encode())
# print(sr.hexdigest())
# print(sr.hexdigest()==pr.hexdigest())