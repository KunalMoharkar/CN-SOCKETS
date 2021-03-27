import socket, getopt
import sys

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

    try: 
        #ipv4 and TCP protocols used
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")

    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))


    #bind to the port and ip
    s.bind((host, port))         
    print (f"socket binded to port: {port} on host-ip {host}")

    s.listen()     
    print ("now the socket is listening .... ")   

    
    acceptConn = True
    #accept the connection from client. 
    while True:
    
        while acceptConn == True:
            c, addr = s.accept() 
            s.close()    
            print ('Got connection from', addr )
            acceptConn = False

        #receive the expression client sends
        expression = c.recv(1024).decode('utf-8')
        print(f"client query: {expression}")

        if expression != 'quit':
            expression = expression.split()
            try:
                num1 = float(expression[0])
                num2 = float(expression[2])
                operator = expression[1]
                #perform comutation based on operator type
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1*num2
                else:
                    result = num1/num2
            except:
                result = 'invalid format provided'
            #send the result back to client
            c.send(str(result).encode('utf-8'))
            print(f"sent the client response {result}")

        else:
            c.close() 
            print(f'connection from {addr} is closed')
            acceptConn = True
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen()  

if __name__ == "__main__":
    main(sys.argv[1:])