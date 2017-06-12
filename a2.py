'''
Created on April 11, 2016

@authors: Austin Takechi, Cuong Su
This code allows the user to request a file located in the same folder as this .py file and see it in html format.
It (i) creates a connection socket when contacted by a client (browser); 
   (ii) receives the HTTP request from this connection; 
   (iii) parses the request to determine the specific file being requested; 
   (iv) gets the requested file from the server's file system; 
   (v) creates an HTTP response message consisting of the requested file preceded by header lines; 
   (vi) sends the response over the TCP connection to the requesting browser. 
If the user requests a file that is not present in the server, the server returns a "404 Not Found" error message.
'''
from socket import *

def main():
    #set up port number = 42069
    serverPort = 42069
    serverSocket = socket(AF_INET, SOCK_STREAM) 
    #Prepare a server socket
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print ('LISTENING AT PORT#: ', serverPort )
    #loop so that the server will be ready for multiple requests
    #can also be set to only take a single request at a time by removing comment before break at the bottom
    while True: 
        #Establish the connection 
        print ('Server is ready...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024)
            print ('\t>FILENAME REQUESTED:', message.split()[1])
            filename = message.split()[1] 
            f = open(filename[1:]) 
            #set outputData = whatever is inside the html file being used
            #if file isn't found, go to error message 
            outputData = f.read()
            #Send one HTTP header line into socket
            print ('\t>OUTPUT DATA SENT BACK TO CLIENT\n', outputData)
            connectionSocket.send(outputData.encode('utf-8'))
            #close the socket in order to not have multiple of the same request
            connectionSocket.close()
        except IOError:
            #if the file is not found, print and send an error message
            print ('ERROR: 404 Not Found\n')
            connectionSocket.send('HTTP/ ERROR: 404 Not Found\n\n'.encode('utf-8'))
            #end the request in order to not have multiple of the same request
            connectionSocket.close()        
    #break
    pass

if __name__ == '__main__':
    main()
