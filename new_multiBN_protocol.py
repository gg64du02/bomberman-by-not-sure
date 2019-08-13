# MultiBN constants



MBN_TCP_CLIENT_JOIN_REQUIRED = 0
# Used by the client to require to join a game
# Used by the server to check if a new client can join (any room left ?)
MBN_TCP_SERVER_JOIN_REFUSED = 1
# Used by the server to answer to MBN_TCP_CLIENT_JOIN_REQUIRED to refuse a join (Client drop the connexion)
MBN_TCP_SERVER_JOIN_ACCEPTED = 2
# Used by the server to answer to MBN_TCP_CLIENT_JOIN_REQUIRED to accept a join


# MBN_SESSION
# client: MBN_JOIN_REQUIRED
# server: MBN_JOIN_REFUSED
# server: MBN_JOIN_ACCEPTED
#
# MBN_DATA or SESSION ?
# server:SERVER_SLOTS_MAPPING
# client:DATA_PING_MS
# server:NUMBER_OF_AVAILABLE_PLAYERS_SLOTS
# server/client:,players,controls,items,bombs
# server/client:map



