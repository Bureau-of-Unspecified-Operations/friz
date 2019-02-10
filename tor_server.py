import asyncio
import rsa
from rpcudp.protocol import RPCProtocol


# Start local UDP server to be able to handle responses
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('127.0.0.1', 4567))
transport, protocol = loop.run_until_complete(listen)



class TORServer(RPCProtocol):
    def rpc_forward(self, sender, data):
        print(sender)
        print(data)
        if TOR.isTorPacket(data):
            TOR.forwardPacket(data, self)
        return "packet recieved"
    
class TOR(object):
    END_OF_TOR_PATH = 0
    
    def __init__(self, loop, port):
        listen = loop.create_datagram_endpoint(TORServer, local_addr=('127.0.0.1', port))
        transport, protocol = loop.run_until_complete(listen)
        self.protocol = protocol
        '''
    @asyncio.coroutine
    def forward(self, protocol, address):
        # result will be a tuple - first arg is a boolean indicating whether a response
        # was received, and the second argument is the response if one was received.
        result = yield from protocol.forward(address, "data")
        print(result[1] if result[0] else "No response received.")

    def forwardTOR(self):
        func = self.forward(self.protocol, ('127.0.0.1', 1234))
        self.loop.run_until_complete(func)
'''
    def forwardPacketSelf(self, packet):
        func = TOR.forward(self.protocol, TOR.addressFromPacket(packet),
                           TOR.dataFromPacket)

    @asyncio.coroutine
    def forward(protocol, address, data):
        result = yield from protocol.forward(address, data)
        print(result[1] if result[0] else "No response received.")

    def forwardPacket(protocol, packet):
        #extract shit
        func = TOR.forward(protocol, address, data)
        asyncio.get_event_loop().run_until_complete(func)
        

    def isTorPacket(packet):
        return True

    def addressFromROT(rotTuple):
        return rotTuple[1]

    def cipherFromROT(rotTuple):
        return rotTuple[0]

    # nodeTuples take form (pubKey, address)
    # dataTuples is (encryptedROT, addresss)
    # type (dataTuple * nodeTuple) -> (cipherPayload, address)
    def rotFold(dataTuple, nodeTuple):
        s = str(dataTuple).encode("utf8")
        return (rsa.encrypt(s, nodeTuple[0]), nodeTuple[1])

    # type = (rotTuple, pub) -> rotTuple
    def rotUnfold(rotTuple, pubKey):
        plain = rsa.decrypt(TOR.cipherFromROT(rotTuple), pubKey)
        rot = ast.literal_eval(plain)
        print(TOR.addressFromROT(rot))
        return rot

    def generateROT(pubID, myIP, ORNodes):
        return reduce(TOR.rotFold, ORNodes, (END_OF_TOR_PATH,END_OF_TOR_PATH))

    def testDecryptROT(rot, ORNodes):
        
        



'''
class T(object):

    def __init__(self, loop, port):
        self.loop = loop
        listen = self.loop.create_datagram_endpoint(TORServer,
                                                     local_addr=('127.0.0.1', port))
        transport, protocol = self.loop.run_until_complete(listen)
        self.protocol = protocol
    @asyncio.coroutine
    def forward(self, protocol, address):
        result = yield from protocol.forward(address, "thiskid")
        print(protocol)
        print(result[1] if result[0] else "No response received.")

    def genSelfPort(self):
        return 6789

    def forwardTOR(self, ip, port):
        func = self.forward(self.protocol, ("128.237.160.131", 6789))
        self.loop.run_until_complete(func)    
'''
