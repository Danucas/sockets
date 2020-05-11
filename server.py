#!/usr/bin/python3
"""
Handles client conections and responses

needs to be called from a API
https://dnart.tech/chat_room?state=new
"""

import socket
import select

HEADER_LENGTH = 10
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1)
sock.bind((socket.gethostname(), 1234))
print("Binded to: ", socket.gethostname(), "on port", 1234)
sock.listen()

socket_list = [sock]
clients = {}


def receive_msg(client_sock):
    """
    Receives a message by the given client_sock
    """
    try:
        message_header = client_sock.recv(HEADER_LENGTH)
        # print("Message header:", message_header)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8'))
        data = client_sock.recv(message_length)
        # print("data: ", data)
        return {"header": message_header, "data": data}
    except Exception as e:
        print(str(e))
        return False

while True:
    r_socks, _, excep_sock = select.select(socket_list,
                                           [],
                                           socket_list)
    for noti_sock in r_socks:
        # print(str(noti_sock))
        # print(str(sock))
        if noti_sock == sock:
            # print("Server socket")
            cli_sock, cli_addr = sock.accept()
            user = receive_msg(cli_sock)
            print(user)
            if user is False:
                continue
            socket_list.append(cli_sock)
            clients[cli_sock] = user
            print("Accepting conection from {}".format(cli_addr))
            print("Username: {}".format(user["data"]))
        else:
            message = receive_msg(noti_sock)

            if message is False:
                print("Close connection from {}".format(clients[noti_sock]['data'].decode('utf-8')))
                socket_list.remove(noti_sock)
                del clients[noti_sock]
                continue
            user = clients[noti_sock]
            print("Received message from {}".format(user['data']))
            print("Message: {}".format(message['data']))

            for cli_sock in clients:
                if cli_sock != noti_sock:
                    cli_sock.send(user['header'] +\
                                  user['data'] +\
                                  message['header']+\
                                  message['data'])
    for noti_sock in excep_sock:
        socket_list.remove(noti_sock)
        del clients[noti_sock]
