import socket

import struct
def sendOneMulticastAdToLAN():
    # print("sendOneMulticastAdToLAN")
    message = b'bomberman-by-not-sure'
    multicast_group = ('192.168.1.255', 10000)
    # Create the datagram socket
    sock_multicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    sock_multicast.settimeout(0)
    # Set the time-to-live for messages to 1 so they do not
    # go past the local network segment.
    ttl = struct.pack('b', 1)
    sock_multicast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    MY_IP = "192.168.1.255"
    # MY_IP = IP_on_LAN
    # MY_IP = 'localhost'
    sock_multicast.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(MY_IP))
    try:
        # while(range(100,0,-1)):
        # Send data to the multicast group
        # print('sending {!r}'.format(message))
        sent = sock_multicast.sendto(message, multicast_group)
    finally:
        # print('closing socket')
        sock_multicast.close()




import socketserver, threading, time
import socket

# UDP connexion handling
# todo: queuing data that needs processing
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global currentHostsOnLan
        # print("ThreadedUDPRequestHandler:handle")
        data = self.request[0].strip()
        socket = self.request[1]
        print("data",data)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

numberOfLocalPlayers = -1

while True:

    if (numberOfLocalPlayers < 0):
        # is hosting a game
        # pygame.display.set_caption('Bomberman-by-not-sure (Host of Tcp/Ip Game)')

        HOST_UDP_server, PORT_UDP_server = "192.168.1.99", 10000
        # HOST_UDP_server, PORT_UDP_server = IP_on_LAN, 5007
        server_udp = ThreadedUDPServer((HOST_UDP_server, PORT_UDP_server), ThreadedUDPRequestHandler)
        server_thread_udp = threading.Thread(target=server_udp.serve_forever)
        server_thread_udp.daemon = True
        try:
            # servers
            server_thread_udp.start()
            print("server_thread_udp.start()")
        except (KeyboardInterrupt, SystemExit):
            server_thread_udp.shutdown()
            server_thread_udp.server_close()
            exit()
        numberOfLocalPlayers = 1
    print("lol")
    time.sleep(1)
    sendOneMulticastAdToLAN()
    time.sleep(1)