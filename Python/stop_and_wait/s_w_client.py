import socket, os

HOST = '127.0.0.1'
PORT = 12345
FILE_PATH = 'myfile.txt'
DATALEN = 500
ACK = b'A'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendFile(s):
    fileSize = os.path.getsize(FILE_PATH)
    s.sendto((str(fileSize).encode('utf-8')), 0,(HOST,PORT))
    ack, addr = s.recvfrom(1024)
    if ack == ACK:
        print('Received ACK for file size')

    sentSize = 0
    currCount = 1
    fileToSend = open(FILE_PATH, "rb")
    while sentSize < fileSize:
        datagram = fileToSend.read(DATALEN)
        s.sendto(datagram, 0, addr)
        print("Sent datagram", currCount)
        ack, addr = s.recvfrom(1024)
        if ack == ACK:
            print("Received ACK for datagram", currCount)
            sentSize += len(datagram)
            currCount += 1

    fileToSend.close()

if __name__ == "__main__":
    sendFile(s)