# image_processing.py
import os

import cv2
import numpy as np

def binary_threshold(image, threshold=127):
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary

def contrast_stretching(image, min_val=0, max_val=255):
    return cv2.normalize(image, None, alpha=min_val, beta=max_val, norm_type=cv2.NORM_MINMAX)

def negative(image):
    return 255 - image
import numpy as np

def log_transformation(image, log_factor):
    c = (255 / (np.log(1 + np.max(image))))*log_factor
    log_image = c * (np.log(1 + image))
    return np.array(log_image, dtype=np.uint8)

def gamma_correction(image, gamma):
    return np.array(255 * (image / 255) ** gamma, dtype=np.uint8)

def resize_image(image, width=300):
    height = int(image.shape[0] * (width / image.shape[1]))
    return cv2.resize(image, (width, height))


def load_images(image_folder):
    images, titles = [], []
    for filename in os.listdir(image_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            images.append(cv2.imread(os.path.join(image_folder, filename), cv2.IMREAD_GRAYSCALE))
            titles.append(filename)
    return images, titles
