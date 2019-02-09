
#############################################
# INTERFACE TO PEERS
#############################################
import rsa
import random
import json

class Network: 
    #this will be replaced with DHT

    def __init__(self,num):
        self.userList = []
        if(num<1):
            self.num = 1
        for i in range(num):
            self.userList.append(User())
    pass

    def addUser(User):
        self.userList.append(User)
    pass

    #probably remove this eventually
    def getUserNum(self,num):
        if(num>len(self.userList)):
            self.num = len(self.userList.len)-1
        if(len(self.userList)>num and num>=0):
            return self.userList[num]
        return None

    def getRandomPath(self,len):
        out = []
        for i in range(len):
            index = random.randint(0,len(self.userList)-1)
            out.append(self.userList[index])
        return out


class User():
    def __init__(self):
        (self.TPuK, self.TPrK) = rsa.newkeys(512)
        (self.IDPuK, self.IDPrK) = rsa.newkeys(512)
        self.IP = "IP:" + str(random.randint(0,1000))
        pass
    
    def formROT(self,payload, Network, trg_IDPuK):
            destination = self.IP.encode('utf8')
            path = Network.getRandomPath(2)
            rot = []
            for i in range(0,path.len()):
                rot.append(rsa.encrypt(destination,path[i].TPuK))
                destination = path[i].IP.encode('utf8');
            rot.append(destination) #not encrypted

            for i in range (0,rot.len()):
                rot[i] = rsa.encrypt[rot[i],trg_IDPuK]

            return rot, rsa.encrypt[payload,trg_IDPuK]

    # post ROT to the forumn
    def sendROT(self,rot, encrypted_payload, target_IDPuK):
        pass

    #take ROT and forward it to the next person
    def forwardROT(self,rot, encrypted_payload):
        next = rot[rot.len()-1]
        next = rot.remove(rot.len()-1)
        next = rsa.decrypt(rot[rot.len-1],TPrK).decode('utf8');
        message = rsa.decrypt(encrypted_payload,TPrK).decode('utf8');
        pass

net = Network(5);
(rot, msg) = net.getUserNum(0).formROT('I fight for the users', net, net.getUserNum(4).IDPuK)