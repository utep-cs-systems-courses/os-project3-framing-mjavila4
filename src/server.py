#! /usr/bin/env python3


import socket, sys, re, os, time, archiver

sys.path.insert(0, '../lib')  # for params
import params

file1 = open('../file-lib/test.txt', 'r')
file_array = {file1}

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

while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    if os.fork() == 0:  # child becomes server
        print('Connected by', addr)
        packed_data = archiver.pack(file_array)
        print("Server Sending {}".format(packed_data))
        conn.send(data)
        conn.shutdown(socket.SHUT_WR)
