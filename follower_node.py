import asyncio
from kademlia.network import Server
from peer import DHTNode

loop = asyncio.get_event_loop()
node = DHTNode(loop)
node.testKeyPut()
