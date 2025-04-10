import cv2
import matplotlib.pyplot as plt
import numpy as np
# Load the image
img = cv2.imread("img.jpeg")
if img is None:
    print("Error: Could not load image. Check file path.")
    exit()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
contrast_enhanced_gray = clahe.apply(gray)
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(gray, cmap='gray')
plt.title("Grayscale Image")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(contrast_enhanced_gray, cmap='gray')
plt.title("Contrast Enhanced (CLAHE)")
plt.axis("off")
plt.tight_layout()
plt.show()
ret, bin_img = cv2.threshold(contrast_enhanced_gray, 0, 255, 
cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
opened_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, 
iterations=2)
sure_bg = cv2.dilate(opened_img, kernel, iterations=5) # Increased iterations
dist = cv2.distanceTransform(opened_img, cv2.DIST_L2, 5)
threshold_value = 0.05
ret, sure_fg = cv2.threshold(dist, threshold_value * dist.max(), 255, 
cv2.THRESH_BINARY)
sure_fg = sure_fg.astype(np.uint8)
unknown = cv2.subtract(sure_bg, sure_fg)
plt.figure(figsize=(15, 5))
plt.subplot(1, 4, 1)
plt.imshow(bin_img, cmap='gray')
plt.title("Binary Image (Otsu on CLAHE)")
plt.axis("off")
plt.subplot(1, 4, 2)
plt.imshow(opened_img, cmap='gray')
plt.title("After Morphological Opening")
plt.axis("off")
plt.subplot(1, 4, 3)
plt.imshow(sure_fg, cmap='gray')
plt.title(f"Sure Foreground (Thresh={threshold_value})")
plt.axis("off")
plt.subplot(1, 4, 4)
plt.imshow(unknown, cmap='gray')
plt.title("Unknown Region")
plt.axis("off")
plt.tight_layout()
plt.show()


##
ret, markers = cv2.connectedComponents(sure_fg)
markers += 1 # Add one so background is 1, not 0
markers[unknown == 255] = 0 # Mark unknown region with 0
# Apply watershed
markers = cv2.watershed(img, markers) # Apply watershed on the 

# --- Final Result Visualization --
result_img = img.copy()
labels = np.unique(markers)
segment_contours = []
# Set boundary color (e.g., bright green)
boundary_color = (0, 255, 0)
boundary_thickness = 1 # Make lines thinner for better visibility
# Draw boundaries directly from the markers image
result_img[markers == -1] = boundary_color
# Display final result
plt.figure(figsize=(10, 8))
plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
plt.title("Watershed Segmentation Result (with CLAHE)")
plt.axis("off")
plt.tight_layout()
plt.show()
# Display markers for debugging
plt.figure(figsize=(10, 8))
plt.imshow(markers, cmap='tab20b') # Use a qualitative colormap
plt.title(
"Watershed Markers")
plt.axis(
"off")
plt.tight_layout()
plt.show()


##
