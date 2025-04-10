import numpy as np
import cv2
import matplotlib.pyplot as plt


class Affirm:
    def __init__(self):
        pass

    def rgb2cmy(self, img):
        colarr = []
        for i in img:
            rowarr = []
            for j in i:
                c = 1 - (j[0] / 255.0)
                m = 1 - (j[1] / 255.0)
                y = 1 - (j[2] / 255.0)
                rowarr.append([c, m, y])
            colarr.append(rowarr)
            # plt.imshow(np.array(cmy))
        return np.array(colarr)

    def cmy2rgb(self, img):
        rowarr = []
        for i in img:
            colarr = []
            for j in i:
                r = round((1 - j[0]) * 255)
                g = round((1 - j[1]) * 255)
                b = round((1 - j[2]) * 255)
                colarr.append([r, g, b])
            rowarr.append(colarr)

        return np.array(rowarr)

    def rgb2hsi(self, img):
        img = np.float32(img) / 255.0
        r = img[:, :, 0]
        g = img[:, :, 1]
        b = img[:, :, 2]

        i = (r + g + b) / 3.0
        saturation = 1 - (np.minimum(np.minimum(r, g), b) / i + 1e-8)

        nr = 0.5 * ((r - g) + (r - b))
        dr = np.sqrt((r - g) ** 2 + (r - b) * (g - b))
        theta = np.arccos(nr / dr)

        hue = np.where(b <= g, theta, 2 * np.pi - theta)

        hue = hue / (2 * np.pi)
        hsi = cv2.merge((hue, saturation, i))

        return hsi

    def HSI_TO_RGB(self, hsi_img):
        # Extract H, S, I channels
        H = hsi_img[:, :, 0] * 2 * np.pi  # Convert normalized Hue back to [0, 2*pi]
        S = hsi_img[:, :, 1]  # Saturation remains in [0, 1]
        I = hsi_img[:, :, 2]
        # Initialize RGB arrays

        R = np.zeros_like(H)
        G = np.zeros_like(H)
        B = np.zeros_like(H)

        # Region 1: 0 <= H < 2*pi/3
        region1 = H < 2 * np.pi / 3
        B[region1] = I[region1] * (1 - S[region1])
        R[region1] = I[region1] * (
            1 + S[region1] * np.cos(H[region1]) / np.cos(np.pi / 3 - H[region1])
        )
        G[region1] = 3 * I[region1] - (R[region1] + B[region1])
        # Region 2: 2*pi/3 <= H < 4*pi/3
        region2 = (H >= 2 * np.pi / 3) & (H < 4 * np.pi / 3)
        H_adj = H[region2] - 2 * np.pi / 3
        R[region2] = I[region2] * (1 - S[region2])
        G[region2] = I[region2] * (
            1 + S[region2] * np.cos(H_adj) / np.cos(np.pi / 3 - H_adj)
        )
        B[region2] = 3 * I[region2] - (R[region2] + G[region2])
        # Region 3: 4*pi/3 <= H < 2*pi
        region3 = H >= 4 * np.pi / 3
        H_adj = H[region3] - 4 * np.pi / 3
        G[region3] = I[region3] * (1 - S[region3])
        B[region3] = I[region3] * (
            1 + S[region3] * np.cos(H_adj) / np.cos(np.pi / 3 - H_adj)
        )
        R[region3] = 3 * I[region3] - (G[region3] + B[region3])
        # Combine R, G, B and clip to valid range [0, 1]
        rgb_img = np.clip(cv2.merge((R, G, B)), 0, 1)

        return rgb_img

    def rgb2neg(self, img):
        # img=cv2.imread('img.jpeg',cv2.IMREAD_GRAYSCALE)
        img = 255 - img
        return img

    def histogramequalization(self, img):

        h = np.zeros(256)
        for pixel in img.flatten():
            h[pixel] += 1

        # calculate cdf
        cdf = np.zeros(256)
        cdf[0] = h[0]
        for i in range(1, 256):
            cdf[i] = cdf[i - 1] + h[i]

        normalized_hist = np.round(cdf * 255 / (img.shape[0] * img.shape[1]))
        equalized_img = normalized_hist[img]
        return equalized_img.astype("uint8")
        # how to show
        r = img[:, :, 0]
        g = img[:, :, 1]
        b = img[:, :, 2]
        r = histogramequalization(r)
        g = histogramequalization(g)
        b = histogramequalization(b)
        equalized_img = cv2.merge((r, g, b))

        plt.subplot(1, 2, 1)
        plt.imshow(r, cmap="Reds")
        plt.subplot(1, 2, 2)
        plt.imshow(g, cmap="Greens")
        plt.show()

    def minfilter(self, window):
        min = window[0]
        for val in window:
            if val < min:
                min = val
        return min

    def maxfilter(self, window):
        max = window[0]
        for val in window:
            if val > max:
                max = val
        return max

    def medianfilter(self, window):
        window.sort()
        return window[len(window) // 2]

    def applyfilter(self, img, filter, kernel_size):
        pad = kernel_size // 2
        filter_image = np.zeros_like(img)
        pad_img = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(img.shape[2]):
                    window = []
                    for ki in range(kernel_size):
                        for kj in range(kernel_size):
                            window.append(pad_img[i + ki, j + kj, k])

                    if filter == "min":
                        filter_image[i, j, k] = self.minfilter(window)
                    if filter == "max":
                        filter_image[i, j, k] = self.maxfilter(window)
                    if filter == "median":
                        filter_image[i, j, k] = self.medianfilter(window)
        return filter_image
        # how to run
        img = cv2.imread("img.jpeg")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(2, 2, 1)
        plt.imshow(img)
        min_img = applyfilter(img, "min", 3)
        max_img = applyfilter(img, "max", 3)
        median_img = applyfilter(img, "median", 3)
        plt.subplot(2, 2, 2)
        plt.imshow(min_img)
        plt.subplot(2, 2, 3)
        plt.imshow(max_img)
        plt.subplot(2, 2, 4)
        plt.imshow(median_img)
        plt.show()

    def bilinear_interpolation(x, y, x1, y1, x2, y2, Q11, Q12, Q21, Q22):

        if x1 == x2 and y1 == y2:
            return Q11
        if x1 == x2:
            R1 = Q11
            R2 = Q12
        else:
            R1 = ((x2 - x) / (x2 - x1)) * Q11 + ((x - x1) / (x2 - x1)) * Q21
            R2 = ((x2 - x) / (x2 - x1)) * Q12 + ((x - x1) / (x2 - x1)) * Q22
        if y1 == y2:
            P = R1
        else:
            P = ((y2 - y) / (y2 - y1)) * R1 + ((y - y1) / (y2 - y1)) * R2
        return round(P, 2)

        # rest of the code
        # Creating an 8x10 matrix initialized with zeros
        matrix = [[0 for _ in range(10)] for _ in range(8)]
        # Known intensity values at the corners
        known_values = {(0, 0): 200, (0, 9): 100, (7, 0): 20, (7, 9): 0}
        # Assigning known values to the matrix
        for (x, y), value in known_values.items():
            matrix[x][y] = value
        # Points where interpolation is required
        interpolation_points = [(1, 1), (2, 9), (3, 2), (4, 5), (5, 3), (6, 7), (7, 5)]
        interpolated_values = {}
        # Performing bilinear interpolation
        for x, y in interpolation_points:
            x1, x2 = 0, 7
            y1, y2 = 0, 9
            Q11 = matrix[x1][y1]
            Q12 = matrix[x1][y2]
            Q21 = matrix[x2][y1]
            Q22 = matrix[x2][y2]
            interpolated_values[(x, y)] = bilinear_interpolation(
                x, y, x1, y1, x2, y2, Q11, Q12, Q21, Q22
            )
            matrix[x][y] = interpolated_values[(x, y)]
        # Displaying interpolated values
        print("\nInterpolated Intensity Values:")
        for (x, y), value in interpolated_values.items():
            print(f"Intensity at ({x}, {y}): {value}")
        # Displaying the updated 8x10 matrix
        print("\n8x10 Matrix with Interpolated Values:")
        for row in matrix:
            print(row)
