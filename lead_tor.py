'''import asyncio
from rpcudp.protocol import RPCProtocol
from tor_server import TOR

loop = asyncio.get_event_loop()
tor = TOR(loop, 6789)
loop.run_forever()
'''


import asyncio
from rpcudp.protocol import RPCProtocol
from tor_server import  TOR



# start a server on UDP port 1234
loop = asyncio.get_event_loop()
t = TOR(loop, 1234)
loop.run_forever()
