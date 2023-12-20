import socket
from typing import List
from protocol import Protocol

CODE = "534307fa63684bddfc0c813283f4d760"

class Server:
    def __init__(self, path, port, code):
        self.path = path
        self.port = port
        self.s = socket.socket()
        self.clients:List[socket] = []
        self.code = code
        self.inc = 50000
        self.num = 0

    def start_server(self):
        self.s.bind((self.path, self.port))
        self.s.listen(10) # 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

    def accept_clients(self):
        client, addr = self.s.accept()
        self.clients.append(client)
        print("here")

    def manage_clients(self):
        for i in self.clients:
            request = Protocol.get_msg(i)
            print(request)
            if request == "code":
                i.send(Protocol.set_msg(self.code).encode())
            elif request[:5] == "ready":
                print("works")
                cores = request[5:]
                i.send(Protocol.set_msg(f"{self.num} - {self.num + self.inc * cores}").encode())
            elif request != "":
                print("her")
                self.s.sendall(Protocol.set_msg("close").encode())
                print(request)
                self.s.close()


def main():
    server = Server("0.0.0.0", 8000, CODE)
    server.start_server()
    while True:
        server.accept_clients()
        server.manage_clients()

if __name__ == "__main__":
    main()