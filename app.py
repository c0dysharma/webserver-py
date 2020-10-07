from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import pdb

serverAddress = '192.168.43.36'
serverPort = 8080

def main():
    try:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind((serverAddress, serverPort))
        serverSocket.listen(1)
    except:
        error = sys.exc_info()
        print(f"{error[0].__name__}:{error[1]}")
        sys.exit(1)

    while True:
        connectedSocket, clientAddress = serverSocket.accept()
        print(f"Connected to {clientAddress}")
        requestedData = connectedSocket.recv(1024)
        fileName = '.'+requestedData.split()[1].decode()
        somethingWrong = 0

        try: 
            file = open(fileName, 'r')
        except:
            error = sys.exc_info()
            print(f"{error[0].__name__}:{error[1]}")
            somethingWrong = 1
            if(sys.exc_info()[0] == FileNotFoundError):
                connectedSocket.send(b'HTTP/1.0 404 Not Found\n\n')
                connectedSocket.sendall(b"404: File Not Found")
                connectedSocket.close()

        if somethingWrong != 1:
            responseData = file.read()
            connectedSocket.send(b'HTTP/1.0 200 OK\nContent-Type: text/html\n\n')
            done = connectedSocket.sendall(responseData.encode())
            file.close()
            if(done == None):
                print("data sent")
            connectedSocket.close()
            
    try:    
        serverSocket.close()
    except:
        error = sys.exc_info()
        print(f"{error[0].__name__}:{error[1]}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as error:
        print(f"{error} Have Good Day")
