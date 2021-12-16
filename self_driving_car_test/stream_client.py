import socket
import sys
import RPi.GPIO as GPIO
from time import sleep
import io
import struct
import time
import threading
import picamera

# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((input("IP"), 8000))
connection = client_socket.makefile('wb')

client = socket.socket()
client.connect((input("IP"), 8080))


def recv_instru():
    incoming_message = client.recv(1024)
    incoming_message = incoming_message.decode()
    return incoming_message


def forward_right():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in_steering1, GPIO.HIGH)
    GPIO.output(in_steering2, GPIO.LOW)


def forward_left():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in_steering1, GPIO.LOW)
    GPIO.output(in_steering2, GPIO.HIGH)


def reserve_right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in_steering1, GPIO.HIGH)
    GPIO.output(in_steering2, GPIO.LOW)


def reserve_left():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in_steering1, GPIO.LOW)
    GPIO.output(in_steering2, GPIO.HIGH)


def forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)


def reserve():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)


def right():
    GPIO.output(in_steering1, GPIO.HIGH)
    GPIO.output(in_steering2, GPIO.LOW)


def left():
    GPIO.output(in_steering1, GPIO.LOW)
    GPIO.output(in_steering2, GPIO.HIGH)


def standby():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in_steering1, GPIO.LOW)
    GPIO.output(in_steering2, GPIO.LOW)


def exit():
    GPIO.cleanup()
    print("GPIO Clean up")


def get_commands():
    while True:
        command = recv_instru()
        if command == "forward_right":
            forward_right()
        elif command == "forward_left":
            forward_left()
        elif command == "reserve_right":
            reserve_right()
        elif command == "reserve_left":
            reserve_right()
        elif command == "forward":
            forward()
        elif command == "reserve":
            reserve()
        elif command == "right":
            right()
        elif command == "left":
            left()
        elif command == "exit":
            exit()
        elif command == "none":
            standby()


in1 = 24
in2 = 23
in_steering1 = 17
in_steering2 = 27
en_steering = 22
en = 25
temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in_steering1, GPIO.OUT)
GPIO.setup(in_steering2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(en_steering, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)
s = GPIO.PWM(en_steering, 1000)

p.start(65)
s.start(100)

Thread = threading.Thread(target=get_commands)
Thread.start()
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)  # pi camera resolution
        camera.framerate = 15  # 15 frames/sec
        time.sleep(2)  # give 2 secs for camera to initilize
        start = time.time()
        stream = io.BytesIO()

        # send jpeg format video stream
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            if time.time() - start > 600:
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))


finally:
    connection.close()
    client_socket.close()
    client.close()
