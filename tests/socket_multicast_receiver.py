# socket_multicast_receiver.py
import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)
# server_address = ("192.168.1.1", 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
print("socket.INADDR_ANY",socket.INADDR_ANY)
# mreq = struct.pack('4sL', group, socket.INADDR_ANY)
# mreq = struct.pack('4sL', group, socket.inet_aton("192.168.1.99"))
# sock.setsockopt(
#     socket.IPPROTO_IP,
#     socket.IP_ADD_MEMBERSHIP,
#     mreq)
MY_IP= "192.168.1.99"

sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 2)
sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(MY_IP))

# Receive/respond loop
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)

    print('received {} bytes from {}'.format(
        len(data), address))
    print(data)

    print('sending acknowledgement to', address)
    sock.sendto(b'ack', address)