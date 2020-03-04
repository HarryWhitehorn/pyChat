#pyChat - commands
import login
data = login.load()

def check(user,adminLevel=1):
    if user[:-1].lower() in data["users"] or user.lower() in data["users"]:
        return(data["users"][user[:-1].lower()]["adminLevel"] >= adminLevel)
    else:
        return(False)

def formatter(message):
    return("send.append(['{}','SERVER',log.time()])".format(message))

#commands
def users(user,users,*args):
    level = 1
    if check(user,level):
        #message = ["{}@{}:{}".format(users[i],i[0],i[1]) for i in users]
        #return("send.append(['{}','SERVER',log.time()])".format(message))
        return("send.append([str(self.users),'SERVER',log.time()])")

    else:
        return(errorAdmin)

def amiadmin(user,*args):
    level = 0
    if check(user,level):
        return(formatter("You are level {}".format(data["users"][user[:-1].lower()]["adminLevel"])))
    else:
        return(formatter("You are level {}".format(0)))

#errors
errorAdmin = formatter('Invaid Permision: You are not admin')


if __name__ == "__main__":
    print(check("testusername"))