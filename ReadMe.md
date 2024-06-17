# MRI Image Enhancement and Thresholding Tool

## Project Overview
This project is an interactive tool for enhancing MRI images using noise reduction techniques and applying manual threshold segmentation. The tool allows users to adjust the threshold value with a slider and compare the effects of different noise reduction methods (Bilateral Filter and Non-Local Means).

## Features
- Load and display MRI images from a specified folder.
- Apply Bilateral Filtering and Non-Local Means for noise reduction.
- Perform contrast adjustment using histogram equalization.
- Manually adjust the threshold value using a slider.
- View original, enhanced, and segmented images side by side.
- Navigate through multiple images in the folder using "Next" and "Previous" buttons.

## Technologies Used
- Python
- NumPy
- Matplotlib
- scikit-image
- Pillow (PIL)
- Tkinter

## Installation and Setup
1. **Clone the repository**:
    ```sh
    git clone https://github.com/albertozilli06/mri-image-enhancement.git
    cd mri-image-enhancement
    ```

2. **Install the required packages**:
    ```sh
    pip install numpy matplotlib scikit-image pillow
    ```

3. **Run the script**:
    - Ensure you have a folder containing JPEG images.
    - Update the `folder_path` variable in the script to point to your image folder.
    - Run the script:
        ```sh
        python main.py
        ```

## Usage
1. **Loading Images**:
    - The script will automatically load all JPEG images from the specified folder.

2. **Enhancing Images**:
    - The first image is enhanced using both Bilateral Filtering and Non-Local Means methods.

3. **Adjusting Threshold**:
    - Use the slider at the bottom of the window to adjust the threshold value.
    - The segmented images will update in real-time as you adjust the slider.

4. **Navigating Images**:
    - Use the "Next" button to move to the next image in the folder.
    - Use the "Previous" button to move to the previous image in the folder.

## Error Handling
- The script includes basic error handling to manage issues such as file not found or invalid image formats.
- If an error occurs while loading images, an error message will be printed and the process will continue with the next image.

## Future Enhancements
- Add a progress bar to show the status of image loading and processing.
- Allow users to select the folder path through a dialog box.
- Add more noise reduction and image enhancement methods for comparison.
- Implement automated thresholding methods in addition to manual adjustment.

## License
This project is licensed under the MIT License - see the License.txt file for details.


## Contact
For any questions or feedback, please contact:
- Name: Alberto Zilli
- Email: alberto.zilli06@gmail.com

LinkedIn: https://www.linkedin.com/in/alberto-zilli-937b92207/
GitHub: https://github.com/albertozilli06
