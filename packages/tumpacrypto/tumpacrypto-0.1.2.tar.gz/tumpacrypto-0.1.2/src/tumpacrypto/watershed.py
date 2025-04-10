import cv2
import numpy as np
import matplotlib.pyplot as plt

def watershed_segmentation(image_path):
    # Step 1: Load the image
    img = cv2.imread(image_path)
    img_copy = img.copy()
    
    # Step 2: Convert to grayscale and apply thresholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Step 3: Noise removal with morphological operations
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Step 4: Find sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Step 5: Find sure foreground area using distance transform
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    
    # Step 6: Find unknown region
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Step 7: Marker labeling
    _, markers = cv2.connectedComponents(sure_fg)
    
    # Add 1 to all labels so that background is not 0, but 1
    markers = markers + 1
    
    # Mark the unknown region with 0
    markers[unknown == 255] = 0
    
    # Step 8: Apply watershed algorithm
    markers = cv2.watershed(img, markers)
    
    # Step 9: Visualize the results
    img[markers == -1] = [255, 0, 0]  # Mark watershed boundaries in blue
    
    # Display results
    plt.figure(figsize=(12, 8))
    
    plt.subplot(231), plt.imshow(cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)), plt.title('Original Image')
    plt.subplot(232), plt.imshow(thresh, cmap='gray'), plt.title('Thresholded Image')
    plt.subplot(233), plt.imshow(sure_bg, cmap='gray'), plt.title('Sure Background')
    plt.subplot(234), plt.imshow(sure_fg, cmap='gray'), plt.title('Sure Foreground')
    plt.subplot(235), plt.imshow(dist_transform, cmap='jet'), plt.title('Distance Transform')
    plt.subplot(236), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('Watershed Result')
    
    plt.tight_layout()
    plt.show()
    
    return img

# Usage example
if __name__ == "__main__":
    # Replace with your image path
    image_path = "img.jpeg"
    segmented_image = watershed_segmentation(image_path)
