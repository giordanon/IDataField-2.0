import streamlit as st
import cv2 as cv
import matplotlib.pyplot as plt
import os
import functions as fx

def app():
    st.title("Image Cropper")

    directory_path = st.text_input("Enter directory path:")

    if directory_path and os.path.isdir(directory_path):
        files = sorted(os.listdir(directory_path))

        repetitions = set()  # Set to store unique repetition numbers
        for file_name in files:
            repetition = file_name.split('-')[4][0]  # Extract first digit of repetition number from file name
            repetitions.add(repetition)
        col1, col2 = st.columns(2)
        with col1:
            selected_repetition = st.selectbox("Filter by Repetition", sorted(list(repetitions)))

        filtered_files = [file_name for file_name in files if file_name.split('-')[4][0] == selected_repetition]
        
        selected_file_index = st.session_state.get("selected_file_index", 0)
            
        if selected_file_index >= len(filtered_files):
            selected_file_index = len(filtered_files) - 1
        elif selected_file_index < 0:
            selected_file_index = 0
        with col2:
            selected_file = st.selectbox("Select Image", filtered_files, index=selected_file_index)

        if selected_file:
            image = cv.imread(os.path.join(directory_path, selected_file))
            
            col1, col2 = st.columns(2)
            with col1:
                rotation_angle = st.number_input("Rotation Angle", min_value=-180, max_value=180, value=0, step=1, format="%d", key="rotation_angle")  # Text input box for rotation angle
            with col2:
                top_text = st.number_input("Top", min_value=800, max_value=2000, value=1300, step=30, format="%d", key="top_text")  # Text input box for top value

            # Rotate the image based on the provided angle
            rows, cols, _ = image.shape
            rotation_matrix = cv.getRotationMatrix2D((cols/2, rows/2), rotation_angle, 1)
            rotated_image = cv.warpAffine(image, rotation_matrix, (cols, rows))

            # Display the cropped and rotated image
            cropped_image = fx.crop_image(rotated_image, top_text)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(cv.cvtColor(cropped_image, cv.COLOR_BGR2RGB))
            ax.axis('off')
            st.pyplot(fig)
    elif directory_path:
        st.write("Invalid directory path. Please enter a valid directory path.")

if __name__ == "__main__":
    main()


