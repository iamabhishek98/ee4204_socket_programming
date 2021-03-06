import socket, sys
from time import sleep

HOST = '127.0.0.1'
PORT = 12345
ACK = 'A'
NACK = 'N'
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
        s.sendto(bytes(ACK,'utf-8'), 0, addr)
        print("Sent ACK for file size")
        fileSizeReceivedStatus = True
    

    receivedFile = open(RECEIVED_FILE_PATH, "wb")
    receivedSize = 0
    currCount = 0
    prevCount = 0
    batchLimit = 1
    batchCount = 0
    batchBuffer = []
    temp = True
    # receive file in short data units
    while receivedSize < fileSize:
        currCount += 1
        batchCount += 1
        datagram, addr = s.recvfrom(DATALEN)
        # print("Received datagram", currCount, prevCount)
        datagramSize = len(datagram)
        batchBuffer.append(datagram)
        
        if batchCount == batchLimit:
            if temp and batchLimit == 5: 
                s.sendto(bytes(NACK+str(batchLimit), 'utf-8'), 0, addr)
                print("Sent NACK")
                currCount = prevCount
                batchCount = 0
                # batch
                temp = False

            else:
                print("hello")
                # sleep(0.5)
                s.sendto(bytes(ACK+str(batchLimit),'utf-8'), 0, addr)
                print("Sent ACK for batch", batchLimit)
                batchCount = 0
                batchLimit += 1
                prevCount = currCount
                for i in batchBuffer:
                    receivedSize += len(i)
                    receivedFile.write(i)
                batchBuffer = []

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