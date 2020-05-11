#!/usr/bin/python3
"""
Simple socket client
"""


import errno
import random
import select
import socket
import string
import sys
import threading
import os

rows, columns = os.popen("stty size", "r").read().split()

def listen_messages(sock, username):
    while True:
        try:
            us_length = int(sock.recv(HEADER_LENGTH).decode('utf-8'))
            us_name = sock.recv(us_length).decode('utf-8')
            mess_length = int(sock.recv(HEADER_LENGTH).decode('utf-8'))
            mess = sock.recv(mess_length).decode("utf-8")
            us = '\033[34m' + username.decode('utf-8') + '\033[0m'
            mess = '\033[0m' + mess + ' : ' + '\033[33m' + us_name + '\033[0m'
            if len(mess) > int(columns):
                start = 0
                end = int(columns) - 2
                while start < len(mess):
                    fin = False
                    if end > len(mess):
                        end = len(mess)
                        fin = True
                    chunk = mess[start:end]
                    start = end
                    end = end + int(columns) - 1
                    if fin:
                        print('\r{chunk:>{div}}\n{us} > '.format(chunk=chunk, div=int(columns), us=us), end='')
                        break
                    else:
                        print('\r{chunk:>{div}}'.format(chunk=chunk, div=int(columns)))
            else:
                print('\r{mess:>{div}}\n{me} > '.format(mess=mess,
                                                              div=int(columns),
                                                              me=us), end='')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print(str(e))
                sys.exit()
            continue
        except Exception as e:
            print(str(e))
            sys.exit()

def input_send(sock, username):
    while True:
        message = input("\033[34m{}\033[0m > ".format(username.decode('utf-8')))
        if message:
            message = message.encode('utf-8')
            mess_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            sock.send(mess_header + message)


HEADER_LENGTH = 10


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# the ip for the Server
ip = socket.gethostname()
# the port to be talk to
port = 1234

sock.connect((ip, port))
sock.setblocking(False)

user = "User" + str(random.choice(string.digits))
username = user.encode('utf-8')

us_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
print("Username:", username.decode('utf-8'))
sock.send(us_header + username)

input_thread = threading.Thread(target=input_send, args=(sock, username))
input_thread.start()
mess_thread = threading.Thread(target=listen_messages, args=(sock, username))
mess_thread.start()
