#Developped by Aruna Jayasena 
#NTRIP data send to the server via UDP application from a Raspberry pi

import socket
import serial
import sys


UDP_IP = "192.168.1.xxx"
UDP_PORT = 2302

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
 
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

while True:
    
    data=ser.readline()
    print >>sys.stderr, [ord(d) for d in data]
    sock.sendto(data, (UDP_IP, UDP_PORT))
