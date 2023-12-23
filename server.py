from socket import create_server
from select import select
from protocol import Protocol

CODE = "EC9C0F7EDCC18A98B1F31853B1813301"


class Server:

    def __init__(self, server_adr):
        self.s = create_server(server_adr)
        self.s.listen(9)
        self.clients = {}
        self.running = True

        self.current_num = 0
        self.amp = 50000

    def accept(self):
        print("at here")
        readable, _, _ = select([self.s], [], [], True)
        print("got here")
        if self.s in readable:
            connection, address = self.s.accept()
            self.clients.update({connection: address})
        print("maybe here")

    def respond(self):
        if len(self.clients.keys()) > 0:
            readable, _, _ = select(self.clients.keys(), [], [])

            for client in readable:
                data = Protocol.receive(client).decode()
                print(data)
                if data == "code":
                    client.send(Protocol.prepare_send(CODE))
                elif "ready" in data:
                    num = int(data[5:])
                    print(num)
                    client.send(Protocol.prepare_send(f"{self.current_num} - {self.amp}"))
                    self.current_num = self.current_num + self.amp * num

                elif "found" in data:
                    answer = Protocol.receive(client).decode()
                    print(answer)
                    self.s.sendall(b"0004STOP")

    def run(self):
        while self.running:
            self.accept()

            self.respond()
            print("here")


def main():
    server = Server(('127.0.0.1', 8000))
    server.run()


if __name__ == "__main__":
    main()
