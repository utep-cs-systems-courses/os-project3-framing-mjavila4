#! /usr/bin/env python3


import socket, sys, re, os, time, archiver, threading, stream_reader

sys.path.insert(0, '../lib')  # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

arch = archiver.Archiver()
server_file1 = open('../file-lib/test.txt', 'rb')

arch.add_file(server_file1)

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
    sr = stream_reader.StreamReader()
    while 1:
        data = connection.recv(100000)
        file_name = sr.listen(data)
        if file_name != 0:
            for f in file_name:
                if arch.file_name_check(f):
                    return
                arch.add_file_name_list(f)
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
    print(arch.get_file_name_list())
