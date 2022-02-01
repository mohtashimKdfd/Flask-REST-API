import bcrypt 
x='hello'
password=x.encode('utf-8')

hasher = bcrypt.hashpw(password,bcrypt.gensalt())
hasheer = bcrypt.hashpw(password,bcrypt.gensalt())
hasheerr = bcrypt.hashpw(hasher,bcrypt.gensalt())

print(hasher.digest())