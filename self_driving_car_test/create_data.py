import socket
import sys
import RPi.GPIO as GPIO
from time import sleep
import io
import struct
from picamera.array import PiRGBArray
import time
import cv2
import os
import numpy as np
import threading
import picamera
from picamera import PiCamera


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


command = recv_instru()


def get_commands():
    while True:
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


class CollectTrainingData(object):

    def __init__(self, input_size):
        self.client = socket.socket()
        self.client.connect((input("IP"), 8080))
        self.send_inst = True

        self.input_size = input_size

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1

    # initialize the camera and stream
    def collect(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        X = np.empty((0, self.input_size))
        y = np.empty((0, 4))

        # stream video frames one by one
        try:
            frame = 1
            with picamera.PiCamera() as camera:
                camera.resolution = (320, 240)  # pi camera resolution
                camera.framerate = 15  # 15 frames/sec
                time.sleep(2)  # give 2 secs for camera to initilize
                start = time.time()
                stream = io.BytesIO()

                # send jpeg format video stream
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                    image = cv2.imdecode(np.frombuffer(stream, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # select lower half of the image
                    height, width = image.shape
                    roi = image[int(height / 2):height, :]

                    cv2.imshow('image', image)

                    # reshape the roi image into a vector
                    temp_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    # pictures += 1
                    # total_frames += 1
                    if command == "forward_right":
                        print("Forward Right")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, self.k[1]))
                        forward_right()

                    elif command == "forward_left":
                        print("Forward Left")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, self.k[0]))
                        forward_left()

                    elif command == "reserve_right":
                        print("Reverse Right")
                        reserve_left()

                    elif command == "reserve_left":
                        print("Reverse Left")
                        reserve_left()


                    # simple orders
                    elif command == "forward":
                        print("Forward")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, self.k[2]))
                        forward()


                    elif command == "reserve":
                        print("Reverse")
                        reserve()


                    elif command == "right":
                        print("Right")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, self.k[1]))
                        right()


                    elif command == "left":
                        print("Left")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, self.k[0]))
                        left()

                    elif command == "x" or "q":
                        print("exit")
                        self.server.close()
                        break
                    elif cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    else:
                        pass
                    stream.truncate()
            file_name = str(int(time.time()))
            directory = "/home/pi/Documents/PythonProjects/self_driving_car"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print(X.shape)
            print(y.shape)
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)

        finally:
            client.close()

if __name__ == '__main__':

    # vector size, half of the image
    s = 120 * 320

    ctd = CollectTrainingData(s)
    ctd.collect()
