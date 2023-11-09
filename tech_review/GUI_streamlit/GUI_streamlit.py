import streamlit as st
import os
from PIL import Image

# Function to list .tif files in a directory
def list_tif_files(directory):
    tif_files = [f for f in os.listdir(f"./{directory}") if f.lower().endswith(".tif")]
    return tif_files

# Function to rotate the image by 90 degrees
def rotate_image(image, degrees):
    return image.rotate(degrees, expand=True)

# Create a Streamlit app
st.title("Pathology Grading UI")

# Create a dropdown to select the directory containing .tif images
base_directory = st.selectbox("Select the directory", [f for f in os.listdir("./") if os.path.isdir(os.path.join("./", f))]
)

if os.path.isdir(base_directory):
    tif_files = [f for f in os.listdir(base_directory) if f.lower().endswith(".tif")]
    
    if tif_files:
        st.write(f"Found {len(tif_files)} .tif files in the selected directory.")
        
        # Create a dropdown to select an image from the directory
        selected_image_index = st.selectbox("Select an image", range(len(tif_files) + 1), key="image_selector")
        
        # Display the selected image
        if selected_image_index is not None:
            selected_image = tif_files[selected_image_index]
            image_path = os.path.join(base_directory, selected_image)
            
            # Read the image
            image = Image.open(image_path)
            image = rotate_image(image, 90)
            
            # Create a button to rotate the image by 90 degrees
            if st.button("Rotate 90 Degrees"):
                image = rotate_image(image, 90)
            # Reset Rotation Button    
            if st.button("Reset Rotation"):
                image = rotate_image(image, 0)
            
            # Display the image
            st.image(image, use_column_width=True, caption=f"Image {selected_image_index + 1} of {len(tif_files)}")
            
    else:
        st.write("No .tif files found in the selected directory.")
else:
    st.write("The selected directory does not exist or is not a directory.")

# Initialize session state for selected image index
if 'selected_image_index' not in st.session_state:
    st.session_state.selected_image_index = 0

# List .tif files in the selected directory
tif_files = list_tif_files(base_directory)

# Update selected image index in session state
st.session_state.selected_image_index = selected_image_index

