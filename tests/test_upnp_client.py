# https://github.com/flyte/upnpclient

import upnpclient

devices = upnpclient.discover()

print(devices)

d = devices[0]

print(d.WANIPConn1.GetStatusInfo())

print(d.WANIPConn1.GetExternalIPAddress())

