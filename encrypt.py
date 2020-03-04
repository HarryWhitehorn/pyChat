#pyChat - encrypt
import hashlib

def encrypt(string):
    if not len(string): #will return None if string == ""
        return(None)

    if type(string) != bytes: #checks bytes
        string = bytes(string,"utf-8")

    hashed = hashlib.sha256()
    hashed.update(string)
    return(hashed.hexdigest())

if __name__ == "__main__":
    string = "testPassword"
    string = encrypt(string)
    print(string)
