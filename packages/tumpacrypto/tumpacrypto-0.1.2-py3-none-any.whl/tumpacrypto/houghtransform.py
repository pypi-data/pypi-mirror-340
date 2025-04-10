import cv2
import numpy as np
import matplotlib.pyplot as plt


class HoughLineDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.original_image = None
        self.gray = None
        self.blurred = None
        self.edges = None
        self.lines = None
        self.lines_p = None
        self.image_with_lines = None
        self.image_with_lines_p = None

        # Parameters for edge detection
        self.low_threshold = 50
        self.high_threshold = 150

        # Parameters for Hough transform
        self.rho = 1
        self.theta = np.pi / 180
        self.threshold = 100
        self.min_line_length = 100
        self.max_line_gap = 10

    def load_image(self):
        self.original_image = cv2.imread(self.image_path)
        if self.original_image is None:
            print(f"Error: Could not open or find the image at {self.image_path}")
            return False
        return True

    def preprocess_image(self):
        self.gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        self.edges = cv2.Canny(
            self.blurred, self.low_threshold, self.high_threshold, apertureSize=3
        )

    def apply_standard_hough_transform(self):
        self.lines = cv2.HoughLines(self.edges, self.rho, self.theta, self.threshold)
        self.image_with_lines = self.original_image.copy()

        if self.lines is not None:
            for i in range(min(len(self.lines), 10)):  # Limit to 10 lines for clarity
                rho, theta = self.lines[i][0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(self.image_with_lines, (x1, y1), (x2, y2), (0, 0, 255), 2)

    def apply_probabilistic_hough_transform(self):
        self.lines_p = cv2.HoughLinesP(
            self.edges,
            self.rho,
            self.theta,
            self.threshold,
            None,
            self.min_line_length,
            self.max_line_gap,
        )
        self.image_with_lines_p = self.original_image.copy()

        if self.lines_p is not None:
            for line in self.lines_p:
                x1, y1, x2, y2 = line[0]
                cv2.line(self.image_with_lines_p, (x1, y1), (x2, y2), (0, 255, 0), 2)

    def visualize_results(self):
        plt.figure(figsize=(15, 10))

        # Original image
        plt.subplot(2, 2, 1)
        plt.imshow(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB))
        plt.title("Original Image")
        plt.axis("off")

        # Edge image
        plt.subplot(2, 2, 2)
        plt.imshow(self.edges, cmap="gray")
        plt.title("Edge Image")
        plt.axis("off")

        # Image with standard Hough lines
        plt.subplot(2, 2, 3)
        plt.imshow(cv2.cvtColor(self.image_with_lines, cv2.COLOR_BGR2RGB))
        plt.title("Standard Hough Lines (first 10)")
        plt.axis("off")

        # Image with probabilistic Hough lines
        plt.subplot(2, 2, 4)
        plt.imshow(cv2.cvtColor(self.image_with_lines_p, cv2.COLOR_BGR2RGB))
        plt.title("Probabilistic Hough Lines")
        plt.axis("off")

        plt.tight_layout()
        plt.show()

    def set_edge_detection_params(self, low_threshold, high_threshold):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def set_hough_transform_params(
        self, rho, theta, threshold, min_line_length, max_line_gap
    ):
        self.rho = rho
        self.theta = theta
        self.threshold = threshold
        self.min_line_length = min_line_length
        self.max_line_gap = max_line_gap

    def run_detection(self):
        if not self.load_image():
            return False

        self.preprocess_image()
        self.apply_standard_hough_transform()
        self.apply_probabilistic_hough_transform()
        self.visualize_results()
        return True


if __name__ == "__main__":
    detector = HoughLineDetector("D:/Machine-Vision/road.jpeg")

    # Optionally set custom parameters
    # detector.set_edge_detection_params(40, 120)
    # detector.set_hough_transform_params(1, np.pi/180, 80, 50, 5)

    detector.run_detection()
