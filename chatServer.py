#pyChat - server
import socket
import select
import sys
import log

# Messages:
#  Client->Server
#   One or two characters. First character is the command:
#     c: connect
#     u: update position
#     d: disconnect
#   Second character only applies to position and specifies direction (udlr)
#
#  Server->Client
#   '|' delimited pairs of positions to draw the players (there is no
#     distinction between the players - not even the client knows where its
#     player is.

class GameServer(object):
    def __init__(self, addr="127.0.0.1", port=9009):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.hostAddr = addr
        self.hostPort = port
        # Bind to localhost - set to external ip to connect from other computers
        self.listener.bind((self.hostAddr, self.hostPort))
        self.read_list = [self.listener]
        self.write_list = []
    
        self.users = []
        self.data = None

    def run(self):
        print("Running on '{}:{}'...".format(self.hostAddr,self.hostPort))
        while True:
            send = []
            readable, writable, exceptional = (select.select(self.read_list, self.write_list, []))
            for item in readable:
                if item is self.listener:
                    msg, addr = item.recvfrom(64)
                    msg = msg.decode("utf-8").split("|")
                    cmd = msg[0]
                    if cmd == "new":
                        print("New connection at {}".format(addr))
                        send.append(["'{}' connected".format(":".join(map(str,addr))),"SERVER",log.time()])
                        self.users.append(addr)
                    elif cmd == "dis":
                        print("User at {} disconnected".format(addr))
                        send.append(["'{}' disconnected".format(":".join(map(str,addr))),"SERVER",log.time()])
                        if addr in self.users: self.users.remove(addr)
                    elif cmd == "chat":
                        print("User at {} did {}".format(addr,msg))
                        send.append([msg[1],":".join(map(str,addr)),log.time()])
            for user in self.users:
              for item in send:
                print(item)
                sendMessage = '|'.join(item)
                self.listener.sendto(bytes(sendMessage,"utf-8"), user)

if __name__ == "__main__":
  g = GameServer()
  g.run()
