'''import asyncio
from rpcudp.protocol import RPCProtocol
from tor_server import TOR

loop = asyncio.get_event_loop()
tor = TOR(loop, 7899)
tor.forwardTOR("",0)
loop.run_forever()
'''

import asyncio
from rpcudp.protocol import RPCProtocol
from tor_server import TOR



# Start local UDP server to be able to handle responses


# Call remote UDP server to say hi
loop = asyncio.get_event_loop()
t = TOR(loop, 4567)
t.forwardTOR()
loop.run_forever()


