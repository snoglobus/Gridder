To set up and run the modified code, follow these steps:

1. **Install Python 3:**

   Make sure you have Python 3 installed on your computer. If you don't have it, download and install Python 3 from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Create a new folder:**

   Create a folder on your computer where you want to store the script and images.

3. **Save the script:**

   Save the modified code provided above as a file named "gridder.py" in the new folder you created.

4. **Install required libraries:**

   Open the terminal (Command Prompt on Windows) and navigate to the folder where you saved the script. Then, run the following commands to install the required libraries:
   ```
   pip install pillow
   pip install tqdm
   ```

5. **Run the script:**

   After installing the required libraries, run the script using the terminal by typing:
   ```
   python gridder.py
   ```

   This will open a graphical user interface where you can input the grid size (1 Number), quality (1-100%), and output folder, or it will default to the "Images" output folder.

6. **Add images:**

   Copy all the images (PNG files) you want to use for creating the grid image into the same folder where the script is saved.

7. **Using the graphical interface:**

   Input the grid size (1 Number)), the image quality (1-100%), and an output folder if necessary, or leave the output folder field empty to use the default "Images" folder. If you want to select a different output folder, click "Browse" to open a folder dialog. After setting all the options, click "Run" to start generating the grid image. The final image will be saved in the specified output folder.

   Please note that running the script may take some time, depending on the number of images and selected grid size. After the process is finished, you should find the grid image in the specified output folder.
