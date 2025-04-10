import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, gaussian_filter

class EdgeDetector:
    @staticmethod
    def sobel(img):
        """Apply Sobel edge detection with self-contained kernels."""
        kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        gx = convolve(img, kx)
        gy = convolve(img, ky)
        return np.sqrt(gx**2 + gy**2)
    
    @staticmethod
    def prewitt(img):
        """Apply Prewitt edge detection with self-contained kernels."""
        kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        ky = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        gx = convolve(img, kx)
        gy = convolve(img, ky)
        return np.sqrt(gx**2 + gy**2)
    
    @staticmethod
    def laplacian(img):
        """Apply Laplacian edge detection with self-contained kernel."""
        k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        return convolve(img, k)
    
    @staticmethod
    def log(img, sigma=1):
        """Apply Laplacian of Gaussian (LoG) edge detection with self-contained kernel."""
        blurred = gaussian_filter(img, sigma)
        k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        return convolve(blurred, k)
    
    @staticmethod
    def normalize(img):
        """Normalize image to 0-255 range."""
        img = np.abs(img)
        if img.max() > 0:  # Avoid division by zero
            img = img / img.max() * 255
        return img.astype(np.uint8)
    
    def detect_all(self, img):
        """Apply all edge detection methods and return results."""
        return {
            'Sobel': self.normalize(self.sobel(img)),
            'Prewitt': self.normalize(self.prewitt(img)),
            'Laplacian': self.normalize(self.laplacian(img)),
            'LoG': self.normalize(self.log(img, 1.0))
        }
    
    def visualize_all(self, img):
        """Visualize all edge detection methods."""
        edges = self.detect_all(img)
        
        plt.figure(figsize=(12, 6))
        for i, (title, edge_img) in enumerate(edges.items()):
            plt.subplot(2, 2, i+1)
            plt.imshow(edge_img, cmap='gray')
            plt.title(title)
            plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        return edges


if __name__ == "__main__":
    # Example 2D matrix image
    img_matrix = np.array([
        [100, 100, 100, 100, 100, 100],
        [100, 200, 200, 200, 200, 100],
        [100, 200, 50, 50, 200, 100],
        [100, 200, 50, 50, 200, 100],
        [100, 200, 200, 200, 200, 100],
        [100, 100, 100, 100, 100, 100]
    ], dtype=np.float32)
    
    # Create edge detector and visualize results
    detector = EdgeDetector()
    detector.visualize_all(img_matrix)
    
    # Example of using individual methods independently
    sobel_edges = EdgeDetector.sobel(img_matrix)
    normalized_sobel = EdgeDetector.normalize(sobel_edges)
    
    plt.figure(figsize=(6, 6))
    plt.imshow(normalized_sobel, cmap='gray')
    plt.title('Sobel Edge Detection')
    plt.axis('off')
    plt.show()
