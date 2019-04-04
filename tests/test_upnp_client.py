# https://github.com/flyte/upnpclient

import upnpclient

devices = upnpclient.discover()

print(devices)

d = devices[0]

# use the debug in pyCharm here to see what is available
print(d.WANIPConn1.GetStatusInfo())

print(d.WANIPConn1.GetExternalIPAddress())

print(d.WANIPConn1.AddPortMapping.argsdef_in)

print(d.WANIPConn1.GetExternalIPAddress())

print(d.WANIPConn1)

# print(d.WANIPConn1.AddPortMapping(
#     # NewRemoteHost='192.168.1.99',
#     # pro tip: never thrust the error output coming from the upnp device,
#     # it could name a problem that is not the actual problem
#     NewRemoteHost='',
#     NewExternalPort=int(5010),
#     NewProtocol='TCP',
#     NewInternalPort=int(5010),
#     NewInternalClient='192.168.1.99',
#     NewEnabled='true',
#     NewPortMappingDescription='Testing',
#     NewLeaseDuration=10000)
# )

print(d.WANIPConn1.DeletePortMapping(
    # NewRemoteHost='192.168.1.99',
    # pro tip: never thrust the error output coming from the upnp device,
    # it could name a problem that is not the actual problem
    NewRemoteHost='',
    NewExternalPort=int(5010),
    NewProtocol='TCP')
)

