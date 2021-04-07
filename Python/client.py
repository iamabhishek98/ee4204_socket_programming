import header as h

def sendFile(s):
    fileSize = h.os.path.getsize(h.FILE_PATH)
    s.sendto((str(fileSize).encode('utf-8')), 0,(h.HOST,h.PORT))
    ack, addr = s.recvfrom(1024)
    if ack.decode('utf-8') == h.ACK:
        print('Received ACK for file size')
    else:
        raise Exception('Error in receiving ACK for file size!')
    
    sentSize = 0
    currCount = 0
    batchLimit = 1
    batchNo = 1
    batchCount = 0
    prevACKStatus = True
    fileToSend = open(h.FILE_PATH, "rb")
    tStart = h.time()
    while sentSize < fileSize:
        if prevACKStatus:
            currCount += 1
            batchCount += 1
            datagram = fileToSend.read(h.DATALEN)
            s.sendto(datagram, 0, addr)
            print("Sent datagram {}".format(currCount))
            sentSize += len(datagram)
        if batchCount == batchLimit:
            prevACKStatus = False
            ack_datagram, addr = s.recvfrom(1024)
            # sleep(0.1)
            ack = ack_datagram.decode('utf-8')
            if ack[0] == h.ACK:
                if int(ack[1:]) == batchNo:
                    print("Received acknowledgement {}".format(ack))
                    prevACKStatus = True
                    batchCount = 0
                    batchNo += 1
                    batchLimit += 1
                    if batchLimit > 3: batchLimit = batchLimit % 3

                    # batchLimit = batchLimit%3
                else: raise Exception('Error in receiving acknowledgement')
    
    if sentSize != fileSize:
        raise Exception('Sent file size != Expected file size')

    if batchCount and batchCount < batchLimit:
        ack_datagram, addr = s.recvfrom(1024)
        # sleep(0.1)
        ack = ack_datagram.decode('utf-8')
        if ack[0] == h.ACK and int(ack[1:]) == batchLimit:
            print("Received acknowledgement {}".format(ack))

    print('File successfully sent!\n')
    ttime = (h.time() - tStart)*1000
    print('Message Transfer Time: {} ms'.format(round(ttime,3)))
    print('Total File Size: {} bytes'.format(fileSize))
    print('Packet length: {} bytes'.format(h.DATALEN))
    print('Data rate: {} (Kbytes/s)'.format(round(fileSize/ttime,3)))
    fileToSend.close()

if __name__ == "__main__":
    s = h.socket.socket(h.socket.AF_INET, h.socket.SOCK_DGRAM)
    sendFile(s)