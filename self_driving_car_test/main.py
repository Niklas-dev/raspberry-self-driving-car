import numpy as np
import cv2
import pygame
from pygame.locals import *
import socket
import time
import os
import sys


class CollectTrainingData(object):

    def __init__(self, host, port, input_size):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # connect instruction server
        self.server = socket.socket()
        self.server.bind((socket.gethostbyname(socket.gethostname()), 8080))
        self.server.listen(0)

        self.conn, addr = self.server.accept()
        self.send_inst = True

        self.input_size = input_size

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1

        pygame.init()
        pygame.display.set_mode((250, 250))
    def send_data(self, command):
        time.sleep(0.1)
        command = command.encode()
        self.conn.send(command)
        print("Sent")

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
            stream_bytes = b' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # select lower half of the image
                    height, width = image.shape

                    cv2.imshow('image', image)

                    # reshape the roi image into a vector
                    temp_array = image

                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            sys.exit()
                    if event.type == KEYDOWN:
                        key_input = pygame.key.get_pressed()

                            # complex orders
                        if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                            print("Forward Right")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[1]))
                            saved_frame += 1
                            self.send_data("forward_right")

                        elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                            print("Forward Left")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[0]))
                            saved_frame += 1
                            self.send_data("forward_left")

                        elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                            print("Reverse Right")
                            self.send_data("reserve_right")

                        elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                            print("Reverse Left")
                            self.send_data("reserve_left")

                        # simple orders
                        elif key_input[pygame.K_UP]:
                            print("Forward")
                            saved_frame += 1
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[2]))
                            self.send_data("forward")

                        elif key_input[pygame.K_DOWN]:
                            print("Reverse")
                            self.send_data("reserve")

                        elif key_input[pygame.K_RIGHT]:
                            print("Right")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[1]))
                            saved_frame += 1
                            self.send_data("right")

                        elif key_input[pygame.K_LEFT]:
                            print("Left")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[0]))
                            saved_frame += 1
                            self.send_data("left")

                        elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                            print("exit")
                            self.send_inst = False
                            self.send_data("exit")
                            self.server.close()
                            break

                    elif event.type == pygame.KEYUP:
                        self.send_data("none")

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            # save data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
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
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p = socket.gethostbyname(socket.gethostname()), 8000



    # vector size, half of the image
    s = 120 * 320

    ctd = CollectTrainingData(h, p, s)
    ctd.collect()