import asyncio
from rpcudop.protocol import RPCProtocol
from tor_server import TORServer
import rsa

loop = asyncio.get_event_loop()
(pub, priv) = rsa.newKeys(512)
port = 5678
server = TORServer.newServer(loop, port, priv, pub)
