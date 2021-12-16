OWN_IMAGE_PATH = 'C:/Users/Admin/PycharmProjects/car_training/Data/Forward/Image_160449650179568.jpg'

import os
import random
import cv2
import numpy as np

train_img_array = cv2.imread(os.path.join(OWN_IMAGE_PATH), cv2.IMREAD_GRAYSCALE)

print(train_img_array / 255)