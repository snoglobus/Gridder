import os
import re
import random
import string
from PIL import Image
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def resize_image(input_image, max_size=(10000, 10000)):
    width, height = input_image.size

    resize_needed = False

    if width > max_size[0]:
        ratio_w = max_size[0] / width
        resize_needed = True
    else:
        ratio_w = 1

    if height > max_size[1]:
        ratio_h = max_size[1] / height
        resize_needed = True
    else:
        ratio_h = 1

    if resize_needed:
        ratio = min(ratio_w, ratio_h)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        input_image = input_image.resize((new_width, new_height), Image.ANTIALIAS)

    return input_image


def paste_image(png_files, used_image_indices, blank_image, cell_width, cell_height, grid_tuple):
    i, j = grid_tuple
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

    blank_image = Image.new('RGB', (grid_size[0] * cell_width, grid_size[1] * cell_height))

    random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    used_image_indices = []

    grid_positions = [(j, i) for i in range(grid_size[0]) for j in range(grid_size[1])]

    total_images = grid_size[0] * grid_size[1]
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
    progress_label.grid(row=12, column=1)
    grid_width_label = tk.Label(window, text="Grid Width:")
    grid_width_input = tk.Entry(window)
    grid_height_label = tk.Label(window, text="Grid Height:")
    grid_height_input = tk.Entry(window)
    quality_label = tk.Label(window, text="Quality (1-100):")
    quality_input = tk.Entry(window)
    max_width_label = tk.Label(window, text="Max Width:")
    max_width_input = tk.Entry(window)
    max_height_label = tk.Label(window, text="Max Height:")
    max_height_input = tk.Entry(window)
    folder_label = tk.Label(window, text="Output folder (leave blank for current directory):")
    folder_input = tk.Entry(window)
    initial_directory = os.getcwd()
    grid_width_label.grid(row=0, column=0)
    grid_width_input.grid(row=0, column=1)
    grid_height_label.grid(row=1, column=0)
    grid_height_input.grid(row=1, column=1)
    quality_label.grid(row=2, column=0)
    quality_input.grid(row=2, column=1)
    max_width_label.grid(row=3, column=0)
    max_width_input.grid(row=3, column=1)
    max_height_label.grid(row=4, column=0)
    max_height_input.grid(row=4, column=1)
    folder_label.grid(row=5, column=0)
    folder_input.grid(row=5, column=1)
    input_folder_label = tk.Label(window, text="Input Folder:")
    input_folder_label.grid(row=6, column=0)
    
    def update_folder_input():
        input_directory = input_dir_var.get()
        if input_directory == "Default":
            folder_input.delete(0, tk.END)
            folder_input.insert(0, os.getcwd())
        else:
            folder_input.delete(0, tk.END)
            folder_input.insert(0, input_directory)

    input_dir_var = tk.StringVar(window)
    input_dir_var.set("Default")
    input_dir_options = [folder for folder in os.listdir(os.getcwd()) if re.match(r'\d+x\d+', folder)]
    input_dir_options.insert(0, "Default")
    input_dir_dropdown = tk.OptionMenu(window, input_dir_var, *input_dir_options, command=None)  # Changed command to None
    input_dir_dropdown.grid(row=6, column=1)

    def on_sort_button_click():
        script_path = os.path.abspath(__file__)  # Get the full path of the main script
        script_dir = os.path.dirname(script_path)  # Get the directory of the main script
        sorter_path = os.path.join(script_dir, 'sorter.py')  # Construct the absolute path to the sorter.py file
        os.system(f'python3 {sorter_path}')
        update_folder_input()
        messagebox.showinfo("Done", "Images have been sorted!")

    def on_run_button_click():
        grid_width = int(grid_width_input.get()) if grid_width_input.get() else 5
        grid_height = int(grid_height_input.get()) if grid_height_input.get() else 5
        grid_size = (grid_width, grid_height)
        quality = int(quality_input.get()) if quality_input.get() else 5
        max_width = int(max_width_input.get()) if max_width_input.get() else 10000
        max_height = int(max_height_input.get()) if max_height_input.get() else 10000
        input_folder_path = input_dir_var.get()
        if input_folder_path == "Default":
            input_folder_path = os.getcwd()

        os.chdir(input_folder_path)
        png_files = [f for f in os.listdir('.') if f.endswith('.png')]
        if not png_files:
            messagebox.showerror("Error", "There are no PNG files in the input folder.")
            return

        folder_path = os.path.join(initial_directory, "Images")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        main(folder_path, grid_size, quality, progress_label, window, (max_width, max_height))
        # Reset the working directory
        os.chdir(initial_directory)
        messagebox.showinfo("Done!", "Image has been generated and saved in the output folder.")

    def on_browse_button_click():
        folder_path = filedialog.askdirectory()
        folder_input.delete(0, tk.END)
        folder_input.insert(0, folder_path)

    run_button = tk.Button(window, text="Run", command=on_run_button_click)
    browse_button = tk.Button(window, text="Browse", command=on_browse_button_click)
    sort_button = tk.Button(window, text="Sort First", command=on_sort_button_click)
    sort_button.grid(row=7,column=1)
    run_button.grid(row=7, column=2)
    browse_button.grid(row=5, column=3)

    window.mainloop()

if __name__ == "__main__":
    start_gui()
