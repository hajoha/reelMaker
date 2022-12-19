import inline
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import cv2
import rembg
import skimage.io
from PIL import Image
from skimage import measure
from skimage.exposure import exposure
from sklearn.impute import SimpleImputer
from skimage.morphology import flood_fill
from rembg import remove
import cv2

plt.rcParams["figure.figsize"] = (12, 8)


def plot_imgs(img, blurred, mask, imglabeled, fill, first_half, second_half):
    fig, ax = plt.subplots(1, 7, figsize=(12, 5))
    ax[0].imshow(img)
    ax[1].imshow(blurred, cmap="gray")
    ax[2].imshow(mask, cmap="gray")
    ax[3].imshow(imglabeled)
    ax[4].imshow(fill, cmap="gray")
    ax[5].imshow(first_half)
    ax[6].imshow(second_half)
    plt.show()


def remove_background(image, in_path, out_path):
    filename = image.removesuffix(".JPG")

    input = cv2.imread(f"{in_path}/{image}")
    session = rembg.new_session(model_name="u2net")
    output = remove(input, session=session)
    # mask = output.copy()
    # mask[output != 0] = 0
    # mask[output == 0] = 255
    # mask = mask[...,0:1]
    # mask = cv2.GaussianBlur(mask, ksize=None, sigmaX=7)
    # masked = cv2.bitwise_and(input, input, mask=mask)
    # #masked[masked == 0] = 255
    cv2.imwrite(f"{out_path}/{filename}_1.png", output)
    cv2.imwrite(f"{out_path}/{filename}_2.png", input)


#    cv2.imwrite(f"{out_path}/{filename}_2.png", second_half.astype(np.uint8))


# https://stackabuse.com/opencv-adaptive-thresholding-in-python-with-cv2adaptivethreshold/
def generate_img(image, in_path, out_path):
    filename = image.removesuffix(".JPG")
    img = skimage.io.imread(f"{in_path}/{image}")
    gray = skimage.color.rgb2gray(img)
    blurred = skimage.filters.gaussian(gray, sigma=3)
    t = skimage.filters.threshold_isodata(blurred)
    mask = blurred > t
    mask = mask.astype(int)
    print("Found automatic threshold t = {}.".format(t))
    imglabeled, island_count = measure.label(mask, background=0,
                                             return_num=True,
                                             connectivity=1)
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

    first_half = img * np.dstack([fill] * 3)
    first_half[fill == 0] = 255

    inv_fill = np.where((fill == 0) | (fill == 1), fill ^ 1, fill)
    second_half = img * np.dstack([inv_fill] * 3)
    second_half[inv_fill == 0] = 255

    skimage.io.imsave(f"{out_path}/{filename}_1.png", first_half.astype(np.uint8))
    skimage.io.imsave(f"{out_path}/{filename}_2.png", second_half.astype(np.uint8))

    # plot_imgs(img, blurred, mask,
    #          imglabeled, fill,
    #          first_half, second_half)


if __name__ == '__main__':
    generate_img("../files/foo.JPG")
