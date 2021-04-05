import socket, sys

HOST = '127.0.0.1'
PORT = 12345
ACK = b'A'
NACK = b'N'
DATALEN = 500
RECEIVED_FILE_PATH = 'myUDPreceive.txt'

def recvFile(s):
    fileSizeReceivedStatus = False
    
    # send file size
    while not fileSizeReceivedStatus:
        file_size_bytes, addr = s.recvfrom(1024)
        fileSize = int(file_size_bytes.decode('utf-8'))
        # if file_size < 0:
        #     raise Exception("file size cannot be negative")
        print('File size is',fileSize)
        s.sendto(ACK, 0, addr)
        print("Sent ACK for file size")
        fileSizeReceivedStatus = True
    

    receivedFile = open(RECEIVED_FILE_PATH, "wb")
    receivedSize = 0
    currCount = 0
    # send file in short datalen
    while receivedSize < fileSize:
        currCount += 1
        datagram, addr = s.recvfrom(DATALEN)
        print("Received datagram", currCount)
        datagramSize = len(datagram)
        receivedFile.write(datagram)
        s.sendto(ACK, 0, addr)
        print("Sent ACK for datagram", currCount)
        receivedSize += datagramSize

    receivedFile.close()

if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print('Failed to create socket! Exiting...')
        sys.exit()

    s.bind((HOST, PORT))
    print('Socket binded to '+str(HOST)+':'+str(PORT))

    recvFile(s)

    s.close()