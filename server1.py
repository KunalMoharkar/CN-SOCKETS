import socket 
import time



try: 
    #ipv4 and TCP protocols used
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")

except socket.error as err: 
    print ("socket creation failed with error %s" %(err))

#port number and ip address
port = 12345    
ip = ''            
  
#bind to the port and ip
s.bind((ip, port))         
print (f"socket binded to port: {port} on host-ip {ip}")


#only 1 connection allowed 
# 0 indiacates keep no one waiting while server is busy 
# just refuse
s.listen(0)     

print ("now the socket is listening .... ")   

while True: 
  
    #accept the connection from client. 
    c, addr = s.accept()     

    print ('Got connection from', addr )
    msg = 'successfully connected'
    msg = msg.encode('utf-8')

    #aknowlege the client that connection successful
    c.send(msg) 

    expression = c.recv(1024).decode('utf-8')
    
    print(f"client query: {expression}")
    
    num1 = int(expression[0])
    num2 = int(expression[2])

    operator = expression[1]

    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1*num2
    else:
        result = num1/num2

    c.send(str(result).encode('utf-8'))

    print(f"{num1}  {operator} {num2}")

    #Close the connection
    c.close() 
    print(f'connection from {addr} is closed')