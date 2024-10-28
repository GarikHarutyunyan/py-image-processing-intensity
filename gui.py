import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, StringVar
from tkinter import ttk
from PIL import Image, ImageTk
import os
from transformations import binary_threshold, contrast_stretching, negative, log_transformation, gamma_correction

# Folder containing images
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'images')
TRESHOLD_DEFAULT_VALUE = 127
CONTRAST_MIN_DEFAULT_VALUE = 0
CONTRAST_MAX_DEFAULT_VALUE = 255
LOG_FACTOR_DEFAULT_VALUE = 1.0
GAMMA_LOW_DEFAULT_VALUE = 0.5
GAMMA_HIGH_DEFAULT_VALUE = 2.0

def resize_image(image, width=200):
    height = int(image.shape[0] * (width / image.shape[1]))
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def display_images(images, titles, options):
    global binary_label, contrast_label, log_label, low_gamma_label, high_gamma_label # Make labels global to update later
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(len(images)):
        resized_image = resize_image(images[i])
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        title_label = Label(frame, text=titles[i])
        title_label.grid(row=(i // 7) * 2, column=i % 7, padx=5, pady=(0, 5))

        label = Label(frame, image=image_tk)
        label.image = image_tk
        label.grid(row=(i // 7) * 2 + 1, column=i % 7, padx=5, pady=(0, 5))
        
        get_option = options[i];
        if get_option is not None:
            get_option().grid(row=(i // 7) * 2+2, column=i % 7, padx=5, pady=(0, 5))

        # Keep a reference  labels
        if titles[i] == 'Binary Threshold':
            binary_label = label
        elif titles[i] == 'Contrast Stretching':
            contrast_label = label
        elif titles[i] == 'Log Transformation':
            log_label = label
        elif titles[i] == 'Gamma < 1':
            low_gamma_label = label
        elif titles[i] == 'Gamma > 1':
            high_gamma_label = label


def apply_transformations(selected_image):
    global original_image, frame
    if selected_image is None:
        return
    
    def get_treshold_option():
        # Scale for binary threshold
        threshold_scale = tk.Scale(frame, from_=0, to=255, orient='horizontal', label='Threshold', command=on_threshold_change)
        threshold_scale.set(TRESHOLD_DEFAULT_VALUE)
        return threshold_scale

    def get_contrast_option():        
        global min_val_scale, max_val_scale
        # Scales for contrast stretching
        options_frame = tk.Frame(frame)
        # options_frame.pack(padx=10, pady=10)
        min_val_scale = tk.Scale(options_frame, from_=0, to=255, orient='horizontal', label='Contrast Min Value', command=on_min_val_change)
        min_val_scale.set(CONTRAST_MIN_DEFAULT_VALUE)        
        min_val_scale.grid(column=1, row=0)
        max_val_scale = tk.Scale(options_frame, from_=0, to=255, orient='horizontal', label='Contrast Max Value', command=on_max_val_change)
        max_val_scale.set(CONTRAST_MAX_DEFAULT_VALUE)
        max_val_scale.grid(column=2, row=0)
        return options_frame
    
    def get_log_option():
        log_scale = tk.Scale(frame, from_=0.1, to=10.0, orient='horizontal', resolution=0.1, label='Log Scale Factor', command=on_log_change)
        log_scale.set(LOG_FACTOR_DEFAULT_VALUE)
        return log_scale
    
    def get_gamma_low_option():
        scale = tk.Scale(frame, from_=0.1, to=1.0, orient='horizontal', resolution=0.1, label='Gamma < 1 Factor', command=on_low_gamma_change)
        scale.set(GAMMA_LOW_DEFAULT_VALUE) 
        return scale
    
    def get_gamma_high_option():
        scale = tk.Scale(frame, from_=1.0, to=3.0, orient='horizontal', resolution=0.1, label='Gamma > 1 Factor', command=on_high_gamma_change)
        scale.set(GAMMA_HIGH_DEFAULT_VALUE) 
        return scale

    original_image = selected_image

    binary_image = binary_threshold(selected_image, threshold=TRESHOLD_DEFAULT_VALUE)
    contrast_image = contrast_stretching(selected_image, min_val=CONTRAST_MIN_DEFAULT_VALUE, max_val=CONTRAST_MAX_DEFAULT_VALUE)
    negative_image = negative(selected_image)
    log_image = log_transformation(selected_image, LOG_FACTOR_DEFAULT_VALUE)
    gamma_image_low = gamma_correction(selected_image, gamma=GAMMA_LOW_DEFAULT_VALUE)
    gamma_image_high = gamma_correction(selected_image, gamma=2.0)

    images = [selected_image, binary_image, contrast_image, negative_image, log_image, gamma_image_low, gamma_image_high]
    titles = ['Original', 'Binary Threshold', 'Contrast Stretching', 'Negative', 'Log Transformation', 'Gamma < 1', 'Gamma > 1']
    options = [None, get_treshold_option, get_contrast_option, None, get_log_option, get_gamma_low_option, get_gamma_high_option]

    display_images(images, titles, options)

def on_selection_change(event):
    print(event)
    selected_image_name = dropdown_var.get()
    selected_image_path = os.path.join(IMAGE_FOLDER, selected_image_name)
    selected_image = cv2.imread(selected_image_path, cv2.IMREAD_GRAYSCALE)
    apply_transformations(selected_image)

def on_threshold_change(value):
    global original_image, binary_label
    if original_image is None:
        return

    threshold_value = int(value)
    binary_image = binary_threshold(original_image, threshold=threshold_value)
    resized_image = resize_image(binary_image)
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)

    binary_label.config(image=image_tk)
    binary_label.image = image_tk

def on_min_val_change(_):
    on_contrast_change()

def on_max_val_change(_):
    on_contrast_change()

def on_contrast_change():
    global original_image, contrast_label, min_val_scale, max_val_scale
    if original_image is None:
        return

    min_val = min_val_scale.get()
    max_val = max_val_scale.get()
    contrast_image = contrast_stretching(original_image, min_val=min_val, max_val=max_val)
    resized_image = resize_image(contrast_image)
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)

    contrast_label.config(image=image_tk)
    contrast_label.image = image_tk

def on_log_change(value):
    global original_image, log_label
    if original_image is None:
        return

    log_value = float(value)
    binary_image = log_transformation(original_image, log_factor=log_value)
    resized_image = resize_image(binary_image)
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)

    log_label.config(image=image_tk)
    log_label.image = image_tk

def on_low_gamma_change(value):
    global original_image, low_gamma_label
    if original_image is None:
        return

    low_gamma = float(value)
    binary_image = gamma_correction(original_image, gamma=low_gamma)
    resized_image = resize_image(binary_image)
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)

    low_gamma_label.config(image=image_tk)
    low_gamma_label.image = image_tk

def on_high_gamma_change(value):
    global original_image, high_gamma_label
    if original_image is None:
        return

    high_gamma = float(value)
    binary_image = gamma_correction(original_image, gamma=high_gamma)
    resized_image = resize_image(binary_image)
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)

    high_gamma_label.config(image=image_tk)
    high_gamma_label.image = image_tk

# Set up the main Tkinter window
root = tk.Tk()
root.title("Image Transformations")
root.state('zoomed')
# root.attributes('-zoomed', True) # For Linux and macOS


# Set up the dropdown menu
dropdown_var = StringVar()
dropdown_menu = ttk.Combobox(root, textvariable=dropdown_var)
dropdown_menu.bind("<<ComboboxSelected>>", on_selection_change)

image_files = os.listdir(IMAGE_FOLDER)
dropdown_menu['values'] = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg'))]
dropdown_menu.pack(pady=10)

if image_files:
    dropdown_var.set(image_files[0])

# Frame for displaying images
frame = tk.Frame(root)
frame.pack(padx=10, pady=200)

original_image = None
binary_label = None
contrast_label = None

# Responsible for initial rendering
on_selection_change(0)

# Start the Tkinter main loop
root.mainloop()
