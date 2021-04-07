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
    batchNo = 1
    batchCount = 0
    s.settimeout(1)
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
            s.sendto(bytes(h.ACK+str(batchNo),'utf-8'), 0, addr)
            print("Sent ACK for batch {}".format(batchNo))
            batchCount = 0
            batchNo += 1
            batchLimit += 1
            if batchLimit > 3: batchLimit = batchLimit % 3

    if receivedSize != fileSize:
        raise Exception('Received file size != Expected file size')
    
    if batchCount and batchCount < batchLimit:
        s.sendto(bytes(h.ACK+str(batchLimit),'utf-8'), 0, addr)
        print("Sent ACK for batch {}".format(batchLimit))

    print('File successfully received!')
    receivedFile.close()

if __name__ == "__main__":
    while True:
        try:
            s = h.socket.socket(h.socket.AF_INET, h.socket.SOCK_DGRAM)
        except:
            raise Exception('Failed to create socket! Exiting...')

        s.bind((h.HOST, h.PORT))
        print('Socket binded to {}:{}'.format(str(h.HOST),str(h.PORT)))
        try:    
            recvFile(s)
        except Exception as e:
            print('Error in receiving file!', e)
        s.close()
        print('Socket closed')
