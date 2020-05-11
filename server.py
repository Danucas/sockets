#!/usr/bin/python3
"""
Handles client conections and responses

needs to be called from a API
https://dnart.tech/chat_room?state=new
"""

import socket
import select


HEADER_LENGTH = 10


class SocketServer:
    """
    Define socket for the sever to listen to the given port
    """
    def __init__(self, port, _id):
        self.sock = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1)
        self.sock.bind(('0.0.0.0', port))
        print("Binded to: ", '0.0.0.0', "on port", port)
        self.socket_list = [self.sock]
        self.clients = {}
        self.sock.listen()
        self.id = _id
        self.main_loop()

    def receive_msg(self, client_sock):
        """
        Receives a message by the given client_sock
        """
        try:
            message_header = client_sock.recv(HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8'))
            data = client_sock.recv(message_length)
            return {"header": message_header, "data": data}
        except Exception as e:
            print(str(e))
            return False


    def main_loop(self):
        """
        start listening for incoming comunication
        """
        while True:
            r_socks, _, excep_sock = select.select(self.socket_list,
                                                   [],
                                                   self.socket_list)
            for noti_sock in r_socks:
                if noti_sock == self.sock:
                    cli_sock, cli_addr = self.sock.accept()
                    user = self.receive_msg(cli_sock)
                    print(user)
                    if user is False:
                        continue
                    self.socket_list.append(cli_sock)
                    self.clients[cli_sock] = user
                    print("Accepting conection from {}".format(cli_addr))
                    print("Username: {}".format(user["data"]))
                    print("\tClients:", self.clients)
                    data = "Say Hello to".encode('utf-8')
                    header = "{data:<{lent}}".format(data=len(data),
                                                     lent=HEADER_LENGTH).encode('utf-8')
                    try:
                        for cli in self.clients:
                            if cli != cli_sock:
                                cli.send(user['header'] +\
                                         user['data'] +\
                                         header +\
                                         data)
                    except Exception as e:
                        print(e)
                else:
                    message = self.receive_msg(noti_sock)
                    if message is False:
                        con = self.clients[noti_sock]['data'].decode('utf-8')
                        print("Close connection from {}".format(con))
                        self.socket_list.remove(noti_sock)
                        del self.clients[noti_sock]
                        continue
                    user = self.clients[noti_sock]
                    print("Received message from {}".format(user['data']))
                    print("Message: {}".format(message['data']))
                    for cli_sock in self.clients:
                        if cli_sock != noti_sock:
                            cli_sock.send(user['header'] +\
                                          user['data'] +\
                                          message['header']+\
                                          message['data'])
            for noti_sock in excep_sock:
                self.socket_list.remove(noti_sock)
                del self.clients[noti_sock]
