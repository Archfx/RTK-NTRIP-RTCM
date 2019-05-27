#!/usr/bin/env python

#Developped by Aruna Jayasena 
#NTRIP data client application for Raspberry pi

import socket
import base64
import sys
import serial

fix_type={ '0' : "Invalid",
           '1' : "GPS fix (SPS)",
           '2' : "DGPS fix",
           '3' : "PPS fix",
           '4' : "Real Time Kinematic",
           '5' : "Float RTK",
           '6' : "estimated (dead reckoning) (2.3 feature)",
           '7' : "Manual input mode",
           '8' : "Simulation mode"} 

ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0)

#server, port, username, password, mountpoint = 'development.enetlk.com',2301,"123","123",'kel'
server, port, username, password, mountpoint = #'192.168.xxx.xxx',#Port,"#UserName","#Password",'#MP'

pwd = base64.b64encode("{}:{}".format("123","123"))

header =\
"GET /{} HTTP/1.1\r\n".format(mountpoint) +\
"Host \r\n".format(server) +\
"Ntrip-Version: Ntrip/2.0\r\n" +\
"User-Agent: NTRIP pyUblox/0.0\r\n" +\
"Connection: close\r\n" +\
"Authorization: Basic {}\r\n\r\n".format(pwd)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server,int(port)))
s.send(header)

resp = s.recv(1024)
print "Receiving NTRIP data over enetlk servers"


try:
    while True:
        # There are some length bytes at the head here but it actually
        # seems more robust to simply let the higher level RTCMv3 parser
        # frame everything itself and bin the garbage as required.

        #length = s.recv(4)

        #try:
        #    length = int(length.strip(), 16)
        #except ValueError:
        #    continue


        RoverMessege=ser.readline()
        try:
            if 'GGA' in RoverMessege:
                data=RoverMessege.split(",")
                print "Fix Type :",fix_type[data[6]],"  North :",float(data[2])/100,"  East :",float(data[4])/100 ,"\r",
                
            

              
                
        except:
            print "Missed" ,"\r"
        
        #print (RoverMessege)
        data = s.recv(1024)
        #print(data)
        #print >>sys.stderr, [ord(d) for d in data]
        sys.stdout.flush()
        ser.write(data)
        #mainloop()

finally:
    s.close()
    #win.quit()


