#! /usr/bin/env python3


import socket, sys, re, os, time, archiver, threading

sys.path.insert(0, '../lib')  # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "Server"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''  # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)  # allow only one outstanding request


# s is a factory for connected sockets


def client_connection(files):
    print('Connected by', addr)
    packed_data = archiver.pack(files)
    print("Server Sending {}".format(packed_data))
    conn.send(packed_data)
    conn.shutdown(socket.SHUT_WR)


def get_files():
    f_list = []
    file1 = open('../file-lib/test.txt', 'r')
    f_list.append(file1)
    return f_list


while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    file_list = get_files()
    t = threading.Thread(target=client_connection(file_list))
    t.start()
