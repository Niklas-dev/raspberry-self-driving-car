# Autopilot #
from tensorflow.keras.models import load_model
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
import time
import numpy as np
import picamera
import cv2
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

has_Stopped = False


class drive(object):
    def __init__(self):
        pass

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
        GPIO.output(in_steering1, GPIO.LOW)
        GPIO.output(in_steering2, GPIO.LOW)
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


model = load_model('/home/pi/Documents/Documents/modelv3.h5')
sign_model = load_model('/home/pi/Documents/model_signsv1.h5')
# model = load_model('model.h5')
CATEGORIES = ["Left", "Right", "Forward"]
CATEGORIES_SIGN = ["No_Signs", "Signs"]


def Auto():
    # stream video frames one by one

    camera = PiCamera()
    camera.resolution = (480, 240)
    camera.framerate = 8
    time.sleep(2)
    rawCapture = PiRGBArray(camera, size=(480, 240))

    for frame in camera.capture_continuous(rawCapture, 'bgr', use_video_port=True):
        image = frame.array

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 60))
        image = np.array(image).reshape(-1, 200, 60, 1)
        image = image / 255

        command = model.predict(image)
        command_sign = sign_model.predict(image)
        command = CATEGORIES[np.argmax(command)]
        command_sign = CATEGORIES_SIGN[np.argmax(command_sign)]

        if command_sign == "No_Signs":
            if command == "Right":
                print("Forward Right")
                drive.forward_right()

            elif command == "Left":
                print("Forward Left")
                drive.forward_left()

            elif command == "Forward":
                print("Forward")
                drive.forward()
            # ------------------------------------------ #
            elif command == "right":
                print("Right")
                drive.right()



            elif command == "left":
                print("Left")
                drive.left()


            elif command == "reserve_right":
                print("Reverse Right")
                drive.reserve_right()


            elif command == "reserve_left":
                print("Reverse Left")
                drive.reserve_left()


            elif command == "reserve":
                print("Reverse")
                drive.reserve()

            elif command == "none":
                drive.standby()
            elif command == "exit":
                drive.exit()
                print("exit")
                break
        elif command_sign == "Signs" and has_stopped == False:
            drive.standby()
            time.sleep(3)
            has_stopped = True

        rawCapture.seek(0)
        rawCapture.truncate()


if __name__ == '__main__':
    drive = drive()
    Auto()
