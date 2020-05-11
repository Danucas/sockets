#!/usr/bin/python3

from flask import Flask, request, jsonify
import socket
import random
from contextlib import closing
from server import SocketServer
import threading
import string
import os
import json


app = Flask(__name__)



def new_socket(port, _id):
    """
    Threading the new socket
    """
    try:
        with open("sockets.json", "r") as socks:
            sockets = json.loads(socks.read())
    except Exception as e:
        sockets = {}
    with open("sockets.json", "w") as socks:
        sockets[_id] = port
        socks.write(json.dumps(sockets))
    sock = SocketServer(port, _id)

def check_id(_id):
    """
    Check if a socket exists by it's id
    """
    try:
        with open("sockets.json", "r") as sock:
            js = json.loads(sock.read())
            if _id in js:
                port = js[_id]
            return port
    except:
        return False


def check_socket(port, _id):
    """
    check if a port is already open
    """
    host = '0.0.0.0'
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            print("Port is open")
            return False
        else:
            print("Port is close")
            socket_thread = threading.Thread(target=new_socket, args=(port,_id,))
            socket_thread.daemon = True
            socket_thread.start()
            return True


@app.route("/api/v1/chat_room", methods=['POST'])
def new_chat():
    """
    Creates a new chat room
    """
    try:
        parms = request.json
        while True:
            port = random.randint(999, 9999)
            list_a = string.ascii_letters +\
                     string.digits
            _id = ''.join(random.choice(list_a) for i in range(16))
            if check_socket(port, _id) is True:
                return jsonify({"port": port, "id": _id})
    except Exception as e:
        print(e)

@app.route("/api/v1/chat_room", methods=['GET'])
def join_room():
    """
    return the port for the specified id
    """
    js = request.json
    print(js)
    _id = js["id"]
    port = check_id(_id)
    if port is False:
        return jsonify({"port": "No port"})
    return jsonify({"port": port, "id": _id})


if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
