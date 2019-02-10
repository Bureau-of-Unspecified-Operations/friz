import asyncio
from kademlia.network import Server




class DHTNode(object):
    def __init__(self, loop):
        self.loop = loop
        self.node = Server()
        loop.run_until_complete(self.node.listen(self.genPersonalPort()))
        ip = input("Enter bootstrap IP:")
        port = input("Enter bootstrap port:")
        self.boot = [(ip, int(port))]
        self.attemptBootstrap()

    def attemptBootstrap(self):
        print(self.boot)
        task = self.loop.create_task(self.node.bootstrap(self.boot))
        task.add_done_callback(lambda future: print("bootstrap attempt failed") if len(future.result()) == 0 else print("bootstrap succeeded"))
        self.loop.run_until_complete(task)

    # actually solve, currently use dummy
    def bootstrappableNodes(self):
        return [("123.123.123.123", 5678)]


    def genPersonalPort(self):
        return 5678

    def testKeyPut(self):
        self.loop.run_until_complete(self.node.set("key","value"))
        result = self.loop.run_until_complete(self.node.get("key"))
        print(result)

    def putData(self, key, value):
        didSucceed = self.loop.run_until_complete(self.node.set(key, value))
        if didSucceed:
            print("succesfully stored [" + key + "," + value + "]")
        else:
            print("failed put")


    def getData(self, key):
        result = self.loop.run_until_complete(self.node.get(key))
        if result != None:
            print("get succeeded")
            return result
        else:
            print("failed get")







                                
    
