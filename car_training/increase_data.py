import os
import cv2

CATEGORIES = ["Left", "Right", "Forward"]
NEW_CATEGORIES = ["NLeft", "NRight", "NForward"]
TRAIN_DIR = 'C:/Users/Admin/PycharmProjects/car_training/DataCollected'
NLeft_DIR = 'C:/Users/Admin/PycharmProjects/car_training/DataCollected/NLeft'
NRight_DIR = 'C:/Users/Admin/PycharmProjects/car_training/DataCollected/NRight'
NForward_DIR = 'C:/Users/Admin/PycharmProjects/car_training/DataCollected/NForward'
train_img_count = 0
print("Processing Images...")
for categories in CATEGORIES:
    train_img_path = os.path.join(TRAIN_DIR, categories)
    print(train_img_path)
    class_num = CATEGORIES.index(categories)
    for img in os.listdir(train_img_path):
        train_img_count += 1
        try:
            print(class_num)
            image = cv2.imread(os.path.join(train_img_path, img), cv2.IMREAD_GRAYSCALE)
            image = cv2.flip(image, 1)
            if class_num == 0:
                fileName = os.path.join(NRight_DIR, f'Image_{train_img_count}.jpg')
                cv2.imwrite(fileName, image)
            elif class_num == 1:
                fileName = os.path.join(NLeft_DIR, f'Image_{train_img_count}.jpg')
                cv2.imwrite(fileName, image)
            elif class_num == 2:
                fileName = os.path.join(NForward_DIR, f'Image_{train_img_count}.jpg')
                cv2.imwrite(fileName, image)

        except:
            pass
