import socket, os
from time import sleep

HOST = '127.0.0.1'
PORT = 12345
FILE_PATH = 'myfile.txt'
DATALEN = 500
ACK = b'A'
NACK = b'N'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendFile(s):
    fileSize = os.path.getsize(FILE_PATH)
    s.sendto((str(fileSize).encode('utf-8')), 0,(HOST,PORT))
    ack, addr = s.recvfrom(1024)
    if ack == ACK:
        print('Received ACK for file size')

    sentSize = 0
    currCount = 0
    batchLimit = 1
    batchCount = 0
    batchBuffer = []
    fileToSend = open(FILE_PATH, "rb")
    while sentSize < fileSize:
        # sleep(1)
        currCount += 1
        batchCount += 1
        datagram = fileToSend.read(DATALEN)
        batchBuffer.append(datagram)
        s.sendto(datagram, 0, addr)
        print("Sent datagram", currCount)
        sentSize += len(datagram)
        # print('buffer', batchBuffer)
        if batchCount == batchLimit:
            ack, addr = s.recvfrom(1024)
            if ack == ACK:
                print("Received ACK for batch", batchLimit)
            batchCount = 0
            batchBuffer = []
            batchLimit += 1

    fileToSend.close()

if __name__ == "__main__":
    sendFile(s)
