import numpy as np
import cv2
import pygame
from pygame.locals import *
import socket
import time
import os
import sys


class CollectTrainingData(object):

    def __init__(self):

        print("Server On")
        # connect instruction server
        self.server = socket.socket()
        self.server.bind((socket.gethostbyname(socket.gethostname()), 8080))
        self.server.listen(0)
        print(socket.gethostbyname(socket.gethostname()))
        self.conn, addr = self.server.accept()
        self.send_inst = True

        pygame.init()
        pygame.display.set_mode((250, 250))

    def send_data(self, command):
        time.sleep(0.05)
        command = command.encode()
        self.conn.send(command)
        print("Sent")

    def collect(self):


        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")

        try:
            while self.send_inst:
                time.sleep(0.05)
                # get input from human driver
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        self.send_data("forward_right")

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
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
                        self.send_data("forward")

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.send_data("reserve")

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.send_data("right")

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.send_data("left")

                    elif key_input[pygame.K_x]:
                        print("exit")
                        self.send_inst = False
                        self.send_data("exit")
                        self.server.close()
                        break

                elif event.type == pygame.KEYUP:
                    self.send_data("none")
        finally:
            self.server.close()


ctd = CollectTrainingData()
ctd.collect()
