import os
import random
import string
from PIL import Image
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
import threading 
import concurrent.futures

def resize_image(input_image, max_size=(10000, 10000)):
    width, height = input_image.size

    if width > max_size[0] or height > max_size[1]:
        ratio = min(max_size[0] / width, max_size[1] / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        input_image = input_image.resize((new_width, new_height), Image.ANTIALIAS)

    return input_image


def paste_image(png_files, used_image_indices, blank_image, cell_width, cell_height, grid_size_tuple):
    i, j = grid_size_tuple
    available_image_indices = [index for index in range(len(png_files)) if index not in used_image_indices]

    if not available_image_indices:
        used_image_indices = []

    if not available_image_indices:
        available_image_indices = list(range(len(png_files)))

    random_image_index = random.choice(available_image_indices)
    im = Image.open(png_files[random_image_index])

    blank_image.paste(im, (j * cell_width, i * cell_height))
    used_image_indices.append(random_image_index)
    return random_image_index

def main(output_dir, grid_size, quality, progress_label, window, max_size=(10000, 10000)):
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]

    first_image = Image.open(png_files[0])
    cell_width, cell_height = first_image.size

    blank_image = Image.new('RGB', (grid_size * cell_width, grid_size * cell_height))

    random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    used_image_indices = []

    grid_positions = [(i, j) for i in range(grid_size) for j in range(grid_size)]
    
    total_images = grid_size * grid_size
    counter = 1
    for pos in grid_positions:
        image_index = paste_image(png_files, used_image_indices, blank_image, cell_width, cell_height, pos)
        progress_label.config(text=f"Pasted image {counter}/{total_images} (Image #{image_index})")
        counter += 1
        window.update_idletasks()

    # Resize the final output image before saving
    blank_image = resize_image(blank_image, max_size)
    blank_image.save(os.path.join(output_dir, f'{random_filename}.jpg'), quality=quality)

def start_gui():
    window = tk.Tk()
    window.title("Gridder")
    progress_label = tk.Label(window, text="")
    progress_label.grid(row=6, column=1)
    # Add labels and input fields
    grid_size_label = tk.Label(window, text="Grid Size:")
    grid_size_input = tk.Entry(window)
    quality_label = tk.Label(window, text="Quality (1-100):")
    quality_input = tk.Entry(window)
    max_width_label = tk.Label(window, text="Max Width:")
    max_width_input = tk.Entry(window)
    max_height_label = tk.Label(window, text="Max Height:")
    max_height_input = tk.Entry(window)
    folder_label = tk.Label(window, text="Output folder (leave blank for current directory):")
    folder_input = tk.Entry(window)

    # Place labels and input fields in the grid
    grid_size_label.grid(row=0, column=0)
    grid_size_input.grid(row=0, column=1)
    quality_label.grid(row=1, column=0)
    quality_input.grid(row=1, column=1)
    max_width_label.grid(row=2, column=0)
    max_width_input.grid(row=2, column=1)
    max_height_label.grid(row=3, column=0)
    max_height_input.grid(row=3, column=1)
    folder_label.grid(row=4, column=0)
    folder_input.grid(row=4, column=1)

    def on_run_button_click():
        grid_size = int(grid_size_input.get())
        quality = int(quality_input.get())
        # Set max_width and max_height based on input or default values
        max_width = int(max_width_input.get()) if max_width_input.get() else 10000
        max_height = int(max_height_input.get()) if max_height_input.get() else 10000
        folder_path = folder_input.get().strip()

        if not folder_path:
            folder_path = os.path.join(os.getcwd(), "Images")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        else:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        main(folder_path, grid_size, quality, progress_label, window, (max_width, max_height))  # Pass max width and height as a tuple

    def on_browse_button_click():
        folder_path = filedialog.askdirectory()
        folder_input.delete(0, tk.END)
        folder_input.insert(0, folder_path)

    # Add button and place it in the grid
    run_button = tk.Button(window, text="Run", command=on_run_button_click)
    browse_button = tk.Button(window, text="Browse", command=on_browse_button_click)
    run_button.grid(row=5, column=1)
    browse_button.grid(row=4, column=2)

    window.mainloop()

if __name__ == "__main__":
    start_gui()
