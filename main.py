import hashlib as hl
import socket as s
from multiprocessing import Pool
import os
from protocol import Protocol

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



class Client:
    def __init__(self, path, port):
        self.path = path
        self.port = port
        self.s = s.socket()
        self.connected = False

    def connect_client(self):
        self.s.connect((self.path, self.port))
        self.connected = True

    def get_enc(self) -> str:
        self.s.send(Protocol.set_msg("code").encode())
        msg = Protocol.get_msg(self.s)
        if msg == "close":
            print("here")
            self.connected = False
            self.s.close()


        return msg

    def answer_server(self, found):
        self.s.send(Protocol.set_msg(found).encode())

    @staticmethod
    def brute_force(start, amount, msg) -> int:
        for i in range(start, start + amount + 1):
            print("H")
            if hl.md5(str(i).encode()).hexdigest() == msg:
                return i
        return -1

    def find_code(self, msg):

        self.s.send(Protocol.set_msg(f"ready{os.cpu_count()}").encode())
        num_range = Protocol.get_msg(self.s)

        if num_range == "close":
            self.s.close()
            self.connected = False
            return

        num_range = num_range.split('-')

        with Pool(os.cpu_count()) as p:
            all_results = [p.apply_async(self.brute_force, [int(num_range[0]) + i*250000, 250000, msg]) for i in range(os.cpu_count())]

            for i in all_results:
                res = i.get()
                if res != -1:
                    return res


def main():

    client = Client("127.0.0.1", 8000)
    client.connect_client()
    msg = client.get_enc()
    while client.connected:
        found = client.find_code(msg)

        if found:
            client.answer_server(found)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
