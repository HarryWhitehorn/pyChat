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
    def __init__(self, port=9009, max_num_players=5):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to localhost - set to external ip to connect from other computers
        self.listener.bind(("127.0.0.1", port))
        self.read_list = [self.listener]
        self.write_list = []
    
        self.users = []
        self.data = None

    def run(self):
        print("Running...")
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
                        self.users.remove(addr)
                    elif cmd == "chat":
                        print("User at {} did {}".format(addr,msg))
                        send.append([msg[1],":".join(map(str,addr)),log.time()])
            for user in self.users:
              for item in send:
                print(item)
                sendMessage = '|'.join(item)
                self.listener.sendto(bytes(sendMessage,"utf-8"), user)
#mes,user,time

if __name__ == "__main__":
  g = GameServer()
  g.run()
