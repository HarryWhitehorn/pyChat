#pyChat - login
import json
FILENAME = "user.json"
 
def save(data,filename=FILENAME):
    with open(filename,"w") as f:
        json.dump(data, f, indent = 4,ensure_ascii=False, encoding='utf-8')

def load(filename=FILENAME):
    with open(filename,"r") as f:
        return(json.load(f))

def init(filename=FILENAME):
    with open(filename,"w") as f:
        data = {"users":{}}
        addUser(data,"userName","fd5cb51bafd60f6fdbedde6e62c473da6f247db271633e15919bab78a02ee9eb",0)
        addUser(data,"Harry","5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",1)
        json.dump(data, f, indent = 4, ensure_ascii=True)

def addUser(json,user,password=None,admin=0):
    username = "{}!".format(user)
    json["users"][user.lower()] = {"username":username,"password":password,"adminLevel":admin}
    #return(json)

def removeUser(json,user):
    del json["users"][user.lower()]

def check(user,password):
    data = load(FILENAME)
    if user.lower() in data["users"]:
        return(data["users"][user.lower()]["password"] == password)
    else:
        return(True)

if __name__ == "__main__":
    init(FILENAME)
    data = load(FILENAME)
    addUser(data,"greg","testPassword")
    print(data)
    #removeUser(data,"greg")
    print(repr(data["users"]["harry"]["username"]))
