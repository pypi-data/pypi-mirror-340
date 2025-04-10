
import numpy as np
import matplotlib.pyplot as plt


def pad(img):
    return np.pad(img, ((1, 1), (1, 1)), mode="constant", constant_values=0)


def erosion(img):
    out = np.zeros_like(img)
    img_p = pad(img)
    for i in range(1, img_p.shape[0] - 1):
        for j in range(1, img_p.shape[1] - 1):
            region = img_p[i - 1 : i + 2, j - 1 : j + 2]
            if np.all(region == 1):
                out[i - 1, j - 1] = 1
    return out


def dilation(img):
    out = np.zeros_like(img)
    img_p = pad(img)
    for i in range(1, img_p.shape[0] - 1):
        for j in range(1, img_p.shape[1] - 1):
            region = img_p[i - 1 : i + 2, j - 1 : j + 2]
            if np.any(region == 1):
                out[i - 1, j - 1] = 1
    return out


def thinning(img):
    prev = np.zeros_like(img)
    curr = img.copy()
    while not np.array_equal(prev, curr):
        prev = curr.copy()
        curr = curr - erosion(curr)
    return curr


def thickening(img):
    prev = np.zeros_like(img)
    curr = img.copy()
    while not np.array_equal(prev, curr):
        prev = curr.copy()
        curr = curr + dilation(curr)
        curr[curr > 1] = 1
    return curr


def show_all(img):
    ops = {
        "Original": img,
        "Erosion": erosion(img),
        "Dilation": dilation(img),
        "Thinning": thinning(img),
        "Thickening": thickening(img),
    }

    plt.figure(figsize=(10, 6))
    for i, (title, op_img) in enumerate(ops.items()):
        plt.subplot(2, 3, i + 1)
        plt.imshow(op_img, cmap="gray")
        plt.title(title)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


# Example binary image
img_matrix = np.array(
    [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ],
    dtype=np.uint8,
)

show_all(img_matrix)
