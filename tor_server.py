import asyncio
import rsa
from rpcudp.protocol import RPCProtocol


# Start local UDP server to be able to handle responses
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('127.0.0.1', 4567))
transport, protocol = loop.run_until_complete(listen)



class TORServer(RPCProtocol):
    def newServer(loop, port, privKey, pubKey, appNode):
        listen = loop.create_datagram_endpoint(TORServer, local_addr=('127.0.0.1', port))
        transport, protocol = loop.run_until_complete(listen)
        protocol.port = port
        protocol.privKey = privKey
        protocol.pubKey = pubKey
        protocol.appNode = appNode
        return protocol
    
    def rpc_forward(self, sender, packet):
        print(sender)
        print(packet)
        if (TORUtil.isTerminalPacket(packet, privKey)):
            encRevTor, payload = TORUtil.splitPacket(packet)
            self.appNode.openPayload(payload)
        else:
            nextPacket, address = TORUtil.peel(packet)
            self.forwardPacket(nextPacket, address)
        return "packet recieved"

    @asyncio.coroutine
    def forward(self, protocol, address, data):
        result = yield from protocol.forward(address, data)
        print(result[1] if result[0] else "No response received.")

    #takes (packet, address) rot tuple and forwarads the packet to the address
    def forwardPacket(self, packet, address):
        func = self.forward(self, address, packet)
        asyncio.get_event_loop().run_until_complete(func)
        

class TORUtil(object):
    TERMINAL_REV_TOR = (0,0)

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



