#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time, archiver

sys.path.insert(0, '../lib')  # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "Client"
paramMap = params.parseParams(switchesVarDefaults)

arch = archiver.Archiver()
client_file1 = open('../file-lib/space.jpg', 'rb')
client_file2 = open("../file-lib/anna.txt", 'rb')
client_file3 = open('../file-lib/test.txt', 'rb')

arch.add_file(client_file1)
arch.add_file(client_file2)
arch.add_file(client_file3)
file_list = arch.get_file_list()

server, usage = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("Creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print("Attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay'])  # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(int(delay))
    print("done sleeping")


def client_send():
    packed_data = archiver.pack(file_list)
    print("Client Sending: {}".format(packed_data[:50]))
    while len(packed_data):
        bytes_sent = s.send(packed_data)
        packed_data = packed_data[bytes_sent:]

    s.shutdown(socket.SHUT_WR)


def client_recv():
    data = bytearray()
    packet = data
    while 1:
        data = s.recv(200000)
        print("Received Data: {}".format(data[:50]))
        if len(data) == 0:
            arch.add_file_list(archiver.unpack(packet))
            break
        packet += data
    s.close()


client_send()
client_recv()
print(arch.get_file_list())
