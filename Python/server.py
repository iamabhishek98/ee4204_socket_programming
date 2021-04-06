import header as h

def recvFile(s):
    # receive file size
    file_size_bytes, addr = s.recvfrom(1024)
    try:
        fileSize = int(file_size_bytes.decode('utf-8'))
        print('File size is {}'.format(fileSize))
        s.sendto(bytes(h.ACK,'utf-8'), 0, addr)
        print("Sent ACK for file size")
    except:
        raise Exception('File size not received properly!')

    receivedFile = open(h.RECEIVED_FILE_PATH, "wb")
    receivedSize = 0
    currCount = 0
    batchLimit = 1
    batchCount = 0
    try:
        # receive file in short data unit
        while receivedSize < fileSize:
            currCount += 1
            batchCount += 1
            datagram, addr = s.recvfrom(h.DATALEN)
            print("Received datagram {}".format(currCount))
            datagramSize = len(datagram)
            receivedFile.write(datagram)
            receivedSize += datagramSize
            if batchCount == batchLimit:
                s.sendto(bytes(h.ACK+str(batchLimit),'utf-8'), 0, addr)
                print("Sent ACK for batch {}".format(batchLimit))
                batchCount = 0
                batchLimit += 1
    except:
        raise Exception("File not received properly!")

    if receivedSize != fileSize:
        raise Exception('Error in sending file!')
    
    if batchCount < batchLimit:
        s.sendto(bytes(h.ACK+str(batchLimit),'utf-8'), 0, addr)
        print("Sent ACK for batch {}".format(batchLimit))

    print('File successfully received!')
    receivedFile.close()

if __name__ == "__main__":
    try:
        s = h.socket.socket(h.socket.AF_INET, h.socket.SOCK_DGRAM)
    except:
        raise Exception('Failed to create socket! Exiting...')

    s.bind((h.HOST, h.PORT))
    print('Socket binded to {}:{}'.format(str(h.HOST),str(h.PORT)))
    
    while True:
        recvFile(s)

    s.close()
