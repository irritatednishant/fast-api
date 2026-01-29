from argon2 import PasswordHasher

ph = PasswordHasher()



def hash(passwd : str):
    return ph.hash(passwd)


def verify(hashed_passwd,passwd):
    return ph.verify(hashed_passwd,passwd)
