#! /usr/bin/env python3


import socket, sys, re, os, time, archiver

sys.path.insert(0, '../lib')  # for params
import params

file_name = "test.txt"

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
        conn.send(b"hello")
        time.sleep(0.25);  # delay 1/4s
        conn.send(b"world")
        conn.shutdown(socket.SHUT_WR)
