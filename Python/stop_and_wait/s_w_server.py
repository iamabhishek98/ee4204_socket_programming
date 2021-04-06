import header as h

def recvFile(s):
    fileSizeReceivedStatus = False
    
    # send file size
    while not fileSizeReceivedStatus:
        file_size_bytes, addr = s.recvfrom(1024)
        fileSize = int(file_size_bytes.decode('utf-8'))
        # if file_size < 0:
        #     raise Exception("file size cannot be negative")
        print('File size is {}'.format(fileSize))
        s.sendto(bytes(h.ACK,'utf-8'), 0, addr)
        print("Sent ACK for file size")
        fileSizeReceivedStatus = True
    

    receivedFile = open(h.RECEIVED_FILE_PATH, "wb")
    receivedSize = 0
    currCount = 1
    s.settimeout(1)
    # send file in short datalen
    while receivedSize < fileSize:
        datagram, addr = s.recvfrom(h.DATALEN)
        print("Received datagram {}".format(currCount))
        datagramSize = len(datagram)
        receivedFile.write(datagram)
        s.sendto(bytes(h.ACK+str(currCount),'utf-8'), 0, addr)
        print("Sent ACK for datagram {}".format(currCount))
        receivedSize += datagramSize
        currCount += 1
    
    print('File successfully received!')
    receivedFile.close()

if __name__ == "__main__":
    while True:
        try:
            s = h.socket.socket(h.socket.AF_INET, h.socket.SOCK_DGRAM)
        except:
            print('Failed to create socket! Exiting...')
            h.sys.exit()
        s.bind((h.HOST, h.PORT))
        print('Socket binded to {}:{}'.format(h.HOST,h.PORT))
        try:
            recvFile(s)
        except h.socket.timeout:
            print('Socket timed out. Error in receiving file!')
        s.close()
        print('Socket closed')