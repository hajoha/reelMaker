import inline
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import canny
from skimage import data, morphology
from skimage.segmentation import watershed
from skimage.color import rgb2gray, label2rgb
import scipy.ndimage as nd
from skimage.filters.edges import sobel
import cv2

plt.rcParams["figure.figsize"] = (12, 8)

#https://stackabuse.com/opencv-adaptive-thresholding-in-python-with-cv2adaptivethreshold/
def generate_img(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    mask = cv2.adaptiveThreshold(blurred,
                              255,
                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY,
                              31,
                              6)



    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax[1].imshow(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
    plt.show()


if __name__ == '__main__':
    generate_img("../files/foo.JPG")
