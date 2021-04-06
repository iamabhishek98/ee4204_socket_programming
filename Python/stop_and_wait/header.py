import socket, os, sys
from time import time, sleep

HOST = '127.0.0.1'
PORT = 12345
ACK = 'A'
DATALEN = 500
FILE_PATH = 'myfile.txt'
RECEIVED_FILE_PATH = 'myUDPreceive.txt'