import socket
import sys
import RPi.GPIO as GPIO
from time import sleep
import io
import struct
from picamera.array import PiRGBArray
import time
import os
import numpy as np
import threading
import picamera
import pandas as pd
import cv2
from datetime import datetime
from picamera import PiCamera

in1 = 24
in2 = 23
in_steering1 = 17
in_steering2 = 27
en_steering = 22
en = 25

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


class drive(object):
    def __init__(self):
        self.client = socket.socket()
        self.client.connect((input("IP"), 8080))
        self.send_inst = True
        self.command = ""

    def forward_right(self):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in_steering1, GPIO.HIGH)
        GPIO.output(in_steering2, GPIO.LOW)
        print("driven")

    def forward_left(self):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in_steering1, GPIO.LOW)
        GPIO.output(in_steering2, GPIO.HIGH)
        print("driven")

    def reserve_right(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in_steering1, GPIO.HIGH)
        GPIO.output(in_steering2, GPIO.LOW)
        print("driven")

    def reserve_left(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in_steering1, GPIO.LOW)
        GPIO.output(in_steering2, GPIO.HIGH)
        print("driven")

    def forward(self):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        print("driven")

    def reserve(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        print("driven")

    def right(self):
        GPIO.output(in_steering1, GPIO.HIGH)
        GPIO.output(in_steering2, GPIO.LOW)
        print("driven")

    def left(self):
        GPIO.output(in_steering1, GPIO.LOW)
        GPIO.output(in_steering2, GPIO.HIGH)
        print("driven")

    def standby(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in_steering1, GPIO.LOW)
        GPIO.output(in_steering2, GPIO.LOW)
        print("driven")

    def exit(self):
        GPIO.cleanup()
        print("GPIO Clean up")


class CollectTrainingData(object):

    def __init__(self):
        self.images = 0
        self.countFolder = 0
        self.count = 0
        self.imgList = []
        self.steeringList = []
        self.myDirectory = ""
        self.newPath = "CollectedData"

        # create labels

    def recv_instru(self):
        drive.incoming_message = drive.client.recv(1024)
        drive.incoming_message = drive.incoming_message.decode()
        return drive.incoming_message

    # initialize the camera and stream
    def saveData(self, img, steering):
        now = datetime.now()
        timestamp = str(datetime.timestamp(now)).replace('.', '')
        # print("timestamp =", timestamp)

        if steering == 1:
            fileName = os.path.join(self.pathRight, f'Image_{timestamp}.jpg')
            cv2.imwrite(fileName, img)
        if steering == 2:
            fileName = os.path.join(self.pathForward, f'Image_{timestamp}.jpg')
            cv2.imwrite(fileName, img)
        if steering == 0:
            fileName = os.path.join(self.pathLeft, f'Image_{timestamp}.jpg')
            cv2.imwrite(fileName, img)



    def saveLog(self):
        print('Log Saved')
        print('Total Images: ', len(self.imgList))

    def collect(self):
        saved_frame = 0
        total_frame = 0
        self.myDirectory = os.path.join(os.getcwd(), 'DataCollected')
        # print(myDirectory)

        # CREATE A NEW FOLDER BASED ON THE PREVIOUS FOLDER COUNT

        self.pathRight = self.myDirectory + "/Right"

        self.pathForward = self.myDirectory + "/Forward"

        self.pathLeft = self.myDirectory + "/Left"

        os.makedirs(self.pathRight)
        os.makedirs(self.pathForward)
        os.makedirs(self.pathLeft)

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        # stream video frames one by one
        try:
            camera = PiCamera()
            camera.resolution = (480, 240)
            camera.framerate = 20
            start = time.time()
            time.sleep(2)
            rawCapture = PiRGBArray(camera, size=(480, 240))

            for frame in camera.capture_continuous(rawCapture, 'bgr', use_video_port=True):
                image = frame.array

                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # select lower half of the image


                # reshape the roi image into a vector
                temp_array = image

                self.images += 1
                total_frame += 1

                # pictures += 1
                # total_frames += 1

                command = self.recv_instru()
                if command == "forward_right":
                    print("Forward Right")
                    self.saveData(temp_array, 1)
                    drive.forward_right()
                    saved_frame += 1


                elif command == "forward_left":
                    print("Forward Left")
                    self.saveData(temp_array, 0)
                    drive.forward_left()
                    saved_frame += 1

                elif command == "reserve_right":
                    print("Reverse Right")
                    drive.reserve_right()


                elif command == "reserve_left":
                    print("Reverse Left")
                    drive.reserve_left()


                # simple orders
                elif command == "forward":
                    print("Forward")
                    self.saveData(temp_array, 2)
                    drive.forward()
                    saved_frame += 1


                elif command == "reserve":
                    print("Reverse")
                    drive.reserve()


                elif command == "right":
                    print("Right")
                    self.saveData(temp_array, 1)
                    drive.right()
                    saved_frame += 1


                elif command == "left":
                    print("Left")
                    self.saveData(temp_array, 0)
                    drive.left()
                    saved_frame += 1

                elif command == "none":
                    drive.standby()
                elif command == "exit":
                    drive.exit()
                    print("exit")
                    break

                rawCapture.seek(0)
                rawCapture.truncate()
            self.saveLog()

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)

        finally:
            drive.client.close()


if __name__ == '__main__':
    ctd = CollectTrainingData()
    drive = drive()
    # vector size, half of the image
    ctd.collect()
