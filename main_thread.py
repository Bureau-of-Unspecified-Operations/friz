def jacobsBootStrapFunction():
    return True

def jacobsRequestSessionFunction(public_key):
    return True

def jacobsSendMessageFunction(message):
    return

def jacobsDisconnectFunction():
    return

def cleanThreadsAndExit():
    # clean threads
    exit(1)

def startSeperateThread():
    pass


### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###


def startChat():
    startSeperateThread()
    while (True):
        next_input = input("Next message (type break to end chat): ")
        if (next_input == 'break'):
            break
        else:
            print('You: ', next_input)


def main():
    while True:
        startBootstrap = input('Would you like to bootstrap? (Y/N)')
        if (startBootstrap.lower() == 'y'):
            if (jacobsBootStrapFunction()):
                print('Bootstrapping Successful!')
                public_key = input('Please input the public key:')
                if (jacobsRequestSessionFunction(public_key)):
                    print('Connection Successful!')
                    startChat()
                    cleanThreadsAndExit()
                else:
                    print('Connection Failed!')
            else:
                print('Bootstrapping Failed!')
            bootstrap()
        elif (startBootstrap.lower() == 'n'):
            cleanThreadsAndExit()


if __name__ == '__main__':
    main()
    print('exited')
