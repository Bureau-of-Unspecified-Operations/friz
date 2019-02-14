PUB_KEY_PROMPT = "Enter public key of contact: "
REQUEST_MESSAGE_PROMPT = "Request message: "
INVALID_REQUEST = "error - not a valid request"
WAIT_PROMPT = "waiting for response \ntype \"quit\" to cancel request"
MESSAGING_PROMPT = "me: "
SELF_SESSION_TERMINATION = "Ending Session\n\n"
SESSION_TERMINATION = "Your peer ended the session\n\n"
QUIT = "quit"
REQUEST = "request"
MESSAGE = "message"


# basic terminal UI for Friz. Quite ugly
class View(object):
    def __init__(self, inbox, outbox, session):
        self.inbox = inbox
        self.outbox = outbox
        self.session = session
        
    def mainLoop(self):
        while True:
            if self.session.hasNewRequest():
                self.session.requestSeen()
                self.messagingLoop()
            else:
                self.requestLoop():


    # will respond to incoming requests, is not expectin responses
    def requestLoop(self):
        while True:
            if self.session.hasNewRequest():
                return
            key = input(PUB_KEY_PROMPT)
            message = input(REQUEST_MESSAGE_PROMPT)
            if (self.isValidRequest(key, message)):
                self.outbox.push((REQUEST, (key, message)))
                self.waitLoop()
                return
            else:
                print(INVALID_REQUEST)
                
    #blocks new requests, waits for response
    # TODO have it time out
    def waitLoop(self):
        while True:
            if self.inbox.empty():
                x = input(WAIT_PROMPT)
                if (self.isQuit(x)):
                    self.kill()
                pass
            else:
                messagingLoop()
                return

    #blocks new requests, waits for response, returns to main on TERMINATE
    def messagingLoop(self):
        prompt = self.session.context
        while True:
            x = input(prompt)
            prompt = MESSAGING_PROMPT
            if self.isTerminateCmd(x):
                print(SELF_SESSION_TERMINATION)
                self.session.setIsOpen(False)
                return
            elif not self.session.isOpen():
                print(SESSION_TERMINATED)
                return
            else:
                self.outbox.push((MESSAGE, x))

    def kill(self):
        pass

    def isQuit(x):
        return x == QUIT

    # What would real validation look like?
    def isValidRequest(req):
        return True
        
    
