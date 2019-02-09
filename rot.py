
#############################################
# INTERFACE TO PEERS
#############################################
import rsa;
import random;

def Network():
    userList;
    def __init__(num):
        if(num<1):
            num = 1
        for i in range(num):
            userList.append(User())
    pass

    def addUser(User):
        user.append(User)
    pass

    #probably remove this eventually
    def getUserNum(num):
        if(num>userList.len()):
            num = userList.len()-1
        if(userList.len()>num and num>0):
            return userList[num]
        return None

    def getUserPub(num):
        for i in range(userList.len()):
            if(userList[i].msgPubKey):
                return None
        return None 

    def getRandom():
        out
        len = random.randint(3,6)
        for i in range(len):
             out.apped(userList[random.randint(0,userList.len()-1)])
        return out


def User():
    msgPubKey, msgPrivKey, namePubKey, namePrivKey
    def __init__():
        (msgPubKey, msgPrivKey) = rsa.newkeys(512)
        (namePubKey, namePrivKey) = rsa.newkeys(512)
        pass
    
    def formROT(payload, trgPub, Network):
            path = Network.getRandom()
            pass


    # takes rot packet and payload, extracts 1st trg IP, and send rot+payload on it's way
    def sendROT(rot, payload):
        pass

    def forwardROT(packet):
        pass

net = Network(5);
net.userList[1]