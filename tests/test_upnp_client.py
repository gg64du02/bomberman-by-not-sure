# https://github.com/flyte/upnpclient

import upnpclient

devices = upnpclient.discover()

print(devices)

d = devices[0]

# print(d.WANIPConn1.GetStatusInfo())
#
# print(d.WANIPConn1.GetExternalIPAddress())
#
print(d.WANIPConn1.AddPortMapping.argsdef_in)

print(d.WANIPConn1)

print(d.WANIPConn1.AddPortMapping(
    NewRemoteHost='0.0.0.0',
    NewExternalPort=0xff00,
    NewProtocol='TCP',
    NewInternalPort=0xff00,
    NewInternalClient='192.168.1.10',
    NewEnabled='1',
    NewPortMappingDescription='Testing',
    NewLeaseDuration=0xff00ff00)
)


# print(d.WANIPConn1.AddPortMapping(
#     NewRemoteHost='0.0.0.0',
#     NewExternalPort=12345,
#     NewProtocol='TCP',
#     NewInternalPort=12345,
#     NewInternalClient='192.168.1.10',
#     NewEnabled='1',
#     NewPortMappingDescription='Testing',
#     NewLeaseDuration=int(10000))
# )


# print(d.WANIPConn1.AddPortMapping(
#     NewRemoteHost='0.0.0.0',
#     NewExternalPort=12345,
#     NewProtocol='TCP',
#     NewInternalPort=12345,
#     NewInternalClient='192.168.1.10',
#     NewEnabled='1',
#     NewPortMappingDescription='Testing',
#     NewLeaseDuration=10000)
# )