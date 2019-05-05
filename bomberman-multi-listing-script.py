import time

import socket

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
        print("socket.getsockname()",socket.getsockname())
        # (HOST_UDP_server, PORT_UDP_server)
        if(socket.getsockname()[1]==5010):
            print("if(socket.getsockname()[1]==5010):")

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


# trying to figure out the IP on the LAN network
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    # doesn't even have to be reachable
    s.connect(('10.255.255.255', 1))
    IP_on_LAN = s.getsockname()[0]
except:
    IP_on_LAN = '127.0.0.1'
finally:
    s.close()
print("IP_on_LAN", IP_on_LAN)

# HOST_UDP_server, PORT_UDP_server = "0.0.0.0", 5007
HOST_UDP_server, PORT_UDP_server = IP_on_LAN, 5010
server_udp = ThreadedUDPServer((HOST_UDP_server, PORT_UDP_server), ThreadedUDPRequestHandler)
server_thread_udp = threading.Thread(target=server_udp.serve_forever)
server_thread_udp.daemon = True
try:
    # servers
    server_thread_udp.start()
except (KeyboardInterrupt, SystemExit):
    server_thread_udp.shutdown()
    server_thread_udp.server_close()
    exit()


while True:
    print("main server listing for online games")
    print(time.time())
    time.sleep(1)

