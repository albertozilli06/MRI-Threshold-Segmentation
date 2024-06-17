import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.color import rgb2gray
from skimage.restoration import denoise_bilateral, denoise_nl_means
from skimage import exposure, filters
from tkinter import Tk, Scale, Button, font, HORIZONTAL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from glob import glob

# Load JPEG images from a specified folder
def load_jpegs(folder_path):
    """
    Load all JPEG images from a specified folder.

    Parameters:
    folder_path (str): Path to the folder containing JPEG images.

    Returns:
    images (list): List of loaded images as NumPy arrays.
    """
    try:
        print(f"Loading images from folder: {folder_path}")
        images = []
        for file_path in sorted(glob(os.path.join(folder_path, '*.jpg'))):
            print(f"Loading image: {file_path}")
            image = np.array(Image.open(file_path))
            images.append(image)
        print(f"Total images loaded: {len(images)}")
        return images
    except Exception as e:
        print(f"Error loading images: {e}")
        return []

# Apply Bilateral Filtering for noise reduction
def apply_bilateral_filter(image):
    """
    Apply bilateral filtering for noise reduction.

    Parameters:
    image (ndarray): Grayscale image.

    Returns:
    filtered_image (ndarray): Bilaterally filtered image.
    """
    print("Applying Bilateral Filter...")
    return denoise_bilateral(image, sigma_color=0.1, sigma_spatial=5)

# Apply Non-Local Means (NL-Means) for noise reduction
def apply_nl_means(image):
    """
    Apply Non-Local Means (NL-Means) filtering for noise reduction.

    Parameters:
    image (ndarray): Grayscale image.

    Returns:
    filtered_image (ndarray): NL-Means filtered image.
    """
    print("Applying Non-Local Means Filter...")
    patch_kw = dict(patch_size=5, patch_distance=3)
    return denoise_nl_means(image, h=0.1 * np.std(image), fast_mode=True, **patch_kw)

# Enhance image: noise reduction and contrast adjustment
def enhance_image(image, method):
    """
    Enhance image using noise reduction and contrast adjustment.

    Parameters:
    image (ndarray): Input image.
    method (str): Noise reduction method ('bilateral' or 'nl_means').

    Returns:
    enhanced_image (ndarray): Enhanced image.
    method_name (str): Name of the enhancement method used.
    """
    print(f"Enhancing image using method: {method}")
    image_gray = rgb2gray(image)
    
    # Choose noise reduction method
    if method == 'bilateral':
        denoised_image = apply_bilateral_filter(image_gray)
        method_name = 'Bilateral Filter'
    elif method == 'nl_means':
        denoised_image = apply_nl_means(image_gray)
        method_name = 'Non-Local Means'
    else:
        raise ValueError("Invalid method. Choose 'bilateral' or 'nl_means'.")
    
    # Contrast adjustment using histogram equalization
    enhanced_image = exposure.equalize_adapthist(denoised_image)
    
    return enhanced_image, method_name

# Apply manual thresholding
def apply_manual_threshold(image, threshold_value):
    """
    Apply manual thresholding to an image.

    Parameters:
    image (ndarray): Input image.
    threshold_value (float): Threshold value.

    Returns:
    segmented_image (ndarray): Binary segmented image.
    """
    print(f"Applying manual threshold: {threshold_value}")
    segmented_image = image > threshold_value
    return segmented_image

# Main function to process images in a folder
def main(folder_path):
    images = load_jpegs(folder_path)
    current_index = [0]

    # Enhance the first image with bilateral filtering
    enhanced_image_bilateral, _ = enhance_image(images[current_index[0]], method='bilateral')
    
    # Enhance the first image with NL-Means
    enhanced_image_nl_means, _ = enhance_image(images[current_index[0]], method='nl_means')
    
    def update_image(threshold_value):
        # Apply manual thresholding
        segmented_image_bilateral = apply_manual_threshold(enhanced_image_bilateral, threshold_value)
        segmented_image_nl_means = apply_manual_threshold(enhanced_image_nl_means, threshold_value)

        # Update plots
        axes[0, 0].imshow(images[current_index[0]], cmap='gray')
        axes[0, 0].set_title('Original Image', fontsize=22)
        
        axes[0, 1].imshow(enhanced_image_bilateral, cmap='gray')
        axes[0, 1].set_title('Enhanced Image - Bilateral Filter', fontsize=22)
        
        axes[1, 1].imshow(segmented_image_bilateral, cmap='gray')
        axes[1, 1].set_title(f'Segmented Image - Bilateral (Threshold: {threshold_value:.2f})', fontsize=22)
        
        axes[0, 2].imshow(enhanced_image_nl_means, cmap='gray')
        axes[0, 2].set_title('Enhanced Image - NL-Means', fontsize=22)
        
        axes[1, 2].imshow(segmented_image_nl_means, cmap='gray')
        axes[1, 2].set_title(f'Segmented Image - NL-Means (Threshold: {threshold_value:.2f})', fontsize=22)

        for a in axes.ravel():
            a.axis('off')

        canvas.draw()

    def next_image():
        if current_index[0] < len(images) - 1:
            current_index[0] += 1
            load_and_update_images()

    def previous_image():
        if current_index[0] > 0:
            current_index[0] -= 1
            load_and_update_images()

    def load_and_update_images():
        nonlocal enhanced_image_bilateral, enhanced_image_nl_means
        enhanced_image_bilateral, _ = enhance_image(images[current_index[0]], method='bilateral')
        enhanced_image_nl_means, _ = enhance_image(images[current_index[0]], method='nl_means')
        update_image(threshold_slider.get())

    # Create a window with Tkinter
    root = Tk()
    root.title("MRI Image Enhancement and Thresholding")
    root.geometry("1600x900")

    obj_font = font.Font(family='Calibri', size=20, weight='bold')

    # Create a figure and axes
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))

    # Add a slider for threshold adjustment
    threshold_slider = Scale(root, from_=0, to=1, orient=HORIZONTAL, resolution=0.01, length=500, width=30, label="Threshold Value", font=obj_font)
    threshold_slider.set(0.5)
    threshold_slider.pack(side="bottom")

    # Add a "Next" button
    next_button = Button(root, text="Next", font=obj_font, command=next_image, width=15, height=3, bg='blue', fg='yellow')
    next_button.pack(side="right")

    # Add a "Previous" button
    previous_button = Button(root, text="Previous", font=obj_font, command=previous_image, width=15, height=3 , bg='blue', fg='yellow')
    previous_button.pack(side="left")

    # Update the image when the slider value changes
    threshold_slider.configure(command=lambda v: update_image(float(v)))

    # Embed the matplotlib figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Initialize the display
    update_image(threshold_slider.get())

    # Start the Tkinter event loop
    root.mainloop()

# Set the folder path
folder_path = r'Your folder path'  # Replace with your actual folder path
main(folder_path)
