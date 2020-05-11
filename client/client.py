#!/usr/bin/python3
"""
Simple socket client
"""


import pyaudio
import wave
import errno
import random
import select
import socket
import string
import sys
import threading
import os
import json
import uuid
import requests
import subprocess as s

rows, columns = os.popen("stty size", "r").read().split()
HEADER_LENGTH = 10


class SocketClient():
    """
    Defines a socket client that listen for messages and send too
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # the ip for the Server
        self.ip = '35.231.236.18'
        # self.ip = socket.gethostname()
        # the port to be talk to
        self.user = self.check_installed_user()
        self.name = self.user["username"].encode('utf-8')
        print("Welcome!! ", self.name.decode('utf-8'))
        print("To quit type '-logout'")
        print('---------------------')
        print("Select any option")
        print('---------------------')
        print("\t0-Create a chatroom")
        print("\t1-Join an existing chatroom")
        print("\t2-Delete user")
        choice = input("(default 0): ")
        if choice == '0' or choice == '':
            self.create_room()
        elif choice == '1':
            self.join_room()
        elif choice == '2':
            self.delete_user()


    def create_room(self):
        """
        Call the ip and receive an id for the socket connection
        """
        data = {}
        data["user"] = self.user
        data["state"] = "new"
        heads = {}
        heads["Content-Type"] = "application/json"
        url = "http://web-01.dnart.tech:5000/api/v1/chat_room"
        resp = requests.post(url, json=data, headers=heads)
        print("\tChat room created\n\t(Id): {}".format(resp.json()["id"]))
        print("\t\033[33mShare this id with yours peers\033[0m")
        self.id = resp.json()["id"]
        port = resp.json()["port"]
        # wait = input("Continue? > ")
        self.run(resp.json())


    def join_room(self):
        """
        Request to join an existing room
        """
        _id = input("Chat room id> ")
        data = {"id": _id}
        heads = {"Content-Type": "application/json"}
        url = "http://web-01.dnart.tech:5000/api/v1/chat_room"
        resp = requests.get(url, json=data, headers=heads)
        # wait = input("Continue? > ")
        self.run(resp.json())


    def run(self, js):
        """
        Runs a chat room
        """
        port = js["port"]
        try:
            self.sock.connect((self.ip, port))
            print("connected to {}".format(js['id']))
            print("________________________________")
            self.sock.setblocking(False)
            us_header = f"{len(self.name):<{HEADER_LENGTH}}".encode('utf-8')
            self.sock.send(us_header + self.name)
            self.running = threading.Event()
            self.running.set()
            self.input_thread = threading.Thread(target=self.input_send,
                                                 args=(self.sock,
                                                       self.name))
            self.input_thread.start()
            self.mess_thread = threading.Thread(target=self.listen_messages,
                                                args=(self.sock,
                                                      self.name))
            self.mess_thread.start()
        except Exception as e:
            print(e)
            print("Unable to connect")
            sys.exit()


    def listen_messages(self, sock, username):
        """
        This thread listen for incomming messages
        """
        while True:
            try:
                us_length = int(sock.recv(HEADER_LENGTH).decode('utf-8'))
                us_name = sock.recv(us_length).decode('utf-8')
                mess_length = int(sock.recv(HEADER_LENGTH).decode('utf-8'))
                mess = sock.recv(mess_length).decode("utf-8")
                us = '\033[34m' + username.decode('utf-8') + '\033[0m'
                mess = '\033[0m' + mess + ' : ' +\
                       '\033[33m' + us_name + '\033[0m'
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
                            noti = mess
                            noti = noti.replace("\033[0m", "")
                            noti = noti.replace("\033[33m", "")
                            s.call(['notify-send', noti])
                            break
                        else:
                            print('\r{chunk:>{div}}'.format(chunk=chunk, div=int(columns)))
                else:
                    noti = mess
                    noti = noti.replace("\033[0m", "")
                    noti = noti.replace("\033[33m", "")
                    s.call(['notify-send', noti])
                    print('\r{mess:>{div}}\n{me} > '.format(mess=mess,
                                                              div=int(columns),
                                                              me=us), end='')

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Quit")
                    # print(str(e))
                    sys.exit()
                continue
            except Exception as e:
                print("Quit")
                # print(str(e))
                sys.exit()

    def input_send(self, sock, username):
        """
        This thread takes input from the user and send it to the channel
        """
        while True:
            message = input("\033[34m{}\033[0m > ".format(username.decode('utf-8')))
            if message:
                if message == "-logout":
                    self.running.clear()
                    self.mess_thread.join()
                    self.input_thread.join()
                    self.sock.close()
                    break
                message = message.encode('utf-8')
                mess_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                self.sock.send(mess_header + message)


    def check_installed_user(self):
        """
        check if the user is already created in json file
        """
        try:
            with open("config.json", "r") as f:
                fil = json.loads(f.read())
                print(json.dumps(fil, indent=2, sort_keys=True))
                return fil
        except Exception as e:
            print("User not found")
            while True:
                user = input("Please type a new Username: ")
                us = {"username": user,"uuid": str(uuid.uuid4())}
                if user != '':
                    with open("config.json", "w") as f:
                        f.write(json.dumps(us))
                    return us
                else:
                    print("Warning: Empty username is not valid")
