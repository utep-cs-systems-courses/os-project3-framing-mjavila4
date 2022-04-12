#! /usr/bin/env python3


import socket, sys, re, os, time, archiver, threading

sys.path.insert(0, '../lib')  # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

arch = archiver.Archiver()
server_file1 = open('../file-lib/test.txt', 'r+')
server_file2 = open("../file-lib/anna.txt", "r+")

arch.add_file(server_file1)
arch.add_file(server_file2)

file_list = arch.get_file_list()


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


def client_connection(connection, address):
    print('Connected by', address)

    server_send(connection)
    server_recv(connection)

    connection.shutdown(socket.SHUT_WR)
    connection.close()


def server_send(connection):
    packed_data = archiver.pack(file_list)
    print("Server Sending: {}".format(packed_data))
    while len(packed_data):
        bytes_sent = connection.send(packed_data)
        packed_data = packed_data[bytes_sent:]


def server_recv(connection):
    while 1:
        data = connection.recv(1024)
        if len(data) == 0:
            break
        print("Received Data: {}".format(data))


while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    t = threading.Thread(target=client_connection(conn, addr))
    t.start()
