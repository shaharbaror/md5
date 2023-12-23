SERVER_ADR = ("127.0.0.1",8000)

class Protocol:
    @staticmethod
    def receive(s) -> bytes:
        msg_len = int(s.recv(4))
        return s.recv(msg_len)

    @staticmethod
    def prepare_send(msg: str) -> bytes:
        msg_len = str(len(msg)).zfill(4)
        return (msg_len + msg).encode()

    @staticmethod
    def get_server_adr():
        return SERVER_ADR
