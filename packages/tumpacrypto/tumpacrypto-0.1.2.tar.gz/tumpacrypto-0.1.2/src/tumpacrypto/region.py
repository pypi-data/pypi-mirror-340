import cv2
import numpy as np
import matplotlib.pyplot as plt


class RegionGrowing:
    def __init__(self, threshold=10):
        self.threshold = threshold

    def grow(self, image, seed_point):
        height, width = image.shape
        mask = np.zeros((height, width), dtype=np.uint8)
        visited = np.zeros((height, width), dtype=np.bool_)

        seed_value = image[seed_point]
        queue = [seed_point]
        mask[seed_point] = 1
        visited[seed_point] = True

        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.pop(0)
            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width:
                    if (
                        not visited[nx, ny]
                        and abs(int(image[nx, ny]) - int(seed_value)) < self.threshold
                    ):
                        mask[nx, ny] = 1
                        visited[nx, ny] = True
                        queue.append((nx, ny))

        return mask


class SplitAndMerge:
    def __init__(self, split_threshold, merge_threshold):
        self.split_threshold = split_threshold
        self.merge_threshold = merge_threshold

    def is_homogeneous(self, region):
        min_val, max_val = np.min(region), np.max(region)
        return (max_val - min_val) <= self.split_threshold

    def recursive_split(self, region):
        rows, cols = region.shape
        if rows <= 1 or cols <= 1:
            return np.zeros_like(region, dtype=np.uint8)

        if self.is_homogeneous(region):
            return np.ones_like(region, dtype=np.uint8)

        mid_row, mid_col = rows // 2, cols // 2
        top_left = region[:mid_row, :mid_col]
        top_right = region[:mid_row, mid_col:]
        bottom_left = region[mid_row:, :mid_col]
        bottom_right = region[mid_row:, mid_col:]

        segmented_quadrants = np.zeros_like(region, dtype=np.uint8)
        segmented_quadrants[:mid_row, :mid_col] = self.recursive_split(top_left)
        segmented_quadrants[:mid_row, mid_col:] = self.recursive_split(top_right)
        segmented_quadrants[mid_row:, :mid_col] = self.recursive_split(bottom_left)
        segmented_quadrants[mid_row:, mid_col:] = self.recursive_split(bottom_right)

        return segmented_quadrants

    def merge_regions(self, segmented, image):
        rows, cols = segmented.shape
        merged = segmented.copy()

        for i in range(rows - 1):
            for j in range(cols - 1):
                if merged[i, j] != merged[i, j + 1]:
                    region1 = image[i, j]
                    region2 = image[i, j + 1]
                    if abs(region1 - region2) <= self.merge_threshold:
                        merged[i, j + 1] = merged[i, j]

                if merged[i, j] != merged[i + 1, j]:
                    region1 = image[i, j]
                    region2 = image[i + 1, j]
                    if abs(region1 - region2) <= self.merge_threshold:
                        merged[i + 1, j] = merged[i, j]

        return merged

    def process(self, image):
        split_image = self.recursive_split(image)
        merged_image = self.merge_regions(split_image, image)
        return split_image, merged_image


def display_results(images, titles):
    n = len(images)
    plt.figure(figsize=(5 * n, 5))
    for i in range(n):
        plt.subplot(1, n, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    try:
        # Region Growing
        image_path = "your_image.jpg"
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            raise Exception("Error: Could not read the image")

        seed = (100, 100)
        region_grower = RegionGrowing(threshold=15)
        segmented_region = region_grower.grow(image, seed)

        display_results(
            [image, segmented_region], ["Original Image", "Segmented Region"]
        )

        # Split and Merge
        split_merge = SplitAndMerge(split_threshold=20, merge_threshold=20)
        split_result, merge_result = split_merge.process(image)

        display_results(
            [image, split_result, merge_result],
            ["Original Image", "After Splitting", "After Merging"],
        )

    except Exception as e:
        print(f"Error: {e}")
