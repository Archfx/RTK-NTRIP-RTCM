#!/usr/bin/env python

#Developped by Aruna Jayasena 
#Send RTCM3 data stream to the NTRIP server via TCP application from a Raspberry pi

import socket
import serial
import sys


TCP_IP = "192.168.1.xxx"
TCP_PORT = 2302
BUFFER_SIZE = 1024



ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    data=ser.readline()
    print >>sys.stderr, [ord(d) for d in data]
    s.send(data)
    #datain = s.recv(BUFFER_SIZE)
    #print "received data:", datain

#s.close() 



