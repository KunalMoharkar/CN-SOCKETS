import socket
import sys, getopt 

def main(argv):

    options = "h:p:"
    long_options = ["host", "port"]
 
    try:
    # Parsing argument
        arguments, values = getopt.getopt(argv, options, long_options)

        # checking each argument
        for currentArgument, currentValue in arguments:
        
            if currentArgument in ("-p", "--port"):
                port = int(currentValue)

            elif currentArgument in ("-h", "--host"):
                host = currentValue

        #create the socket connection
        createSocket(port,host)

    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

    
def createSocket(port,host):

    # Create a socket object 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        

    # connect to the server 

    try:
        s.connect((host, port)) 
    
    except:
        print("failed to connect to the server")
    
    print('successfully connected to the server')

    #input query
    exp = input()
    print(f"sending query {exp} to the server")

    s.send(exp.encode('utf-8'))

    print('Response received from the server:')
    print (s.recv(1024).decode('utf-8') )

    # close the connection 
    s.close()    

if __name__ == "__main__":
    main(sys.argv[1:])