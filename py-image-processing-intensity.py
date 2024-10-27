import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, StringVar
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Folder containing images
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'images')

def binary_threshold(image, threshold=127):
    """Apply binary thresholding to the image."""
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary

def contrast_stretching(image, min_val=0, max_val=255):
    """Apply contrast stretching to the image."""
    stretched = cv2.normalize(image, None, alpha=min_val, beta=max_val, norm_type=cv2.NORM_MINMAX)
    return stretched

def negative(image):
    """Create a negative of the image."""
    return 255 - image

def log_transformation(image):
    """Apply logarithmic transformation to the image."""
    c = 255 / (np.log(1 + np.max(image)))
    log_image = c * (np.log(1 + image))
    log_image = np.array(log_image, dtype=np.uint8)
    return log_image

def gamma_correction(image, gamma):
    """Apply gamma correction to the image."""
    gamma_corrected = np.array(255 * (image / 255) ** gamma, dtype=np.uint8)
    return gamma_corrected

def resize_image(image, width=300):
    """Resize the image to a specified width while maintaining aspect ratio."""
    height = int(image.shape[0] * (width / image.shape[1]))
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def display_images(images, titles):
    """Display multiple images in a single Tkinter window."""
    for widget in grid_frame.winfo_children():
        widget.destroy()  # Clear existing images

    for i in range(len(images)):
        resized_image = resize_image(images[i])

        # Convert the image to RGB format and then to a PhotoImage
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)  # Convert to RGB
        image_pil = Image.fromarray(image_rgb)  # Convert to PIL Image
        image_tk = ImageTk.PhotoImage(image_pil)  # Convert to ImageTk PhotoImage

        title_label = Label(grid_frame, text=titles[i])
        title_label.grid(row=(i // 3) * 2, column=i % 3, padx=5, pady=(0, 5))

        label = Label(grid_frame, image=image_tk)
        label.image = image_tk  # Keep a reference to avoid garbage collection
        label.grid(row=(i // 3) * 2 + 1, column=i % 3, padx=5, pady=(0, 5)) 

def load_images():
    """Load images from the specified folder and return their file paths."""
    images = []
    titles = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            images.append(cv2.imread(os.path.join(IMAGE_FOLDER, filename), cv2.IMREAD_GRAYSCALE))
            titles.append(filename)
    return images, titles

def apply_transformations(selected_image):
    """Apply transformations to the selected image."""
    if selected_image is None:
        return

    binary_image = binary_threshold(selected_image)
    contrast_image = contrast_stretching(selected_image)
    negative_image = negative(selected_image)
    log_image = log_transformation(selected_image)
    gamma_image_low = gamma_correction(selected_image, gamma=0.5)  # γ < 1
    gamma_image_high = gamma_correction(selected_image, gamma=2.0)  # γ > 1

    images = [selected_image, binary_image, contrast_image, negative_image, log_image, gamma_image_low, gamma_image_high]
    titles = ['Original', 'Binary Threshold', 'Contrast Stretching', 'Negative', 'Log Transformation', 'Gamma < 1', 'Gamma > 1']

    display_images(images, titles)

def on_selection_change(event):
    """Handle selection change in the dropdown."""
    selected_image_name = dropdown_var.get()
    selected_image_path = os.path.join(IMAGE_FOLDER, selected_image_name)
    selected_image = cv2.imread(selected_image_path, cv2.IMREAD_GRAYSCALE)
    apply_transformations(selected_image)

# Set up the main Tkinter window
root = tk.Tk()
root.title("Image Transformations")

dropdown_var = StringVar()
dropdown_menu = ttk.Combobox(root, textvariable=dropdown_var)
dropdown_menu.bind("<<ComboboxSelected>>", on_selection_change)


# Load images for the dropdown
image_files = os.listdir(IMAGE_FOLDER)
dropdown_menu['values'] = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg'))]
dropdown_menu.pack(pady=10)


if image_files: 
    dropdown_var.set(image_files[0])

# Create a frame to hold the grid of images
grid_frame = tk.Frame(root)
grid_frame.pack()

on_selection_change(0)

# Start the Tkinter main loop
root.mainloop()
