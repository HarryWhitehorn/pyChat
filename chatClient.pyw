#pyChat - client
import socket
import select
import random
import time
import interface, log, login

class GameClient(object):
    def __init__(self, window, log, addr="127.0.0.1", serverport=9009, username="Mix", password=""):
        self.username = username
        self.window = window
        self.log = log
        self.clientport = random.randrange(8000, 8999)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to localhost - set to external ip to connect from other computers
        self.addr = addr
        self.conn.bind((socket.gethostbyname(socket.gethostname()), self.clientport))
        self.conn.connect((self.addr, serverport))
        self.serverport = serverport
        
        self.read_list = [self.conn]
        self.write_list = []
        self.window.root.title("Client - {}".format(self.clientport))

    def run(self):
        running = True
        try:
        # Initialize connection to server
            connectMsg = bytes("{}|{}".format("new",self.username),"utf-8")
            self.conn.sendto(connectMsg, (self.addr, self.serverport))
            while running:
                # select on specified file descriptors
                readable, writable, exceptional = (
                    select.select(self.read_list, self.write_list, [], 0)
                )
                for item in readable:
                    #if item is self.conn:
                    msg = item.recv(2048)
                    msg = msg.decode("utf-8").split("|") 
                    print(msg)
                    self.log.add(*msg)
                    self.window.receive(self.log.data)
                if self.window.sending:
                    data = bytes("{}|{}".format("chat",self.window.data),"utf-8")
                    self.window.sending = False
                    self.conn.sendto(data, (self.addr, self.serverport))
                try:
                    self.window.root.update()
                except interface.tk.TclError:
                    print("user quit (1)")
                    running = False
        finally:
            self.conn.sendto(b"dis", (self.addr, self.serverport))



if __name__ == "__main__":
    valid = False
    while not valid:
        loginW = interface.LoginWindow()
        loginW.root.mainloop()
        data = loginW.data
        username = data["username"]
        password = data["password"]
        serverAddr = data["addr"]
        serverPort = data["port"]
        valid = login.check(username,password)
        print("Login Valid: {}".format(valid))
    log = log.Log()
    window = interface.ChatWindow("Client")
    g = GameClient(window,log,serverAddr,serverPort,username,password)
    g.run()
    print("user quit (0)")