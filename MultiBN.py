# MultiBN constants

MBN_TCP_CLIENT_JOIN_REQUIRED = 0
# Used by the client to require to join a game
# Used by the server to check if a new client can join (any room left ?)
MBN_TCP_SERVER_JOIN_REFUSED = 1
# Used by the server to answer to MBN_TCP_CLIENT_JOIN_REQUIRED to refuse a join (Client drop the connexion)
MBN_TCP_SERVER_JOIN_ACCEPTED = 2
# Used by the server to answer to MBN_TCP_CLIENT_JOIN_REQUIRED to accept a join


MBN_SESSION_TCP_SERVER_NUMBER_OF_AVAILABLE_PLAYERS_SLOTS = 3
# Used by the server to let know the clients how many local players there are left (after MBN_TCP_SERVER_JOIN_ACCEPTED)

MBN_SESSION_TCP_CLIENT_NUMBER_OF_LOCAL_PLAYERS = 4
# Used by the client to answer to MBN_SESSION_TCP_SERVER_NUMBER_OF_AVAILABLE_PLAYERS_SLOTS to let know the server how many
# local players there are

MBN_SESSION_TCP_CLIENT_PLAYERS_ARE_READY = 5
# Used by the client to (after MBN_TCP_SERVER_JOIN_ACCEPTED) to let know the players' client are ready

MBN_SESSION_TCP_SERVER_BEFORE_COUNTDOWN_FIRST_ROUND = 6
# Used by the server to if the UDP packets can ping at least once per client

MBN_SESSION_TCP_SERVER_COUNTDOWN_FIRST_ROUND = 7
# Used by the server to tell the client to prepare processing the incoming UDP packets about the game info.

MBN_SESSION_TCP_SERVER_TRANSMIT_MAP = 8
# Used by the server to transmit the map to the clients

MBN_SESSION_TCP_SERVER_PING = 9
# Used by the client let know the server he is still online


# datagram shape
# data|data type|data|crc
MBN_CON_UDP_CLIENT_DATA = 100
MBN_CON_UDP_CLIENT_DATA_LOOP_START = 101
MBN_CON_UDP_CLIENT_DATA_LOOP_END = 102
MBN_CON_UDP_CLIENT_DATA_LOOP_NUMBER = 103
MBN_CON_UDP_CLIENT_DATA_PING = 104

# time in ms
MBN_CON_UDP_CLIENT_DATA_PING_MS = 5000