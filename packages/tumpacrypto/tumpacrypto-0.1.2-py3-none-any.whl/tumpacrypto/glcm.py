import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.feature import graycomatrix, graycoprops
from skimage.color import rgb2gray

class GLCMAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.gray_image = None
        self.glcm = None
        self.feature_results = {}
        self.distances = [1, 3, 5]
        self.angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        self.properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']
    
    def load_image(self):
        try:
            im_frame = Image.open(self.image_path)
            print("Image loaded successfully")
            self.image = np.array(im_frame.convert('RGB'))
            self.gray_image = (255 * rgb2gray(self.image)).astype(np.uint8)
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def display_images(self):
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(self.image)
        plt.title("Original Image")
        plt.axis("off")
        
        plt.subplot(1, 2, 2)
        plt.imshow(self.gray_image, cmap='gray')
        plt.title("Grayscale Image")
        plt.axis("off")
        
        plt.tight_layout()
        plt.show()
    
    def calculate_glcm(self):
        self.glcm = graycomatrix(
            self.gray_image,
            distances=self.distances,
            angles=self.angles,
            levels=256,
            symmetric=True,
            normed=True
        )
    
    def calculate_features(self):
        for prop in self.properties:
            self.feature_results[prop] = graycoprops(self.glcm, prop)
    
    def plot_features(self):
        plt.figure(figsize=(15, 10))
        for i, prop in enumerate(self.properties):
            plt.subplot(2, 3, i+1)
            for j, d in enumerate(self.distances):
                plt.plot(self.angles, self.feature_results[prop][j, :], 'o-', label=f'distance={d}')
            plt.title(prop.capitalize())
            plt.xlabel('Angle (radians)')
            plt.ylabel(prop)
            plt.grid(True)
            plt.legend()
        plt.tight_layout()
        plt.show()
    
    def print_specific_features(self, distance=1, angle=np.pi/2):
        dist_idx = self.distances.index(distance) if distance in self.distances else 0
        angle_idx = self.angles.index(angle) if angle in self.angles else 0
        
        print(f"\nGLCM Features at distance={distance}, angle={angle} radians:")
        print("-" * 50)
        for prop in self.properties:
            value = self.feature_results[prop][dist_idx, angle_idx]
            print(f"{prop.capitalize()}: {value:.6f}")
    
    def display_glcm_subset(self, subset_size=16, distance_idx=0, angle_idx=0):
        plt.figure(figsize=(8, 6))
        glcm_subset = self.glcm[0:subset_size, 0:subset_size, distance_idx, angle_idx]
        plt.imshow(glcm_subset, cmap='hot', interpolation='nearest')
        plt.colorbar(label='Probability')
        plt.title(f'GLCM Subset (d={self.distances[distance_idx]}, θ={self.angles[angle_idx]} rad)')
        plt.xlabel('Gray Level j')
        plt.ylabel('Gray Level i')
        plt.tight_layout()
        plt.show()
    
    def run_analysis(self):
        if not self.load_image():
            return False
        
        self.display_images()
        self.calculate_glcm()
        self.calculate_features()
        self.plot_features()
        self.print_specific_features()
        self.display_glcm_subset()
        return True


if __name__ == "__main__":
    # Create an instance of the GLCMAnalyzer class
    analyzer = GLCMAnalyzer("D:\Machine-Vision\input.png")
    
    # Run the full analysis
    analyzer.run_analysis()
