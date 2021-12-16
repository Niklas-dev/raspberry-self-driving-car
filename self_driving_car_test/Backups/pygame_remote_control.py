import pygame
import numpy as np
import struct
import socket
import os
from threading import Thread
from PIL import Image
import matplotlib.pyplot as pl
from threading import Thread
import sys
import qimage2ndarray
import cv2
import io
import time


class host:
    def __init__(self):
        self.s = socket.socket()
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080
        self.connected = False


    def start_server(self):
        self.s.bind((self.host, self.port))
        print(self.host)

    def server_listen(self):
        self.s.listen(0)
        self.conn, addr = self.s.accept()
        self.connected = True

    def receive_data(self):
        self.incoming_message = self.connection.recv(1024)
        self.incoming_message = self.incoming_message.decode()
        if self.incoming_message == "1":
            print("Data")

    def send_data(self, command):
        message = command
        message = message.encode()
        self.conn.send(message)
        print("Sent")

    def run_server(self):
        self.start_server()
        self.server_listen()

    def send_for(self):
        server.send_data("for")

    def send_back(self):
        server.send_data("back")

    def send_start(self):
        server.send_data("run")

    def send_stop(self):
        server.send_data("stop")

    def send_exit(self):
        server.send_data("exit")

    def send_straight(self):
        server.send_data("st")

    def send_right(self):
        server.send_data("tr")

    def send_left(self):
        server.send_data("tl")

    def send_high(self):
        server.send_data("high")

    def send_medium(self):
        server.send_data("medium")

    def send_low(self):
        server.send_data("low")



class VideoStream:
    def __init__(self):
        self.img = None
        self.connection = None
        self.server_socket = socket.socket()
        self.end_image = None
        self.img_count_l = 0
        self.img_count_r = 0
        self.img_count_f = 0
        self.pathf = 'D:/Programming/Self-Driving-Car/Forward'
        self.pathl = 'D:/Programming/Self-Driving-Car/Left'
        self.pathr = 'D:/Programming/Self-Driving-Car/Right'
        self.frame = None

    def connect_stream(self):
        self.server_socket.bind((socket.gethostbyname(socket.gethostname()), 8000))  # ADD IP HERE
        self.server_socket.listen(0)

        self.connection = self.server_socket.accept()[0].makefile('rb')

    def get_frames(self):
        self.connect_stream()
        try:
            while True:
                img = None

                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]

                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                image = Image.open(image_stream)
                image = np.array(image)
                image = Image.fromarray(image,'RGB')
                image = np.uint8(image)
                screen.fill([0, 0, 0])
                image = np.rot90(image)
                self.frame = image
                image = pygame.surfarray.make_surface(image)
                image = pygame.transform.scale(image, (512, 512))
                screen.blit(image, (0, 0))
                pygame.display.update()


        except:
            self.connection.close()
            self.server_socket.close()

    def save_img_left(self):
        time.sleep(0.05)
        cv2.imwrite(f'{self.img_count_l}left.jpg', self.frame)
        self.img_count_l += 1
    def save_img_forward(self):
        time.sleep(0.05)
        cv2.imwrite(f'{self.img_count_f}forward.jpg', self.frame)
        self.img_count_f += 1
    def save_img_right(self):
        time.sleep(0.05)
        cv2.imwrite(f'{self.img_count_r}right.jpg', self.frame)
        self.img_count_r += 1


pygame.init()

screen = pygame.display.set_mode((512, 512))
server = host()
stream = VideoStream()


thread1 = Thread(target=server.run_server)
thread1.start()
thread2 = Thread(target=stream.get_frames)
thread2.start()


save_images = True
last_key = ""
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        server.send_for()
        last_key = "forward"
        stream.save_img_forward()
    if keys[pygame.K_a]:
        server.send_left()
        last_key = "left"
        stream.save_img_left()
    if keys[pygame.K_d]:
        server.send_right()
        last_key = "right"
        stream.save_img_right()
    if keys[pygame.K_s]:
        server.send_back()
    if keys[pygame.K_e]:
        server.send_exit()
    if keys[pygame.K_r]:
        server.send_stop()
    if keys[pygame.K_1]:
        server.send_low()
    if keys[pygame.K_2]:
        server.send_medium()
    if keys[pygame.K_3]:
        server.send_high()
    if keys[pygame.K_SPACE]:
        server.send_straight()


