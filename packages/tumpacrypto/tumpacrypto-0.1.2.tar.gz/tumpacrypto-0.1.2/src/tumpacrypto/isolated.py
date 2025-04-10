import numpy as np
import matplotlib.pyplot as plt


def pad(img):
    return np.pad(img, ((1, 1), (1, 1)), mode="constant", constant_values=0)


# Isolated point removal
def remove_isolated_points(img):
    out = img.copy()
    img_p = pad(img)
    for i in range(1, img_p.shape[0] - 1):
        for j in range(1, img_p.shape[1] - 1):
            if img_p[i, j] == 1:
                region = img_p[i - 1 : i + 2, j - 1 : j + 2]
                if np.sum(region) == 1:
                    out[i - 1, j - 1] = 0
    return out


# Zhang-Suen thinning (skeletal thinning)
def zhang_suen_thinning(img):
    img = img.copy()
    changing = True
    while changing:
        changing = False
        m1 = []
        m2 = []
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                P = img[i - 1 : i + 2, j - 1 : j + 2].flatten()
                P2 = P[1]
                P3 = P[2]
                P4 = P[5]
                P5 = P[8]
                P6 = P[7]
                P7 = P[6]
                P8 = P[3]
                P9 = P[0]
                if img[i, j] == 1:
                    A = (
                        (P2 == 0 and P3 == 1)
                        + (P3 == 0 and P4 == 1)
                        + (P4 == 0 and P5 == 1)
                        + (P5 == 0 and P6 == 1)
                        + (P6 == 0 and P7 == 1)
                        + (P7 == 0 and P8 == 1)
                        + (P8 == 0 and P9 == 1)
                        + (P9 == 0 and P2 == 1)
                    )
                    B = sum([P2, P3, P4, P5, P6, P7, P8, P9])
                    if (
                        2 <= B <= 6
                        and A == 1
                        and P2 * P4 * P6 == 0
                        and P4 * P6 * P8 == 0
                    ):
                        m1.append((i, j))
        for i, j in m1:
            img[i, j] = 0
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                P = img[i - 1 : i + 2, j - 1 : j + 2].flatten()
                P2 = P[1]
                P3 = P[2]
                P4 = P[5]
                P5 = P[8]
                P6 = P[7]
                P7 = P[6]
                P8 = P[3]
                P9 = P[0]
                if img[i, j] == 1:
                    A = (
                        (P2 == 0 and P3 == 1)
                        + (P3 == 0 and P4 == 1)
                        + (P4 == 0 and P5 == 1)
                        + (P5 == 0 and P6 == 1)
                        + (P6 == 0 and P7 == 1)
                        + (P7 == 0 and P8 == 1)
                        + (P8 == 0 and P9 == 1)
                        + (P9 == 0 and P2 == 1)
                    )
                    B = sum([P2, P3, P4, P5, P6, P7, P8, P9])
                    if (
                        2 <= B <= 6
                        and A == 1
                        and P2 * P4 * P8 == 0
                        and P2 * P6 * P8 == 0
                    ):
                        m2.append((i, j))
        for i, j in m2:
            img[i, j] = 0
        if m1 or m2:
            changing = True
    return img


# Display results
def show_isolation_and_thinning(img):
    clean = remove_isolated_points(img)
    thin = zhang_suen_thinning(clean)
    plt.figure(figsize=(12, 4))
    titles = ["Original", "No Isolated Points", "Skeletal Thinning"]
    imgs = [img, clean, thin]
    for i in range(3):
        plt.subplot(1, 3, i + 1)
        plt.imshow(imgs[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")
    plt.tight_layout()
    plt.show()


# Example binary image with isolated point
img_matrix = np.array(
    [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ],
    dtype=np.uint8,
)

show_isolation_and_thinning(img_matrix)
