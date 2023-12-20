import socket


class Protocol:

    @staticmethod
    def set_msg(msg: str) -> str:
        msg_len = str(len(msg)).zfill(4)
        return msg_len + msg

    @staticmethod
    def get_msg(s):
        msg_len = int(s.recv(4))
        return s.recv(msg_len).decode()