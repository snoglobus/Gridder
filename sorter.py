import os
import shutil
from PIL import Image
import zipfile

def extract_images_from_zip(input_folder):
    extracted_folder_name = "extracted_images"
    extracted_folder = os.path.join(os.getcwd(), extracted_folder_name)
    os.makedirs(extracted_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith('.zip') and 'midjourney' in file_name.lower():
            with zipfile.ZipFile(os.path.join(input_folder, file_name), 'r') as zip_ref:
                zip_ref.extractall(extracted_folder)

    return extracted_folder

def sort_images_by_exact_size(input_folder):
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img = Image.open(os.path.join(input_folder, file_name))
            width, height = img.size

            output_folder = f"{width}x{height}"
            full_path = os.path.join(os.getcwd(), output_folder)

            if not os.path.exists(full_path):
                os.makedirs(full_path)
                
            os.rename(os.path.join(input_folder, file_name), os.path.join(full_path, file_name))

if __name__ == '__main__':
    input_folder = os.getcwd()

    if input_folder:
        extracted_folder = extract_images_from_zip(input_folder)
        
        if extracted_folder:
            sort_images_by_exact_size(extracted_folder)
            shutil.rmtree(extracted_folder)
        else:
            print("No images found to extract")
    else:
        print("No directory selected")
