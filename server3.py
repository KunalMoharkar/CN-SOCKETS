import select, socket, sys , getopt
import queue as Queue


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


def serve(expression):

    result = 'quitting connection'
    #receive the expression client sends
    expression = expression.decode('utf-8')
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
    
    return result




def createSocket(port,host):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")      
    server.setblocking(0)
    server.bind((host, port))
    server.listen()
    print ("now the socket is listening .... ")
    inputs = [server]
    outputs = []
    message_queues = {}

    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                print ('Got connection from', client_address )
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
            else:
                data = s.recv(1024)
                
                if data:
                    data = serve(data)
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                outputs.remove(s)
            else:
                print(f'server sent response {next_msg}')
                s.send(str(next_msg).encode('utf-8'))

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]

if __name__ == "__main__":
    main(sys.argv[1:])