import inline
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import cv2
import skimage.io
from skimage import measure
from sklearn.impute import SimpleImputer
from skimage.morphology import flood_fill

plt.rcParams["figure.figsize"] = (12, 8)


# https://stackabuse.com/opencv-adaptive-thresholding-in-python-with-cv2adaptivethreshold/
def generate_img(image):
    img = skimage.io.imread(image)
    gray = skimage.color.rgb2gray(img)
    blurred = skimage.filters.gaussian(gray, sigma=6)
    t = skimage.filters.threshold_otsu(blurred)
    mask = blurred > t
    mask = mask.astype(int)
    print("Found automatic threshold t = {}.".format(t))
    imglabeled, island_count = measure.label(mask, background=0,
                                             return_num=True,
                                             connectivity=2)
    regions = measure.regionprops(imglabeled)
    sorted_region = sorted(
            regions,
            key=lambda r: r.area,
            reverse=True,
    )
    fill = mask.copy()
    head = sorted_region.pop(0)
    for region in sorted_region:
        fill = flood_fill(fill, tuple(region.coords[0]), new_value=0)

    fig, ax = plt.subplots(1, 5, figsize=(12, 5))
    ax[0].imshow(img)
    ax[1].imshow(blurred, cmap="gray")
    ax[2].imshow(mask, cmap="gray")
    ax[3].imshow(imglabeled)
    ax[4].imshow(fill, cmap="gray")
    plt.show()


if __name__ == '__main__':
    generate_img("../files/foo.JPG")
