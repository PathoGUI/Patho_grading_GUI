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
st.set_page_config(layout="wide")
st.title("Pathology Grading GUI")

# Create a dropdown to select the directory containing .tif images
base_directory = st.selectbox("Select the directory", [f for f in os.listdir("./") if os.path.isdir(os.path.join("./", f))]
)

if 'tags' not in st.session_state:
    st.session_state.tags = []



if os.path.isdir(base_directory):
    try:
        tif_files = [f for f in os.listdir(base_directory) if f.lower().endswith(".tif")]
    except Exception as e:
        st.error(f"No .tif images in selected directory")

    if tif_files:
        st.write(f"Found {len(tif_files)} .tif files in the selected directory.")
        
        # Create a dropdown to select an image from the directory
        selected_image_index = st.selectbox("Select an image", range(len(tif_files)), key="image_selector")
        
        # Create columns for side by side buttons:
        col1, col2 = st.columns(2)
        scol1, scol2, scol3 = col2.columns(3)
        # Next button
        if scol1.button("Next Image"):
            selected_image_index = st.session_state.selected_image_index  # Retrieve the current index
            if selected_image_index + 1 < len(tif_files):
                selected_image_index += 1
                st.session_state.selected_image_index = selected_image_index

        # Previous button
        if scol1.button("Previous Image"):
            selected_image_index = st.session_state.selected_image_index  # Retrieve the current index
            if selected_image_index - 1 >= 0:
                selected_image_index -= 1
                st.session_state.selected_image_index = selected_image_index

        # Display the selected image
        if selected_image_index is not None:
            selected_image = tif_files[selected_image_index]
            image_path = os.path.join(base_directory, selected_image)
            
            # Read the image
            image = Image.open(image_path)
            image = rotate_image(image, 90)
            
            # Create a button to rotate the image by 90 degrees
            if scol2.button("Rotate 90 Degrees"):
                image = rotate_image(image, 90)
            # Reset Rotation Button    
            if scol2.button("Reset Rotation"):
                image = rotate_image(image, 0)
            
            # Display the image
            col1.image(image, use_column_width=True, caption=f"Image {selected_image_index + 1} of {len(tif_files)}")

        else:
            st.write("No .tif files found in the selected directory.")
    else:
        st.write("The selected directory does not exist or is not a directory.")
    
    # Update selected image index in session state
    st.session_state.selected_image_index = selected_image_index
        
# st.write("Current Tags:", st.session_state.tags)

if 'applied_tags' not in st.session_state:
    st.session_state.applied_tags = [[] for _ in range(len(tif_files))]

# Text input to get the new tag from the user
new_tag = col2.text_input("Enter a new tag:")

col12, col22 = st.columns(2)
scol12, scol22, scol32 = col22.columns(3)
# Button to add the new tag to the list
if col2.button("Add Tag"):
    if new_tag:
        st.session_state.tags.append(new_tag)
        st.success(f'Tag "{new_tag}" added successfully!')
    else:
        st.warning("Please enter a tag before adding.")

# Selectbox to choose a tag from the current list
selected_tag = col2.selectbox("Select a tag:", st.session_state.tags, index=len(st.session_state.tags)-1 if st.session_state.tags else 0)

if scol12.button("Apply Selected Tag"):
    if st.session_state.applied_tags is None:
        st.session_state.applied_tags[selected_image_index] = [selected_tag]
    else:
        st.session_state.applied_tags[selected_image_index].append(selected_tag)

if scol22.button("Remove Selected Tag"):
    if selected_tag in st.session_state.applied_tags[selected_image_index]:
        st.session_state.applied_tags[selected_image_index].remove(selected_tag)

st.write("Tags Applied to this Image:")
st.write(st.session_state.applied_tags[selected_image_index])
    

# Display the selected tag
# st.write("Selected Tag:", selected_tag)

# Display the updated list of tags
# st.write("Updated Tags:", st.session_state.tags)

# Initialize session state for selected image index
if 'selected_image_index' not in st.session_state:
    st.session_state.selected_image_index = 0

# List .tif files in the selected directory
tif_files = list_tif_files(base_directory)

