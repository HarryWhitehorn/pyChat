#pyChat - log
from time import gmtime

def time():
        now = gmtime()
        year, month, day, hour, minute, second, wday, yday, huh = now
        return("<{}/{}/{},{}:{}:{}>".format(day,month,year,hour,minute,second))

class Log:
    def __init__(self):
        self.data = ""
    
    def add(self,message,user,time=None):
        if time == None:
            time = "<Error noTime>"
                #+=
        self.data = "{} '{}': {}\n".format(time,user,message)

    def time(self):
        now = gmtime()
        year, month, day, hour, minute, second, wday, yday, huh = now
        return("<{}/{}/{},{}:{}:{}>".format(day,month,year,hour,minute,second))

if __name__ == "__main__":
    log = Log()
    log.add("hello","alex")
    print(log.data)
    log.add("hi","josh")
    print("-------")
    print(log.data)
