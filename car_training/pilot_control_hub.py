import socket
import time

class server_commands(object):
    def __init__(self):
        self.server = socket.socket()
        self.server.bind((socket.gethostbyname(socket.gethostname()), 8080))
        self.server.listen(0)
        print(socket.gethostbyname(socket.gethostname()))
        self.conn, addr = self.server.accept()

    def send_data(self, command):
        command = command.encode()
        self.conn.send(command)
        print("Sent")


host_server = server_commands()

while True:
    instru = input("Instruction")
    host_server.send_data(instru)
    if instru == "stop":
        time.sleep(1)
        host_server.server.close()
        break
