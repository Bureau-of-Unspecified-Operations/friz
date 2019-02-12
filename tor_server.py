import asyncio
import rsa
from rpcudp.protocol import RPCProtocol


# Start local UDP server to be able to handle responses
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('127.0.0.1', 4567))
transport, protocol = loop.run_until_complete(listen)



class TORServer(RPCProtocol):
    TERMINAL_TUPLE = (0,0)

    def newServer(loop, port, privKey, pubKey):
        listen = loop.create_datagram_endpoint(TORServer, local_addr=('127.0.0.1', port))
        transport, protocol = loop.run_until_complete(listen)
        protocol.port = port
        protocol.privKey = privKey
        protocol.pubKey = pubKey
        return protocol
    
    def rpc_forward(self, sender, packet):
        print(sender)
        print(packet)
        if (isTerminalPacket(packet, privKey)):
            #give message to UI
            pass
        else:
            nextPacket, address = peel(packet)
            forwardPacket(nextPacket, address)
        return "packet recieved"

    @asyncio.coroutine
    def forward(self, protocol, address, data):
        result = yield from protocol.forward(address, data)
        print(result[1] if result[0] else "No response received.")

    #takes (packet, address) rot tuple and forwarads the packet to the address
    def forwardROT(self, packet, address):
        func = self.forward(self, address, packet)
        asyncio.get_event_loop().run_until_complete(func)
        

class TORUtil(object):
    TERMINAL_REV_TOR = (0,0)

    # serverOnion <=> (data_to_send, address)
    #       - data_to_send is what other TOR servers recieve
    # data_to_send <=> (encrypted(ROT), encrypted(payload))
    # payload <=> ROT, encyrpt(message), pubKey
    #    - ROT will let the payload recipient find the caller
    #    - message will be decrypted with the recipients IDprivateKey
    #    - pubKey is the identity key that the caller wants to be reached by in future
    # ROT <=> layered encrypted(ROT'),IP
    #    - you could just send a rot, but DONT, becaues it has no payload


    #generate a revTor that would travel from the end to the beginning of the ORnodes
    def generateRevTor(ORNodes):
        return reduce(TORUtil.wrapRevTor, ORNodes, TERMINAL_ROTOR)

    # payloads can be dead dropped in DHT, or be tagged onto a revTor transmission
    def generatePayload(trgPubKey, revTor, message, replyPubKey):
        bits = str((revTor, message, replyPubKey)).encode.("utf8")
        return rsa.encrypt(bits, trgPubKey)

    def splitPacket(packet):
        encRevTor, payload = ast.literal_eval(packet.decode("utf8"))
        return encRevTor, payload

    def mergeTor(encRevTor, payload):
        return str((encRevTor, payload)).encode("utf8")

    # takes encrypted pyaload, returns (revTor, message, pubKey) tuple
    def splitPayload(payload, privKeyID):
        return ast.literal_eval(rsa.decrypt(payload, privKeyId).decode("utf8"))

    def isTerminalPacket(packet, privKey):
        encRevTor, payload = TORUtil.splitPacket(packet)
        revTor = ast.literal_eval(rsa.decrypt(encRevTor, privKey).decode("utf8"))
        return revTor == TERMINAL_REV_TOR

    # adds another node to revTor
    # revTorn * nodeTuple -> revTor
    def wrapRevTor(revTor, nodeTuple):
        bits = str(revTor).encode("utf8")
        return (rsa.encrypt(bits, nodeTuple[0]), nodeTuple[1])

    # takes packet, unpackes revTor, removes encryption layer, repackages as (packet, address)
    def peel(packet, privKey):
        encRevTor, payload = TORUtil.splitPacket(packet)
        encRevTorPrime, nextAddress = ast.literal(rsa.decrypt(encRevTor, privKey).decode("utf8"))
        return (TORUtil.mergeTor(encRevTorPrime, payload), nextAddress)

    # creates (packet, address) tuple
    def generateTransmission(revTor, payload):
        encRevTor, address = revTor
        return (TORUtil.merge(encRevTor, payload), address)
        


    # packet:
    ######## - rot
    ######## - message
    ########
    # address:
    ######## - IP : string
    ######## - port: int
    #


def newTORServer(loop, port, privKey, pubKey):
    listen = loop.create_datagram_endpoint(TORServer, local_addr=('127.0.0.1', port))
    transport, protocol = loop.run_until_complete(listen)
    protocol.port = port
    protocol.privKey = privKey
    protocol.pubKey = pubKey
    return protocol


'''
class TOR(object):
    TERMINAL_TUPLE = (0,0)
    
    def __init__(self, loop, port):
        listen = loop.create_datagram_endpoint(TORServer, local_addr=('127.0.0.1', port))
        transport, protocol = loop.run_until_complete(listen)
        self.protocol = protocol
        
    @asyncio.coroutine
    def forward(self, protocol, address):
        # result will be a tuple - first arg is a boolean indicating whether a response
        # was received, and the second argument is the response if one was received.
        result = yield from protocol.forward(address, "data")
        print(result[1] if result[0] else "No response received.")

    def forwardTOR(self):
        func = self.forward(self.protocol, ('127.0.0.1', 1234))
        self.loop.run_until_complete(func)

    def forwardPacketSelf(self, packet):
        func = TOR.forward(self.protocol, TOR.addressFromPacket(packet),
                           TOR.dataFromPacket)

    @asyncio.coroutine
    def forward(protocol, address, data):
        result = yield from protocol.forward(address, data)
        print(result[1] if result[0] else "No response received.")


    #takes (packet, address) rot tuple and forwarads the packet to the address
    def forwardROT(protocol, rot):
        func = TOR.forward(protocol, TOR.addressFromROT(rot), TOR.packetFromROT(rot))
        asyncio.get_event_loop().run_until_complete(func)
        

    def isTerminalPacket(packet, priKey):
        return TOR.packetFromROT(TOR.packetUnfold(packet, priKey)) == TOR.TERMINAL_TUPLE

    def addressFromROT(rotTuple):
        return rotTuple[1]

    def packetFromROT(rotTuple):
        return rotTuple[0]

    # nodeTuples take form (pubKey, address)
    # dataTuples is (encryptedROT, addresss)
    # type (dataTuple * nodeTuple) -> (cipherPayload, address)
    def rotFold(dataTuple, nodeTuple):
        s = str(dataTuple).encode("utf8")
        return (rsa.encrypt(s, nodeTuple[0]), nodeTuple[1])

    # type = (cipher, pri) -> rotTuple
    def packetUnfold(cipher, priKey):
        plain = rsa.decrypt(cipher, priKey)
        rot = ast.literal_eval(plain)
        print(TOR.addressFromROT(rot))
        return rot

    def generateROT(pubID, myIP, ORNodes):
        return reduce(TOR.rotFold, ORNodes, TERMINAL_TUPLE)

    def testDecryptROT(rot, ORNodes):
        
        """
