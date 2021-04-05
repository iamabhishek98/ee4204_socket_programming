import socket, os
from time import sleep

HOST = '127.0.0.1'
PORT = 12345
FILE_PATH = 'myfile.txt'
DATALEN = 500
ACK = 'A'
NACK = 'N'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def fillBuffer(fileToSend, batchLimit):
    buffer = []
    for i in range(batchLimit):
        buffer.append(fileToSend.read(DATALEN))
    return buffer

def sendFile(s):
    fileSize = os.path.getsize(FILE_PATH)
    s.sendto((str(fileSize).encode('utf-8')), 0,(HOST,PORT))
    resp, addr = s.recvfrom(1024)
    if resp == ACK:
        print('Received ACK for file size')

    sentSize = 0
    currCount = 0
    batchLimit = 1
    batchCount = 0
    prevACKStatus = True
    fileToSend = open(FILE_PATH, "rb")
    batchBuffer = fillBuffer(fileToSend, batchLimit)
    # send file in short data units
    while sentSize < fileSize:
        # print(batchBuffer)
        if prevACKStatus:
            # if sendStatus
            # sleep(1)
            currCount += 1
            datagram = batchBuffer[batchCount]
            s.sendto(datagram, 0, addr)
            print("Sent datagram", currCount)
            batchCount += 1
            sentSize += len(datagram)
            # print('buffer', batchBuffer)
        if batchCount == batchLimit:
            s.settimeout(1)
            
            print(len(batchBuffer))
            prevACKStatus = False
            ack_datagram, addr = s.recvfrom(1024)
            sleep(0.1)

            resp = ack_datagram.decode('utf-8')
            if resp[0] == ACK and int(resp[1:]) == batchLimit:
                print("Received ACK:", resp)
                prevACKStatus = True
                batchCount = 0
                batchLimit += 1
                batchBuffer = fillBuffer(fileToSend, batchLimit)

            elif resp[0] == NACK:
                print("Received NACK:", resp)
                prevACKStatus = True 
                batchCount = 0
                print("Resending batch", batchLimit)

    fileToSend.close()

if __name__ == "__main__":
    sendFile(s)
