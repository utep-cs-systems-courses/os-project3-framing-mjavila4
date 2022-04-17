#! /usr/bin/env python3


import socket, sys, re, os, time, archiver, threading

sys.path.insert(0, '../lib')  # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

arch = archiver.Archiver()
server_file1 = open('../file-lib/test.txt', 'rb')
#server_file2 = open("../file-lib/anna.txt", 'rb')
#server_file3 = open("../file-lib/rplace.jpg", 'rb')

arch.add_file(server_file1)
#arch.add_file(server_file2)
#arch.add_file(server_file3)

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
    print("Server Sending: {}".format(packed_data[:50]))
    while len(packed_data):
        bytes_sent = connection.send(packed_data)
        packed_data = packed_data[bytes_sent:]


def server_recv(connection):
    data = bytearray()
    packet = data
    while 1:
        data = connection.recv(150000)
        print("Received Data: {}".format(data[:50]))
        if len(data) == 0:
            arch.add_file_list(archiver.unpack(packet))
            break
        packet += data
        print("Sleeping...")
        time.sleep(int(1))


while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    t = threading.Thread(target=client_connection(conn, addr))
    t.start()
    print(arch.get_file_list())
