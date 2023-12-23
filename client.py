import hashlib
from multiprocessing import Pool
import os
import socket
from protocol import Protocol
from typing import List


class Client:
    def __init__(self):
        self.s = socket.socket()
        self.s.connect(Protocol.get_server_adr())
        self.connected = True
        self.cpus = os.cpu_count()

    def get_code(self):
        self.s.send(Protocol.prepare_send("code"))
        return Protocol.receive(self.s).decode()

    def get_numbers(self):
        self.s.send(Protocol.prepare_send(f"ready{self.cpus}"))
        return Protocol.receive(self.s).decode()

    @staticmethod
    def find_answer(num_range: List[int], code: str) -> str:

        for i in range(num_range[0], num_range[0] + num_range[1]):

            if hashlib.md5(str(i).encode()).hexdigest() == code:
                return str(i)
        return ""

    def send_answer(self, answer):
        self.s.send(Protocol.prepare_send("found"))
        self.s.send(Protocol.prepare_send(answer))
        self.connected = False

    def run(self, code):
        while self.connected:
            num_range = self.get_numbers().split("-")
            print(num_range)

            if num_range == "STOP":
                self.connected = False
                break

            # create a pool of workers
            with Pool(processes=self.cpus) as pool:
                multiple_results = [pool.apply_async(self.find_answer, args=([int(num_range[0]) + i*int(num_range[1]), int(num_range[1])], code)) for i in range(self.cpus)]
                print([res.get() for res in multiple_results])
                for res in multiple_results:
                    if res.get() != "":
                        self.send_answer(res.get())


def main():
    client = Client()
    code = client.get_code()

    if code != "STOP":
        client.run(code)

    client.s.close()


if __name__ == "__main__":
    main()

