import socket
import sys
import RPi.GPIO as GPIO          
from time import sleep
import io
import struct
import time
import threading
import picamera


class stream_client:
    def __init__(self):
        self.connection = None
        self.client_socket = socket.socket()
        self.HOST = input(str("IP for stream(Use same IP) " ))
        
    def connect_stream(self):
        self.client_socket.connect((self.HOST, 8000))  # ADD IP HERE
        self.connection = self.client_socket.makefile('wb')
        
    def stream_video(self):
        self.connect_stream()
        try:

            camera = picamera.PiCamera()
            camera.hflip = True
            camera.framerate = 7
            camera.resolution = (480, 480)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            time.sleep(2)

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                self.connection.write(struct.pack('<L', stream.tell()))
                self.connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                self.connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            # Write a length of zero to the stream to signal we're done
            self.connection.write(struct.pack('<L', 0))
        finally:
            self.connection.close()
            self.client_socket.close()
    
class Client:
    def __init__(self):
        self.s = socket.socket()
        self.host = input(str("Please enter the hostname of the server : "))
        self.port = 8080

    def connect(self):
        self.s.connect((self.host, self.port))
        print(" Connected to chat server")
    def receive(self):
        self.incoming_message = self.s.recv(1024)
        self.incoming_message = self.incoming_message.decode()
        return self.incoming_message




    def get_commands(self):
        self.message = self.receive()
        if self.message == "run":
            return
        elif self.message == "tr":
            return "tr"
        elif self.message == "tl":
            return "tl"
        elif self.message == "st":
            return "st"
        elif self.message == "low":
            return "l"
        elif self.message == "medium":
            return "m"
        elif self.message == "high":
            return "h"
        elif self.message == "for":
            return "f"
        elif self.message == "back":
            return "b"
        elif self.message == "stop":
            return "s"
        elif self.message == "exit":
            return "e"
        elif self.message == "for":
            return "f"
        else:
            pass
            



client = Client()
client.connect()

stream = stream_client()


in1 = 24
in2 = 23
in_steering1 = 17
in_steering2 = 27
en_steering = 22
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in_steering1, GPIO.OUT)
GPIO.setup(in_steering2, GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(en_steering, GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
s=GPIO.PWM(en_steering, 1000)


p.start(30)
s.start(100)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    
GPIO.output(in_steering1, GPIO.LOW)
GPIO.output(in_steering2, GPIO.LOW)
while(1):
    x=client.get_commands()
    
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=1
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(60)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(80)
        x='z'

     
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
        
    elif x == "tl":
            GPIO.output(in_steering1, GPIO.LOW)
            GPIO.output(in_steering2, GPIO.HIGH)
            

            
    elif x == "tr":
            GPIO.output(in_steering1, GPIO.HIGH)
            GPIO.output(in_steering2, GPIO.LOW)
            
            
            
    elif x == "st":
            GPIO.output(in_steering1, GPIO.LOW)
            GPIO.output(in_steering2, GPIO.LOW)

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")

    stream.stream_video()
