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

    exp = input()

    s.send(exp.encode('utf-8'))

    # receive data from the server 
    print (s.recv(1024).decode('utf-8') )

    print (s.recv(1024).decode('utf-8') )
    # close the connection 
    s.close()    


if __name__ == "__main__":
    main(sys.argv[1:])