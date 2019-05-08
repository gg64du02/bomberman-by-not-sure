import time

import socket

import socketserver, threading, time
import socket
import pickle

# TCP connexion handling
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("ThreadedTCPRequestHandler:handle")
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("self.client_address",self.client_address)
        # print("ThreadedTCPRequestHandler: {} wrote:".format(self.client_address[0]))
        print("self.data",self.data)
        dataFromPickle = self.data
        print("dataFromPickle",dataFromPickle)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
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
server_udp = ThreadedTCPServer((HOST_UDP_server, PORT_UDP_server), ThreadedTCPRequestHandler)
server_thread_udp = threading.Thread(target=server_udp.serve_forever)
server_thread_udp.daemon = True
try:
    # servers
    server_thread_udp.start()
except (KeyboardInterrupt, SystemExit):
    server_thread_udp.shutdown()
    server_thread_udp.server_close()
    exit()

# https://github.com/flyte/upnpclient
import upnpclient
devices = upnpclient.discover()
# debugging  purpose
# print(devices)
d = devices[0]
def addUPnPrule(port,internal_ip,udp_tcp=('UDP'or'TCP')):
    print('def addUPnPrule(port,internal_ip):')
    print('udp_tcp',udp_tcp)
    tmplol = d.WANIPConn1.AddPortMapping(
    # NewRemoteHost='192.168.1.99',
    # pro tip: never thrust the error output coming from the upnp device,
    # it could name a problem that is not the actual problem
    NewRemoteHost='',
    NewExternalPort=int(port),
    NewProtocol=udp_tcp,
    NewInternalPort=int(port),
    NewInternalClient=internal_ip,
    NewEnabled='true',
    NewPortMappingDescription='BombermanByNotSure',
    NewLeaseDuration=10000)
    if(bool(tmplol)==False):
        print('addUPnPrule')
    else:
        print('!addUPnPrule')

def removeUPnPrule(port,udp_tcp=('UDP'or'TCP')):
    print('def removeUPnPrule(port):')
    print('udp_tcp',udp_tcp)
    tmplol = d.WANIPConn1.DeletePortMapping(
    # pro tip: never thrust the error output coming from the upnp device,
    # it could name a problem that is not the actual problem
    NewRemoteHost='',
    NewExternalPort=int(port),
    NewProtocol=udp_tcp)
    if(bool(tmplol)==False):
        print('removeUPnPrule')
    else:
        print('!removeUPnPrule')
# testing purposes
# removeUPnPrule()
# testing purposes
# addUPnPrule()


# 5010 is used by the servers to declare themself and ask the listing (the clients would)
addUPnPrule(5010,IP_on_LAN,'TCP')

# main server
# <- "declare" IP,port |Server|
# -> 'OK' |Server|

# main server
# <- 'list' |Client|
# ->'list of' |Client|

while True:
    print("main server listing for online games")
    print(time.time())
    time.sleep(10)

removeUPnPrule(5010,'TCP')