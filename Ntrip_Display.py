#Developped by Aruna Jayasena 
#NTRIP data client application for Raspberry pi
#Available Data is Printed on Nokia 5800 Black and white display.


import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import socket
import base64
import sys
import serial

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


fix_type={ '0' : "Invalid",
           '1' : "GPS fix (SPS)",
           '2' : "DGPS fix",
           '3' : "PPS fix",
           '4' : "Real Time Kinematic",
           '5' : "Float RTK",
           '6' : "estimated (dead reckoning) (2.3 feature)",
           '7' : "Manual input mode",
           '8' : "Simulation mode"}



# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Raspberry Pi software SPI config:
# SCLK = 4
# DIN = 17
# DC = 23
# RST = 24
# CS = 8

# Beaglebone Black hardware SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Beaglebone Black software SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SCLK = 'P8_7'
# DIN = 'P8_9'
# CS = 'P8_11'


# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)



# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 8)

# Write some text.
draw.text((10,15), 'Waiting for', font=font)
draw.text((3,25), 'eNetlk server', font=font)


# Display image.
disp.clear()
disp.image(image)
disp.display()


ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0)

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
print "Fetching NTRIP data from enetlk servers"


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
                # Write some text.
                draw.rectangle((0,0,83,47), outline=255, fill=255)
                draw.text((8,15), 'Fix:'+fix_type[data[6]], font=font)
                draw.text((8,25), 'N:'+str(float(data[2])/100), font=font)
                draw.text((8,35), 'E:'+str(float(data[4])/100), font=font)

                # Display image.
                disp.image(image)
                disp.display()
            

              
                
        except:
            print "Missed" ,"\r",
        
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



print('Press Ctrl-C to quit.')
while True:
    time.sleep(1.0)
