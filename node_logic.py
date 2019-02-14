import rsa
from tor_server import TORUtil

# thread safe wrapper for UI thread to check variables
class Session(object):
    def getContext():
        pass

    def setContext():

    def isOpen():
        pass

    def setIsOpen(bol):
        pass

    def hasNewRequest():
        pass

    def requestSeen():
        pass

    def clearSession():
        pass



class Peer(object):
    def __init__(self):
        self.inbox
        self.outbox
        self.session 

    def requestSession(message, pubKeyId):
        outRevTor = TORUtil.generateRevTor(self.randORNodes())
        payload = TORUtil.generatePayload(pubKeyId, revTor, message, self.pubKeyId)
        self.DHT.put(pubKeyId, payload)

    # solid, ready to test
    def sendMessage(message):
        outRevTor = TORUtil.generateRevTor(self.randORNodes())
        payload = TORUtil.generatePayload(self.session.lastPubKey, outRevTor,
                                          message, self.pubKeyID)
        packet, address = TORUtil.generateTransmission(self.session.lastRevTor, payload)
        self.torServer.forwardPacket(packet, address)

    #solid ready to test
    def displayPayload(payload):
        revTor, message, pubKey = TORUtil.splitPayload(payload, self.privKeyId)
        self.session.lastRevTor = revTor
        self.session.lastPubKey = pubKey
        
        if (not self.session.isOpen()):
            self.session.setIsOpen(True)
            self.session.setContext(pubKey)
            
        if (self.isTerminate(message)):
            self.session.clearSession()
        else:
            print(self.formatMessage(message, pubKey))

    def formatMessage(self, message, pubKey):
        return "\n" + str(pubKey) + "::" + message + "\n" + "me: "

    @asyncio.coroutine
    def pollRequests():
        if something:
            
        pass

    @asyncio.coroutine
    def pollUI():
        pass
